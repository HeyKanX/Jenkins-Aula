import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  noConnectionReuse: true,

  stages: [
    { duration: '5s', target: 10 },
    { duration: '5s', target: 10 },   
    { duration: '10s', target: 200 },
    { duration: '25s', target: 200 },  
    { duration: '5s', target: 10 },
    { duration: '5s', target: 10 },  
    { duration: '3s', target: 0 },
  ],

  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    http_req_connecting: ['p(95)<500'],
    checks: ['rate==1'],
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/api/student`, {
    timeout: '5s',
  });

  check(response, {
    'servidor responde HTTP 200': (r) => r.status === 200,
  });

  sleep(0.1);
}
