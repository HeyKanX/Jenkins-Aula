import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  stages: [
    { duration: '5s', target: 2 },
    { duration: '5s', target: 2 },
    { duration: '2s', target: 100 },  
    { duration: '15s', target: 100 },
    { duration: '2s', target: 2 },
    { duration: '5s', target: 2 },
    { duration: '3s', target: 0 },
  ],
  thresholds: {
    'http_req_duration{operacion:envio}': ['p(95)<1000'],
    'http_req_failed{operacion:envio}': ['rate<0.05'],
    checks: ['rate==1'],
  },
};

export default function () {
  const payload = JSON.stringify({
    courseId: 'prog-105',
    subject: `Consulta ${__VU}-${__ITER}`,
    body: 'Mensaje válido para evaluar envíos durante un pico de carga.',
  });

  const response = http.post(`${BASE_URL}/api/messages`, payload, {
    headers: { 'Content-Type': 'application/json' },
    tags: { operacion: 'envio' },
  });

  check(response, {
    'mensaje responde HTTP 201': (r) => r.status === 201,
    'respuesta contiene un identificador': (r) => {
      if (r.status !== 201) return false;

      try {
        return typeof r.json('message.id') === 'string';
      } catch {
        return false;
      }
    },
  });

  sleep(0.5);
}
