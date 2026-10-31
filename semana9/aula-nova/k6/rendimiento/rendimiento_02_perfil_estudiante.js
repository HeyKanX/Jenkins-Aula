// P2 (consigna): GET /api/student; HTTP 200, JSON valido y p95 < 300 ms.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1|aula-nova)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost, 127.0.0.1 o Aula Nova en Docker.');
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

export default function () {
  const respuesta = http.get(`${BASE_URL}/api/student`, { tags: { caso: 'P2' } });
  const datos = jsonSeguro(respuesta);
  check(respuesta, {
    'P2: perfil devuelve HTTP 200': (r) => r.status === 200,
    'P2: JSON contiene datos del estudiante': () => Boolean(datos && datos.student &&
      typeof datos.student.firstName === 'string' && typeof datos.student.email === 'string'),
  });
  sleep(1);
}
