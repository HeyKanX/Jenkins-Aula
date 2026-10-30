// P3 (consigna): GET /api/courses, cursos y notas presentes; p95 < 300 ms.
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

export default function () {
  const respuesta = http.get(`${BASE_URL}/api/courses`, { tags: { caso: 'P3' } });
  const datos = jsonSeguro(respuesta);
  check(respuesta, {
    'P3: cursos devuelve HTTP 200': (r) => r.status === 200,
    'P3: JSON incluye los cuatro cursos': () => Boolean(datos && Array.isArray(datos.courses) && datos.courses.length === 4),
    'P3: cursos incluyen calificaciones T1, T2, T3 y Final': () => Boolean(
      datos && Array.isArray(datos.courses) && datos.courses.length > 0 && datos.courses.every((c) =>
        c.grades && ['t1', 't2', 't3', 'final'].every((campo) => Object.prototype.hasOwnProperty.call(c.grades, campo))
      )
    ),
  });
  sleep(1);
}
