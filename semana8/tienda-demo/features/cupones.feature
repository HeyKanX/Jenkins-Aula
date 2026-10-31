Feature: Aplicación de cupones
  Como usuario de TiendaDemo
  Quiero completar y validar los flujos de compra
  Para comprobar el comportamiento solicitado

  Background:
    Given [cupones] estoy en el catálogo de TiendaDemo

  @TC-14
  Scenario: TC-14 - Aplicar un cupón válido
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    And [cupones] aplico el cupón "DESCUENTO10"
    Then [cupones] veo el mensaje de cupón aplicado

  @TC-15
  Scenario: TC-15 - Rechazar un cupón inválido
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    And [cupones] aplico el cupón "INVALIDO"
    Then [cupones] veo el mensaje de cupón no válido
    And [cupones] el total es igual al subtotal

  @TC-16
  Scenario: TC-16 - Validar un cupón vacío
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    And [cupones] aplico un cupón vacío
    Then [cupones] veo el mensaje de cupón vacío
    And [cupones] el total es igual al subtotal

  @TC-17
  Scenario: TC-17 - Rechazar el cupón repetido
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    And [cupones] aplico el cupón "DESCUENTO10"
    Then [cupones] el total corresponde a un descuento del 10 por ciento
    When [cupones] vuelvo a aplicar el cupón "DESCUENTO10"
    Then [cupones] veo un aviso de cupón repetido
    And [cupones] el total corresponde a un descuento del 10 por ciento

  @TC-18
  Scenario: TC-18 - Calcular el total con descuento
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    And [cupones] aplico el cupón "DESCUENTO10"
    Then [cupones] el total corresponde a un descuento del 10 por ciento

  @TC-19
  Scenario: TC-19 - Mantener el total sin cupón
    When [cupones] agrego "Laptop Pro 15" al carrito
    And [cupones] abro el carrito
    Then [cupones] el total es igual al subtotal
