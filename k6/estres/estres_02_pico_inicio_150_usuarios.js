import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  stages: [
    { duration: '10s', target: 10 },   
    { duration: '20s', target: 10 },   
    { duration: '2s', target: 1000 },  
    { duration: '30s', target: 1000 }, 
    { duration: '2s', target: 10 },   
    { duration: '30s', target: 10 },   
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate==1'],
  },
};

export default function () {
  const responses = http.batch([
    ['GET', `${BASE_URL}/`, null, { tags: { ruta: 'inicio' } }],
    ['GET', `${BASE_URL}/api/student`, null, { tags: { ruta: 'perfil' } }],
    ['GET', `${BASE_URL}/api/courses`, null, { tags: { ruta: 'cursos' } }],
    ['GET', `${BASE_URL}/api/messages`, null, { tags: { ruta: 'mensajes' } }],
  ]);

  for (const response of responses) {
    check(response, {
      'respuesta HTTP 200': (r) => r.status === 200,
    });
  }

  sleep(0.1);
}