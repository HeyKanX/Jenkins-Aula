import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const TAMANOS = [15360, 16300, 16384];

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '15s', target: 30 },
    { duration: '30s', target: 30 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate==1'],
  },
};

function crearCuerpo(bytes) {
  const payload = {
    courseId: 'calc-201',
    subject: 'Prueba de cuerpo cercano al limite',
    body: 'Mensaje valido para comprobar estabilidad bajo carga.',
    padding: '',
  };

  const longitudBase = JSON.stringify(payload).length;
  payload.padding = 'x'.repeat(bytes - longitudBase);

  return JSON.stringify(payload);
}

const cuerpos = TAMANOS.map(crearCuerpo);

export default function () {
  const indice = (__VU + __ITER) % cuerpos.length;
  const bytes = TAMANOS[indice];

  const response = http.post(
    `${BASE_URL}/api/messages`,
    cuerpos[indice],
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { cuerpo_bytes: String(bytes) },
    }
  );

  check(response, {
    'cuerpo dentro del limite responde HTTP 201':
      (r) => r.status === 201,
    'respuesta contiene identificador':
      (r) => {
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