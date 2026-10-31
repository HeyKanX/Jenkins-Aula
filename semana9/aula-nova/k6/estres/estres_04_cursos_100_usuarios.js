import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  scenarios: {
    carga_cursos: {
      executor: 'ramping-vus',
      exec: 'consultarCursos',
      stages: [
        { duration: '5s', target: 10 },
        { duration: '10s', target: 100 },
        { duration: '25s', target: 100 },
        { duration: '5s', target: 0 },
      ],
    },
    control_perfil: {
      executor: 'constant-vus',
      exec: 'consultarPerfil',
      vus: 1,
      duration: '45s',
    },
  },
  thresholds: {
    'http_req_duration{ruta:cursos}': ['p(95)<1000'],
    'http_req_duration{ruta:perfil}': ['p(95)<1000'],
    'http_req_failed{ruta:cursos}': ['rate<0.05'],
    'http_req_failed{ruta:perfil}': ['rate<0.05'],
    checks: ['rate==1'],
  },
};

export function consultarCursos() {
  const response = http.get(`${BASE_URL}/api/courses`, {
    tags: { ruta: 'cursos' },
  });

  check(response, {
    'cursos responde HTTP 200': (r) => r.status === 200,
  });

  sleep(0.1);
}

export function consultarPerfil() {
  const response = http.get(`${BASE_URL}/api/student`, {
    tags: { ruta: 'perfil' },
  });

  check(response, {
    'perfil responde HTTP 200': (r) => r.status === 200,
  });

  sleep(1);
}
