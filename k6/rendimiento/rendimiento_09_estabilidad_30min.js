// P9 (consigna): 30 minutos de lecturas moderadas; comparar p95 y errores cada 5 minutos.
// Una ejecucion corta NO cumple los 30 minutos requeridos: usar k6 run (sin --duration).
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
  new Trend('latencia_min_00_05', true),
  new Trend('latencia_min_05_10', true),
  new Trend('latencia_min_10_15', true),
  new Trend('latencia_min_15_20', true),
  new Trend('latencia_min_20_25', true),
  new Trend('latencia_min_25_30', true),
];
const errores = [
  new Rate('errores_min_00_05'),
  new Rate('errores_min_05_10'),
  new Rate('errores_min_10_15'),
  new Rate('errores_min_15_20'),
  new Rate('errores_min_20_25'),
  new Rate('errores_min_25_30'),
];
export const options = {
  vus: 10,
  duration: '30m',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const tiempoMs = Date.now() - exec.scenario.startTime;
  const bloque = Math.max(0, Math.min(5, Math.floor(tiempoMs / (5 * 60 * 1000))));
  const ruta = RUTAS[(__VU + __ITER) % RUTAS.length];
  const respuesta = http.get(`${BASE_URL}${ruta}`, {
    tags: { caso: 'P9', ruta, intervalo_5min: String(bloque + 1) },
  });
  const bien = respuesta.status === 200;
  duraciones[bloque].add(respuesta.timings.duration);
  errores[bloque].add(!bien);
  check(respuesta, { 'P9: lecturas disponibles durante la ejecucion': (r) => r.status === 200 });
  sleep(1);
}
