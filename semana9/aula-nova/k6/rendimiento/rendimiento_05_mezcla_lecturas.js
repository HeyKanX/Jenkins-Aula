// P5 (consigna): repartir los VUs entre cuatro rutas de lectura, errores < 1% y p95 < 500 ms.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1|aula-nova)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost, 127.0.0.1 o Aula Nova en Docker.');
}
const RUTAS = ['/', '/api/student', '/api/courses', '/api/messages'];
export const options = {
  vus: 12, // Multiplo de 4 para repartir los usuarios en partes iguales.
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

function contenidoValido(respuesta, ruta) {
  if (ruta === '/') return respuesta.body && respuesta.body.includes('Aula Nova');
  let datos;
  try { datos = respuesta.json(); } catch (_) { return false; }
  if (ruta === '/api/student') return Boolean(datos && datos.student && datos.student.email);
  if (ruta === '/api/courses') return Boolean(datos && Array.isArray(datos.courses));
  return Boolean(datos && Array.isArray(datos.messages));
}

export default function () {
  const ruta = RUTAS[(__VU - 1) % RUTAS.length];
  const respuesta = http.get(`${BASE_URL}${ruta}`, { tags: { caso: 'P5', ruta } });
  check(respuesta, {
    'P5: lectura devuelve HTTP 200': (r) => r.status === 200,
    'P5: lectura devuelve contenido valido': (r) => Boolean(contenidoValido(r, ruta)),
  });
  sleep(1);
}
