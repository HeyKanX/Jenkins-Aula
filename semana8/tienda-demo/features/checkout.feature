Feature: Validación y compra en checkout
  Como usuario de TiendaDemo
  Quiero completar y validar los flujos de compra
  Para comprobar el comportamiento solicitado

  Background:
    Given [checkout] estoy en el catálogo de TiendaDemo

  @TC-20
  Scenario: TC-20 - Impedir checkout con carrito vacío
    When [checkout] abro el carrito
    Then [checkout] no se ofrece proceder al pago

  @TC-21
  Scenario: TC-21 - Validar checkout vacío
    Given [checkout] tengo un producto en el carrito
    And [checkout] abro el carrito
    And [checkout] procedo al checkout
    When [checkout] confirmo el pago sin completar los datos
    Then [checkout] veo mensajes de error para los campos obligatorios

  @TC-22
  Scenario: TC-22 - Validar nombre obligatorio
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago dejando vacío el campo "nombre"
    Then [checkout] veo el error del campo "nombre"

  @TC-23
  Scenario: TC-23 - Validar apellido obligatorio
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago dejando vacío el campo "apellido"
    Then [checkout] veo el error del campo "apellido"

  @TC-24
  Scenario: TC-24 - Validar correo obligatorio
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago dejando vacío el campo "correo"
    Then [checkout] veo el error del campo "correo"

  @TC-25
  Scenario: TC-25 - Rechazar formato de correo inválido
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago con un correo inválido
    Then [checkout] veo el error del campo "correo"

  @TC-26
  Scenario: TC-26 - Validar teléfono obligatorio
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago dejando vacío el campo "teléfono"
    Then [checkout] veo el error del campo "teléfono"

  @TC-27
  Scenario: TC-27 - Validar dirección obligatoria
    Given [checkout] estoy en checkout con un producto
    When [checkout] confirmo el pago dejando vacío el campo "dirección"
    Then [checkout] veo el error del campo "dirección"

  @TC-28
  Scenario: TC-28 - Completar una compra válida
    Given [checkout] estoy en checkout con un producto
    When [checkout] completo los datos válidos y confirmo la compra
    Then [checkout] veo la pantalla de confirmación

  @TC-29
  Scenario: TC-29 - Completar una compra con varios productos
    Given [checkout] tengo dos productos diferentes en el carrito
    When [checkout] abro el carrito
    Then [checkout] veo los dos productos diferentes en el carrito
    When [checkout] procedo al checkout
    When [checkout] completo los datos válidos y confirmo la compra
    Then [checkout] veo la pantalla de confirmación

  @TC-30
  Scenario: TC-30 - Mostrar confirmación y número de pedido
    Given [checkout] estoy en checkout con un producto
    When [checkout] completo los datos válidos y confirmo la compra
    Then [checkout] veo el número de orden

  @TC-31
  Scenario: TC-31 - Volver al catálogo después de comprar
    Given [checkout] estoy en checkout con un producto
    When [checkout] completo los datos válidos y confirmo la compra
    And [checkout] regreso al catálogo
    Then [checkout] veo el catálogo de productos
