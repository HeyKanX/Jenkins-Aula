// P7 (consigna): consultas GET mientras se envian POST; los mensajes deben aparecer en la bandeja.
// No usar cargas masivas por defecto: la bandeja completa se guarda y transmite en memoria.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:3000').replace(/\/$/, '');
if (!/^http:\/\/(localhost|127\.0\.0\.1|aula-nova)(:\d+)?\/?$/.test(BASE_URL)) {
  throw new Error('Estas pruebas solo pueden ejecutarse contra localhost, 127.0.0.1 o Aula Nova en Docker.');
}
const RUTAS_LECTURA = ['/', '/api/student', '/api/courses', '/api/messages'];
export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

function jsonSeguro(respuesta) {
  try { return respuesta.json(); } catch (_) { return null; }
}

export default function () {
  if (__VU % 5 === 0) { // Aproximadamente 20% de los VUs escriben.
    const mensaje = {
      courseId: 'calc-201',
      subject: `Lectura escritura VU${__VU} I${__ITER}`,
      body: 'Mensaje valido para verificar lectura y escritura simultanea.',
    };
    const envio = http.post(`${BASE_URL}/api/messages`, JSON.stringify(mensaje), {
      headers: { 'Content-Type': 'application/json' },
      tags: { caso: 'P7', accion: 'escritura' },
    });
    const respuestaEnvio = jsonSeguro(envio);
    check(envio, {
      'P7: POST acepta mensaje valido': (r) => r.status === 201,
      'P7: POST devuelve identificador': () => Boolean(respuestaEnvio && respuestaEnvio.message && respuestaEnvio.message.id),
    });
    if (envio.status === 201 && respuestaEnvio && respuestaEnvio.message) {
      const bandeja = http.get(`${BASE_URL}/api/messages`, { tags: { caso: 'P7', accion: 'verificacion_lectura' } });
      const datos = jsonSeguro(bandeja);
      check(bandeja, {
        'P7: GET bandeja responde 200 tras POST': (r) => r.status === 200,
        'P7: mensaje enviado aparece en bandeja': () => Boolean(datos && Array.isArray(datos.messages) &&
          datos.messages.some((m) => m.id === respuestaEnvio.message.id)),
      });
    }
  } else {
    const ruta = RUTAS_LECTURA[(__VU + __ITER) % RUTAS_LECTURA.length];
    const respuesta = http.get(`${BASE_URL}${ruta}`, { tags: { caso: 'P7', accion: 'lectura', ruta } });
    check(respuesta, { 'P7: las lecturas siguen respondiendo HTTP 200': (r) => r.status === 200 });
  }
  sleep(2);
}
