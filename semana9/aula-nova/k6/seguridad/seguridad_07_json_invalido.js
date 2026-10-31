import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected400 = http.expectedStatuses(400);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.post(`${BASE_URL}/api/messages`, '{json-inválido', {
    headers: { 'Content-Type': 'application/json' },
    responseCallback: expected400,
  });
  check(response, { 'rechaza JSON inválido': (r) => r.status === 400 });
}
