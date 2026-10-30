import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  stages: [
    { duration: '15s', target: 25 },
    { duration: '30s', target: 2000 },
    { duration: '2m', target: 2000 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate==1'],
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/`);
  check(response, { 'inicio responde 200 bajo estrés': (r) => r.status === 200 });
  sleep(0.1);
}
