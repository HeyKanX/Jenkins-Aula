@messages
Feature: Mensajes del aula virtual
  Como estudiante
  Quiero comunicarme con mis profesores
  Para resolver mis consultas académicas

  @tc12
  Scenario: TC-12 - Bandeja de mensajes inicialmente vacía
    Given que abro Aula Nova
    When selecciono "Mensajes" en el menú
    Then se muestra una bandeja de mensajes vacía

  @tc13
  Scenario: TC-13 - Apertura de redacción desde Inicio
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    Then se abre el diálogo de redacción con Curso, Asunto y Mensaje

  @tc14
  Scenario: TC-14 - Apertura de redacción desde Mensajes
    Given que abro Aula Nova
    When selecciono "Mensajes" en el menú
    And selecciono "Nuevo mensaje"
    Then se abre el diálogo de redacción con Curso, Asunto y Mensaje

  @tc15
  Scenario: TC-15 - Cancelación de mensaje
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And completo un mensaje válido
    And cancelo el mensaje
    Then el diálogo de redacción está cerrado
    And se muestra una bandeja de mensajes vacía

  @tc16
  Scenario: TC-16 - Validación del formulario completamente vacío
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And envío el formulario de mensaje sin completar campos
    Then se muestra el error "Completa el curso, el asunto y el mensaje."
    And el diálogo de redacción permanece abierto

  @tc17
  Scenario: TC-17 - Validación de curso obligatorio
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And completo asunto y mensaje válidos sin seleccionar curso
    And envío el formulario de mensaje
    Then se muestra el error "Completa el curso, el asunto y el mensaje."
    And el diálogo de redacción permanece abierto

  @tc18
  Scenario: TC-18 - Rechazo de asunto menor que 3 caracteres
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And completo el mensaje con curso "calc-201", asunto "Hi" y cuerpo "Mensaje válido de prueba"
    And envío el formulario de mensaje
    Then se muestra un error que contiene "3–100 caracteres"
    And el diálogo de redacción permanece abierto

  @tc19
  Scenario: TC-19 - Rechazo de mensaje menor que 5 caracteres
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And completo el mensaje con curso "calc-201", asunto "Consulta válida" y cuerpo "Hola"
    And envío el formulario de mensaje
    Then se muestra un error que contiene "5–1000 caracteres"
    And el diálogo de redacción permanece abierto

  @tc20
  Scenario: TC-20 - Envío válido y persistencia durante la sesión
    Given que abro Aula Nova
    When selecciono "Escribir a un profesor"
    And completo el mensaje con curso "calc-201", asunto "Consulta de práctica" y cuerpo "¿Podría explicar el ejercicio número tres?"
    And envío el formulario de mensaje
    Then el diálogo de redacción está cerrado
    And se muestra la confirmación "Mensaje enviado correctamente."
    And la bandeja contiene el mensaje "Consulta de práctica" con el texto "¿Podría explicar el ejercicio número tres?" para "Dra. Elena Torres"
    When recargo la página
    Then la bandeja contiene el mensaje "Consulta de práctica" con el texto "¿Podría explicar el ejercicio número tres?" para "Dra. Elena Torres"
