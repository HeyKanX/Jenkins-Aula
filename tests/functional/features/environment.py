import re
import socket
import subprocess
import time
import urllib.request
import os
import sys
from pathlib import Path


FUNCTIONAL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = FUNCTIONAL_ROOT.parents[1]

if str(FUNCTIONAL_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTIONAL_ROOT))

from utils.driver_factory import create_driver


def available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def start_isolated_server():
    port = available_port()
    environment = os.environ.copy()
    environment["PORT"] = str(port)
    process = subprocess.Popen(
        ["node", "backend/server.js"],
        cwd=PROJECT_ROOT,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 10

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{base_url}/api/messages", timeout=1):
                return process, base_url
        except OSError:
            time.sleep(0.1)

    process.terminate()
    raise RuntimeError("No se pudo iniciar el servidor aislado de Aula Nova.")


def before_scenario(context, scenario):
    tags = set(scenario.tags) | set(getattr(scenario.feature, "tags", []))
    context.server_process = None

    if "messages" in tags:
        context.server_process, context.base_url = start_isolated_server()
    else:
        context.base_url = "http://127.0.0.1:3000"

    context.driver = create_driver()


def after_scenario(context, scenario):
    evidence_dir = FUNCTIONAL_ROOT / "evidencias"
    evidence_dir.mkdir(exist_ok=True)

    status = getattr(scenario.status, "name", str(scenario.status)).lower()
    result = "aprobado" if status.endswith("passed") else "fallido"
    file_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", scenario.name)

    driver = getattr(context, "driver", None)
    if driver:
        driver.save_screenshot(str(evidence_dir / f"{result}_{file_name}.png"))
        driver.quit()

    process = getattr(context, "server_process", None)
    if process:
        process.terminate()
        process.wait(timeout=5)
