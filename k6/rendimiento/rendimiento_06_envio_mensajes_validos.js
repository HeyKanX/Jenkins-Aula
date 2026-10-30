// P6 (consigna): POST /api/messages valido devuelve HTTP 201; medir latencia y errores.
// La API conserva mensajes en memoria: reiniciar servidor entre ejecuciones comparables.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost o 127.0.0.1.');
}
export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const mensaje = {
    courseId: 'calc-201',
    subject: `Consulta rendimiento VU${__VU} I${__ITER}`,
    body: 'Solicito una orientacion sobre la practica de calculo diferencial.',
  };
  const respuesta = http.post(`${BASE_URL}/api/messages`, JSON.stringify(mensaje), {
    headers: { 'Content-Type': 'application/json' },
    tags: { caso: 'P6', accion: 'envio' },
  });
  let datos;
  try { datos = respuesta.json(); } catch (_) { datos = null; }
  check(respuesta, {
    'P6: envio valido devuelve HTTP 201': (r) => r.status === 201,
    'P6: respuesta confirma mensaje y curso': () => Boolean(datos && datos.message && datos.message.courseId === mensaje.courseId),
  });
  sleep(2); // Limita el crecimiento de mensajes en memoria.
}
