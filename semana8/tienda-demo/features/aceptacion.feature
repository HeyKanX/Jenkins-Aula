Feature: Pruebas de aceptación de usuario
  Como usuario de TiendaDemo
  Quiero completar y validar los flujos de compra
  Para comprobar el comportamiento solicitado

  Background:
    Given [aceptacion] estoy en el catálogo de TiendaDemo

  @TC-32
  Scenario: TC-32 - Como usuario, agregar un producto
    When [aceptacion] agrego "Laptop Pro 15" al carrito
    Then [aceptacion] el contador del carrito es 1

  @TC-33
  Scenario: TC-33 - Como usuario, consultar el carrito
    When [aceptacion] agrego "Laptop Pro 15" al carrito
    And [aceptacion] abro el carrito
    Then [aceptacion] veo el producto "Laptop Pro 15" en el carrito
    And [aceptacion] el subtotal del carrito es S/ 2499.00

  @TC-34
  Scenario: TC-34 - Como usuario, aplicar un cupón
    When [aceptacion] agrego "Laptop Pro 15" al carrito
    And [aceptacion] abro el carrito
    And [aceptacion] aplico el cupón "DESCUENTO10"
    Then [aceptacion] veo el mensaje de cupón aplicado
    And [aceptacion] el total corresponde a un descuento del 10 por ciento

  @TC-35
  Scenario: TC-35 - Como usuario, completar checkout
    Given [aceptacion] estoy en checkout con un producto
    When [aceptacion] completo los datos válidos y confirmo la compra
    Then [aceptacion] veo la pantalla de confirmación

  @TC-36
  Scenario: TC-36 - Como usuario, detectar datos incompletos
    Given [aceptacion] estoy en checkout con un producto
    When [aceptacion] confirmo el pago dejando vacío el campo "dirección"
    Then [aceptacion] veo el error del campo "dirección"
    And [aceptacion] la compra no se confirma

  @TC-37
  Scenario: TC-37 - Como usuario, confirmar el pedido
    Given [aceptacion] estoy en checkout con un producto
    When [aceptacion] completo los datos válidos y confirmo la compra
    Then [aceptacion] veo la pantalla de confirmación
    And [aceptacion] veo el número de orden

  @TC-38
  Scenario: TC-38 - Como usuario, comprar varios productos
    Given [aceptacion] tengo dos productos diferentes en el carrito
    When [aceptacion] abro el carrito
    Then [aceptacion] veo los dos productos diferentes en el carrito
    When [aceptacion] procedo al checkout
    When [aceptacion] completo los datos válidos y confirmo la compra
    Then [aceptacion] veo la pantalla de confirmación

  @TC-39
  Scenario: TC-39 - Como usuario, intentar comprar con carrito vacío
    When [aceptacion] abro el carrito
    Then [aceptacion] no se ofrece proceder al pago

  @TC-40
  Scenario: TC-40 - Como usuario, verificar el total con descuento
    When [aceptacion] agrego "Laptop Pro 15" al carrito
    And [aceptacion] abro el carrito
    And [aceptacion] aplico el cupón "DESCUENTO10"
    Then [aceptacion] el total corresponde a un descuento del 10 por ciento

  @TC-41
  Scenario: TC-41 - Como usuario, completar la compra con cupón
    When [aceptacion] agrego "Laptop Pro 15" al carrito
    And [aceptacion] abro el carrito
    And [aceptacion] aplico el cupón "DESCUENTO10"
    And [aceptacion] procedo al checkout
    And [aceptacion] completo los datos válidos y confirmo la compra
    Then [aceptacion] veo la pantalla de confirmación
    And [aceptacion] veo el número de orden
