import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected403 = http.expectedStatuses(403);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/%2e%2e%2fbackend%2fserver.js`, { responseCallback: expected403 });
  check(response, { 'bloquea acceso fuera de la aplicación': (r) => r.status === 403 });
}
