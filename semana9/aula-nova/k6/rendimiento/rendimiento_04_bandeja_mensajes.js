// P4 (consigna): GET /api/messages sobre bandeja inicialmente vacia; p95 < 300 ms.
// Si ejecutaste P6/P7/P8 antes, reinicia 'npm start' para vaciar la memoria.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost o 127.0.0.1.');
}
export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

function jsonSeguro(respuesta) {
  try { return respuesta.json(); } catch (_) { return null; }
}

export function setup() {
  const respuesta = http.get(`${BASE_URL}/api/messages`, { tags: { caso: 'P4', etapa: 'precondicion' } });
  const datos = jsonSeguro(respuesta);
  if (respuesta.status !== 200 || !datos || !Array.isArray(datos.messages) || datos.messages.length !== 0) {
    throw new Error('P4 requiere bandeja vacia: reinicia el servidor Node.js y vuelve a ejecutar P4.');
  }
}

export default function () {
  const respuesta = http.get(`${BASE_URL}/api/messages`, { tags: { caso: 'P4', etapa: 'medicion' } });
  const datos = jsonSeguro(respuesta);
  check(respuesta, {
    'P4: mensajes devuelve HTTP 200': (r) => r.status === 200,
    'P4: respuesta es JSON con lista de mensajes': () => Boolean(datos && Array.isArray(datos.messages)),
    'P4: bandeja sigue vacia': () => Boolean(datos && Array.isArray(datos.messages) && datos.messages.length === 0),
  });
  sleep(1);
}
