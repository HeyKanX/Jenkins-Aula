import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';
const expected404 = http.expectedStatuses(404);

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/api/admin`, { responseCallback: expected404 });
  check(response, { 'API inexistente no queda expuesta': (r) => r.status === 404 });
}
