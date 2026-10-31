import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = { vus: 1, iterations: 1, thresholds: { checks: ['rate==1'] } };

export default function () {
  const response = http.get(`${BASE_URL}/`);
  check(response, {
    'inicio responde 200': (r) => r.status === 200,
    'bloquea iframes': (r) => r.headers['X-Frame-Options'] === 'DENY',
    'evita MIME sniffing': (r) => r.headers['X-Content-Type-Options'] === 'nosniff',
    'incluye política CSP': (r) => r.headers['Content-Security-Policy'].includes("default-src 'self'"),
  });
}
