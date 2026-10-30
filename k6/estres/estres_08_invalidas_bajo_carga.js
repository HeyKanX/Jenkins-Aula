import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:3000';

export const options = {
  stages: [
    { duration: '10s', target: 5 },
    { duration: '20s', target: 50 },
    { duration: '1m', target: 50 },
    { duration: '15s', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate==1'],
  },
};

export default function () {
  const caso = (__VU + __ITER) % 4;
  let response;
  let esperado;

  if (caso === 0) {
    // Tráfico normal: consulta de cursos.
    esperado = 200;
    response = http.get(`${BASE_URL}/api/courses`, {
      tags: { tipo: 'consulta_valida' },
      responseCallback: http.expectedStatuses(200),
    });
  } else if (caso === 1) {
    // Tráfico normal: envío válido.
    esperado = 201;
    response = http.post(
      `${BASE_URL}/api/messages`,
      JSON.stringify({
        courseId: 'calc-201',
        subject: 'Consulta valida',
        body: 'Mensaje valido durante la carga mixta.',
      }),
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { tipo: 'envio_valido' },
        responseCallback: http.expectedStatuses(201),
      }
    );
  } else if (caso === 2) {
    // JSON malformado.
    esperado = 400;
    response = http.post(
      `${BASE_URL}/api/messages`,
      '{"courseId":',
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { tipo: 'json_invalido' },
        responseCallback: http.expectedStatuses(400),
      }
    );
  } else {
    // JSON válido con campos inválidos.
    esperado = 400;
    response = http.post(
      `${BASE_URL}/api/messages`,
      JSON.stringify({
        courseId: 'curso-inexistente',
        subject: 'No',
        body: 'Mal',
      }),
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { tipo: 'campos_invalidos' },
        responseCallback: http.expectedStatuses(400),
      }
    );
  }

  check(response, {
    'respuesta coincide con el estado esperado':
      (r) => r.status === esperado,
  });

  sleep(0.2);
}