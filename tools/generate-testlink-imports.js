/*
 * Genera archivos XML compatibles con la importación de casos de TestLink.
 * Los casos se obtienen de las pruebas ya existentes de las semanas 8 y 9.
 */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const output = path.join(root, 'testlink', 'imports');

function xml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function humanize(value) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, letter => letter.toUpperCase());
}

function filesRecursively(folder, extension) {
  return fs.readdirSync(folder, { withFileTypes: true }).flatMap(item => {
    const itemPath = path.join(folder, item.name);
    if (item.isDirectory()) return filesRecursively(itemPath, extension);
    return item.name.endsWith(extension) ? [itemPath] : [];
  });
}

function pythonCases(folder, tool) {
  const found = [];
  for (const file of filesRecursively(folder, '.py')) {
    const content = fs.readFileSync(file, 'utf8');
    for (const match of content.matchAll(/^\s+def test_tc(\d+)_([a-z0-9_]+)\(/gm)) {
      found.push({
        id: `TC-${match[1].padStart(2, '0')}`,
        title: `TC-${match[1].padStart(2, '0')} - ${humanize(match[2])} (${tool})`,
      });
    }
  }
  return found.sort((a, b) => Number(a.id.slice(3)) - Number(b.id.slice(3)));
}

function featureCases(folder) {
  const found = [];
  for (const file of filesRecursively(folder, '.feature')) {
    const content = fs.readFileSync(file, 'utf8');
    for (const match of content.matchAll(/^\s*Scenario:\s*(TC-\d+\s*-\s*.+)$/gm)) {
      const title = match[1].trim();
      found.push({ id: title.match(/^TC-\d+/)[0], title });
    }
  }
  return found.sort((a, b) => Number(a.id.slice(3)) - Number(b.id.slice(3)));
}

function k6Cases(folder, prefix) {
  return filesRecursively(folder, '.js')
    .sort()
    .map(file => {
      const stem = path.basename(file, '.js');
      const match = stem.match(/_(\d+)_/);
      const number = match ? match[1] : '00';
      const description = stem.replace(/^[a-z]+_\d+_/, '');
      return {
        id: `${prefix}-${number}`,
        title: `${prefix}-${number} - ${humanize(description)} (k6)`,
      };
    });
}

function testCaseXml(testCase, externalId, tool) {
  return `  <testcase name="${xml(testCase.title)}">\n` +
    `    <node_order><![CDATA[${externalId}]]></node_order>\n` +
    `    <externalid><![CDATA[${externalId}]]></externalid>\n` +
    '    <version><![CDATA[1]]></version>\n' +
    `    <summary><![CDATA[<p>Caso ${testCase.id} automatizado con ${tool}.</p>]]></summary>\n` +
    '    <preconditions><![CDATA[<p>La aplicación y el entorno de pruebas están disponibles.</p>]]></preconditions>\n' +
    '    <execution_type><![CDATA[2]]></execution_type>\n' +
    '    <importance><![CDATA[2]]></importance>\n' +
    '    <steps>\n' +
    '      <step>\n' +
    '        <step_number><![CDATA[1]]></step_number>\n' +
    `        <actions><![CDATA[<p>Ejecutar ${testCase.id} mediante ${tool}.</p>]]></actions>\n` +
    '        <expectedresults><![CDATA[<p>El caso cumple los criterios de aceptación definidos.</p>]]></expectedresults>\n' +
    '        <execution_type><![CDATA[2]]></execution_type>\n' +
    '      </step>\n' +
    '    </steps>\n' +
    '  </testcase>';
}

function writeImport(filename, cases, startId, tool) {
  const content = ['<?xml version="1.0" encoding="UTF-8"?>', '<testcases>'];
  cases.forEach((testCase, index) => content.push(testCaseXml(testCase, startId + index, tool)));
  content.push('</testcases>', '');
  fs.writeFileSync(path.join(output, filename), content.join('\n'), 'utf8');
}

fs.mkdirSync(output, { recursive: true });

const tienda = path.join(root, 'semana8', 'tienda-demo');
const aula = path.join(root, 'semana9', 'aula-nova');

writeImport('semana8_selenium.xml', pythonCases(path.join(tienda, 'selenium', 'tests'), 'Selenium'), 1, 'Selenium');
writeImport('semana8_playwright.xml', pythonCases(path.join(tienda, 'playwright_tests', 'tests'), 'Playwright'), 101, 'Playwright');
writeImport('semana8_uat.xml', featureCases(path.join(tienda, 'features')), 201, 'Behave (UAT)');
writeImport('semana9_funcionales.xml', featureCases(path.join(aula, 'tests', 'functional', 'features')), 301, 'Behave');
writeImport('semana9_rendimiento_k6.xml', k6Cases(path.join(aula, 'k6', 'rendimiento'), 'P'), 401, 'Grafana k6');
writeImport('semana9_estres_k6.xml', k6Cases(path.join(aula, 'k6', 'estres'), 'E'), 411, 'Grafana k6');
writeImport('semana9_seguridad_k6.xml', k6Cases(path.join(aula, 'k6', 'seguridad'), 'S'), 421, 'Grafana k6');

console.log(`Archivos de importación generados en: ${output}`);
