import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

const latenciaControl = new Trend('latencia_control', true);
const fallosControl = new Rate('fallos_control');

export const options = {
  noConnectionReuse: false,

  scenarios: {
    referencia: {
      executor: 'constant-vus',
      exec: 'consultarPerfil',
      vus: 1,
      duration: '10s',
      gracefulStop: '3s',
      tags: { fase: 'antes' },
    },

    carga: {
      executor: 'ramping-vus',
      exec: 'consultarCursos',
      startTime: '15s',
      stages: [
        { duration: '2s', target: 300 },
        { duration: '20s', target: 300 },
        { duration: '3s', target: 0 },
      ],
      gracefulRampDown: '3s',
      gracefulStop: '3s',
    },

    control_durante: {
      executor: 'constant-vus',
      exec: 'consultarPerfil',
      startTime: '15s',
      vus: 1,
      duration: '25s',
      gracefulStop: '3s',
      tags: { fase: 'durante' },
    },

    recuperacion: {
      executor: 'constant-vus',
      exec: 'consultarPerfil',
      startTime: '45s',
      vus: 1,
      duration: '15s',
      gracefulStop: '3s',
      tags: { fase: 'despues' },
    },
  },

  thresholds: {
    'latencia_control{fase:antes}': ['p(95)<1000'],
    'latencia_control{fase:durante}': ['p(95)<1000'],
    'latencia_control{fase:despues}': ['p(95)<1000'],

    'fallos_control{fase:antes}': ['rate==0'],
    'fallos_control{fase:durante}': ['rate==0'],
    'fallos_control{fase:despues}': ['rate==0'],

    checks: ['rate==1'],
  },
};

export function consultarCursos() {
  const response = http.get(`${BASE_URL}/api/courses`, {
    timeout: '5s',
    tags: { ruta: 'cursos' },
  });

  check(response, {
    'cursos responde HTTP 200': (r) => r.status === 200,
  });

  sleep(0.1);
}

export function consultarPerfil() {
  const response = http.get(`${BASE_URL}/api/student`, {
    timeout: '5s',
    tags: { ruta: 'perfil' },
  });

  const correcto = response.status === 200;

  fallosControl.add(!correcto);

  if (correcto) {
    latenciaControl.add(response.timings.duration);
  }

  check(response, {
    'perfil responde HTTP 200': () => correcto,
  });

  sleep(1);
}
