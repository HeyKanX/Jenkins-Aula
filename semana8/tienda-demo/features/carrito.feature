Feature: Carrito de compras
  Como usuario de TiendaDemo
  Quiero completar y validar los flujos de compra
  Para comprobar el comportamiento solicitado

  Background:
    Given [carrito] estoy en el catálogo de TiendaDemo

  @TC-01
  Scenario: TC-01 - Agregar un producto al carrito
    When [carrito] agrego "Laptop Pro 15" al carrito
    Then [carrito] veo el producto "Laptop Pro 15" en el carrito

  @TC-02
  Scenario: TC-02 - Agregar varios productos diferentes
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] agrego "Mouse Inalámbrico" al carrito
    Then [carrito] veo los productos "Laptop Pro 15" y "Mouse Inalámbrico" en el carrito

  @TC-03
  Scenario: TC-03 - Agregar dos veces el mismo producto
    When [carrito] agrego "Laptop Pro 15" al carrito dos veces
    Then [carrito] la cantidad de "Laptop Pro 15" es 2

  @TC-04
  Scenario: TC-04 - Actualizar el contador de artículos
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] agrego "Mouse Inalámbrico" al carrito
    Then [carrito] el contador del carrito es 2

  @TC-05
  Scenario: TC-05 - Consultar el producto agregado al carrito
    When [carrito] agrego "Teclado Mecánico" al carrito
    And [carrito] abro el carrito
    Then [carrito] veo el producto "Teclado Mecánico" en el carrito

  @TC-06
  Scenario: TC-06 - Aumentar la cantidad de un producto
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] abro el carrito
    And [carrito] aumento la cantidad de "Laptop Pro 15"
    Then [carrito] la cantidad de "Laptop Pro 15" es 2

  @TC-07
  Scenario: TC-07 - Disminuir la cantidad de un producto
    When [carrito] agrego "Laptop Pro 15" al carrito dos veces
    And [carrito] abro el carrito
    And [carrito] disminuyo la cantidad de "Laptop Pro 15"
    Then [carrito] la cantidad de "Laptop Pro 15" es 1

  @TC-08
  Scenario: TC-08 - Impedir o resolver una cantidad igual a cero
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] abro el carrito
    And [carrito] disminuyo la cantidad de "Laptop Pro 15"
    Then [carrito] el carrito ya no contiene "Laptop Pro 15"

  @TC-09
  Scenario: TC-09 - Ingresar una cantidad negativa
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] abro el carrito
    And [carrito] intento ingresar la cantidad negativa -1
    Then [carrito] la cantidad negativa es rechazada

  @TC-10
  Scenario: TC-10 - Eliminar un producto del carrito
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] abro el carrito
    And [carrito] elimino "Laptop Pro 15" del carrito
    Then [carrito] el carrito ya no contiene "Laptop Pro 15"

  @TC-11
  Scenario: TC-11 - Eliminar el último producto
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] abro el carrito
    And [carrito] elimino "Laptop Pro 15" del carrito
    Then [carrito] se muestra el carrito vacío

  @TC-12
  Scenario: TC-12 - Eliminar un artículo y conservar los demás
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] agrego "Mouse Inalámbrico" al carrito
    And [carrito] abro el carrito
    And [carrito] elimino "Laptop Pro 15" del carrito
    Then [carrito] veo el producto "Mouse Inalámbrico" en el carrito

  @TC-13
  Scenario: TC-13 - Actualizar el subtotal al eliminar un producto
    When [carrito] agrego "Laptop Pro 15" al carrito
    And [carrito] agrego "Mouse Inalámbrico" al carrito
    And [carrito] abro el carrito
    Then [carrito] el subtotal del carrito es S/ 2588.90
    When [carrito] elimino "Laptop Pro 15" del carrito
    Then [carrito] el subtotal del carrito es S/ 89.90
