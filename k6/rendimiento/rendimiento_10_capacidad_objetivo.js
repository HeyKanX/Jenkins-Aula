// P10 (consigna): aumentar usuarios en etapas y estimar concurrencia que conserva los umbrales.
// Cambiar rampas desde PowerShell usando --stage; no se necesita editar este archivo.
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';
import exec from 'k6/execution';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost o 127.0.0.1.');
}
const RUTAS = ['/', '/api/student', '/api/courses', '/api/messages'];
const duraciones = [
  new Trend('latencia_01_10_vus', true),
  new Trend('latencia_11_20_vus', true),
  new Trend('latencia_21_30_vus', true),
  new Trend('latencia_31_40_vus', true),
  new Trend('latencia_mas_40_vus', true),
];
const errores = [
  new Rate('errores_01_10_vus'),
  new Rate('errores_11_20_vus'),
  new Rate('errores_21_30_vus'),
  new Rate('errores_31_40_vus'),
  new Rate('errores_mas_40_vus'),
];
export const options = {
  stages: [
    { duration: '15s', target: 10 },
    { duration: '30s', target: 20 },
    { duration: '30s', target: 30 },
    { duration: '30s', target: 40 },
    { duration: '15s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const cantidadVU = exec.instance.vusActive;
  const rango = cantidadVU <= 10 ? 0 : cantidadVU <= 20 ? 1 : cantidadVU <= 30 ? 2 : cantidadVU <= 40 ? 3 : 4;
  const ruta = RUTAS[(__VU + __ITER) % RUTAS.length];
  const respuesta = http.get(`${BASE_URL}${ruta}`, { tags: { caso: 'P10', ruta, rango_vus: String(rango + 1) } });
  const bien = respuesta.status === 200;
  duraciones[rango].add(respuesta.timings.duration);
  errores[rango].add(!bien);
  check(respuesta, { 'P10: rutas responden HTTP 200': (r) => r.status === 200 });
  sleep(1);
}
