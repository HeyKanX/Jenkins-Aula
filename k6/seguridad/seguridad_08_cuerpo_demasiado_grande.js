import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected413 = http.expectedStatuses(413);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const payload = JSON.stringify({ courseId: 'calc-201', subject: 'Carga grande', body: 'A'.repeat(17000) });
  const response = http.post(`${BASE_URL}/api/messages`, payload, {
    headers: { 'Content-Type': 'application/json' },
    responseCallback: expected413,
  });
  check(response, { 'rechaza cuerpo mayor al límite': (r) => r.status === 413 });
}
