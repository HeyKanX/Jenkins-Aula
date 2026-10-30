// P8 (consigna): mensajes validos cortos y cercanos a 1000 caracteres; medir latencia y HTTP 201.
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost o 127.0.0.1.');
}
const duracionCorto = new Trend('duracion_mensaje_corto_ms', true);
const duracionCercaLimite = new Trend('duracion_mensaje_cerca_limite_ms', true);
export const options = {
  vus: 4,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const largo = (__VU + __ITER) % 2 === 0;
  const cuerpo = largo ? 'A'.repeat(995) : 'Consulta corta de prueba.';
  const tipo = largo ? 'cerca_de_1000' : 'corto';
  const mensaje = {
    courseId: 'calc-201',
    subject: `Tamano ${tipo} VU${__VU} I${__ITER}`,
    body: cuerpo,
  };
  const respuesta = http.post(`${BASE_URL}/api/messages`, JSON.stringify(mensaje), {
    headers: { 'Content-Type': 'application/json' },
    tags: { caso: 'P8', tamano: tipo },
  });
  if (largo) duracionCercaLimite.add(respuesta.timings.duration);
  else duracionCorto.add(respuesta.timings.duration);
  let datos;
  try { datos = respuesta.json(); } catch (_) { datos = null; }
  check(respuesta, {
    'P8: POST devuelve HTTP 201': (r) => r.status === 201,
    'P8: mantiene tamano del contenido enviado': () => Boolean(datos && datos.message && datos.message.body === cuerpo),
  });
  sleep(2);
}
