import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/api/student`);
  check(response, {
    'API responde 200': (r) => r.status === 200,
    'API no permite cache': (r) => r.headers['Cache-Control'] === 'no-store',
    'API evita MIME sniffing': (r) => r.headers['X-Content-Type-Options'] === 'nosniff',
  });
}
