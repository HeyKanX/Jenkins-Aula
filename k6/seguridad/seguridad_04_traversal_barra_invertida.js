import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected403 = http.expectedStatuses(403);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/%2e%2e%5cbackend%5cserver.js`, { responseCallback: expected403 });
  check(response, { 'bloquea traversal con barra invertida': (r) => r.status === 403 });
}
