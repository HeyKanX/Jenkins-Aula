import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected400 = http.expectedStatuses(400);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/%C0%AF`, { responseCallback: expected400 });
  check(response, { 'rechaza codificación de ruta inválida': (r) => r.status === 400 });
}
