#!/usr/bin/env python3
"""Publica en TestLink los resultados producidos por las suites de CI.

No contiene claves. Recibe TESTLINK_DEVKEY mediante secretos del pipeline.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from xmlrpc.client import ServerProxy, Fault, ProtocolError

ROOT = Path(__file__).resolve().parents[1]
PLAN_NAME = os.getenv("TESTLINK_PLAN_NAME", "Plan de Pruebas - Semana 11")
BUILD_NAME = os.getenv("TESTLINK_BUILD_NAME", "Build CI - Semana 11")
PROJECT_NAME = os.getenv("TESTLINK_PROJECT_NAME", "Semana 11 - TiendaDemo y Aula Nova")
URL = os.getenv("TESTLINK_URL", "").strip()
DEV_KEY = os.getenv("TESTLINK_DEVKEY", "").strip()
PIPELINE_ID = os.getenv("TESTLINK_PIPELINE_ID", "ejecución local")


def result_status(case: ET.Element) -> tuple[str, str]:
    failure = case.find("failure")
    error = case.find("error")
    if failure is not None or error is not None:
        detail = " ".join((failure if failure is not None else error).itertext()).strip()
        return "f", detail[:1000] or "La prueba registró un fallo."
    if case.find("skipped") is not None:
        return "b", "La prueba fue omitida o bloqueada durante la ejecución."
    return "p", "La prueba finalizó correctamente."


def junit_cases(pattern: str, offset: int, tool: str) -> list[dict]:
    results: dict[str, dict] = {}
    for filename in glob.glob(str(ROOT / pattern), recursive=True):
        try:
            root = ET.parse(filename).getroot()
        except ET.ParseError:
            continue
        for case in root.iter("testcase"):
            text = " ".join([case.attrib.get("name", ""), case.attrib.get("classname", "")])
            match = re.search(r"test_tc0*(\d{1,2})(?:_|\b)", text, re.IGNORECASE)
            if not match:
                match = re.search(r"TC-(\d{1,2})\b", text, re.IGNORECASE)
            if not match:
                continue
            status, detail = result_status(case)
            external = f"S11-{offset + int(match.group(1)) - 1}"
            results[external] = {
                "external": external,
                "status": status,
                "tool": tool,
                "detail": detail,
            }
    return list(results.values())


def k6_cases(folder: str, offset: int, label: str) -> list[dict]:
    results = []
    for filename in sorted(glob.glob(str(ROOT / "reports" / "k6" / folder / "*.json"))):
        match = re.search(r"_(\d{2})_", Path(filename).stem)
        if not match:
            continue
        try:
            summary = json.loads(Path(filename).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        passed = True
        for metric in summary.get("metrics", {}).values():
            for threshold in metric.get("thresholds", {}).values():
                threshold_failed = (
                    threshold is False
                    or (isinstance(threshold, dict) and threshold.get("ok") is False)
                )
                if threshold_failed:
                    passed = False
        checks = summary.get("metrics", {}).get("checks", {}).get("values", {})
        if checks.get("fails", 0) > 0:
            passed = False
        number = int(match.group(1))
        external = f"S11-{offset + number - 1}"
        results.append({
            "external": external,
            "status": "p" if passed else "f",
            "tool": f"Grafana k6 ({label})",
            "detail": "Los umbrales y verificaciones de k6 aprobaron." if passed else "Uno o más umbrales o verificaciones de k6 fallaron.",
        })
    return results


def collect_results() -> list[dict]:
    collected = []
    collected.extend(junit_cases("reports/selenium/**/*.xml", 1, "Selenium"))
    collected.extend(junit_cases("reports/playwright/**/*.xml", 101, "Playwright"))
    collected.extend(junit_cases("semana9/aula-nova/tests/functional/reports/*.xml", 301, "Behave funcional"))
    collected.extend(k6_cases("rendimiento", 401, "Rendimiento"))
    collected.extend(k6_cases("estres", 411, "Estrés"))
    collected.extend(k6_cases("seguridad", 421, "Seguridad"))
    return collected


def api_error(value: object) -> bool:
    return isinstance(value, list) and value and isinstance(value[0], dict) and "code" in value[0]


def main() -> int:
    if not URL or not DEV_KEY:
        print("TestLink no configurado: faltan TESTLINK_URL o TESTLINK_DEVKEY.")
        return 2

    results = collect_results()
    if not results:
        print("No se encontraron resultados de prueba para publicar en TestLink.")
        return 3

    server = ServerProxy(URL, allow_none=True)
    try:
        plan = server.tl.getTestPlanByName({
            "devKey": DEV_KEY,
            "testprojectname": PROJECT_NAME,
            "testplanname": PLAN_NAME,
        })
        if api_error(plan):
            raise RuntimeError(plan[0].get("message", "No se encontró el plan de pruebas."))
        if isinstance(plan, list):
            if not plan:
                raise RuntimeError("TestLink no devolvió datos del plan de pruebas.")
            plan = plan[0]
        plan_id = plan["id"]
        builds = server.tl.getBuildsForTestPlan({"devKey": DEV_KEY, "testplanid": plan_id}) or []
        build = next((item for item in builds if item.get("name") == BUILD_NAME), None)
        if not build:
            raise RuntimeError(f"No se encontró el Build '{BUILD_NAME}'.")
    except (Fault, ProtocolError, OSError, RuntimeError) as error:
        print(f"No fue posible preparar la publicación en TestLink: {error}", file=sys.stderr)
        return 4

    published, failed = [], []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    for result in results:
        note = (
            f"Herramienta: {result['tool']}\n"
            f"Estado CI: {result['status']}\n"
            f"Fecha UTC: {timestamp}\n"
            f"Pipeline: {PIPELINE_ID}\n"
            f"Detalle: {result['detail']}"
        )
        try:
            response = server.tl.reportTCResult({
                "devKey": DEV_KEY,
                "testplanid": plan_id,
                "buildid": build["id"],
                "testcaseexternalid": result["external"],
                "status": result["status"],
                "notes": note,
                "overwrite": True,
            })
            if api_error(response) or not response or not response[0].get("status"):
                message = response[0].get("message", str(response)) if response else "Sin respuesta"
                raise RuntimeError(message)
            published.append(result)
        except (Fault, ProtocolError, OSError, RuntimeError) as error:
            failed.append({**result, "error": str(error)})

    output = ROOT / "reports" / "testlink"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "project": PROJECT_NAME,
        "plan": PLAN_NAME,
        "build": BUILD_NAME,
        "pipeline": PIPELINE_ID,
        "published": published,
        "failed": failed,
    }
    (output / "resultados-testlink.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TestLink: {len(published)} resultados publicados; {len(failed)} errores.")
    return 0 if not failed else 5


if __name__ == "__main__":
    raise SystemExit(main())
