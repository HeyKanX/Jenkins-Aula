import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const CANTIDAD = Number(__ENV.MENSAJES || 100);

export const options = {
  setupTimeout: '5m',
  stages: [
    { duration: '5s', target: 10 },
    { duration: '10s', target: 100 },
    { duration: '25s', target: 100 },
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    'http_req_duration{fase:consulta}': ['p(95)<1000'],
    'http_req_failed{fase:consulta}': ['rate<0.05'],
    checks: ['rate==1'],
  },
};

export function setup() {
  if (!Number.isInteger(CANTIDAD) || CANTIDAD < 0) {
    throw new Error('MENSAJES debe ser un entero mayor o igual a cero.');
  }

  const inicial = http.get(`${BASE_URL}/api/messages`, {
    tags: { fase: 'preparacion' },
  });

  if (inicial.status !== 200) {
    throw new Error('No se pudo consultar la bandeja inicial.');
  }

  if (inicial.json('messages').length !== 0) {
    throw new Error(
      'La bandeja debe estar vacía. Reinicia el servidor antes de ejecutar.'
    );
  }

  for (let i = 0; i < CANTIDAD; i++) {
    const response = http.post(
      `${BASE_URL}/api/messages`,
      JSON.stringify({
        courseId: 'calc-201',
        subject: `Consulta de prueba ${i + 1}`,
        body: 'Mensaje de prueba para evaluar la consulta de la bandeja.',
      }),
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { fase: 'preparacion' },
      }
    );

    if (response.status !== 201) {
      throw new Error(`No se pudo crear el mensaje ${i + 1}.`);
    }
  }

  return { cantidad: CANTIDAD };
}

export default function (data) {
  const response = http.get(`${BASE_URL}/api/messages`, {
    tags: { fase: 'consulta' },
    responseType: 'text',
  });

  check(response, {
    'bandeja responde HTTP 200': (r) => r.status === 200,
    'bandeja conserva la cantidad esperada': (r) => {
      if (r.status !== 200) return false;

      try {
        return r.json('messages').length === data.cantidad;
      } catch {
        return false;
      }
    },
  });

  sleep(0.1);
}
