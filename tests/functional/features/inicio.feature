Feature: Inicio del aula virtual
  Como estudiante
  Quiero abrir Aula Nova
  Para visualizar mi espacio académico

  @tc01
  Scenario: TC-01 - Carga de la página principal
    Given que abro Aula Nova
    Then se muestra el encabezado "Hola, María"
    And la vista Inicio está visible
    And la URL termina en "#inicio"

  @tc02
  Scenario: TC-02 - Resumen académico
    Given que abro Aula Nova
    Then el resumen académico muestra 3 tarjetas
    And la tarjeta "Cursos matriculados" muestra "04"
    And la tarjeta "Promedio general" muestra "16.4/20"
    And la tarjeta "Próximas evaluaciones" muestra "03"

  @tc03
  Scenario: TC-03 - Listado resumido de cursos
    Given que abro Aula Nova
    Then el listado resumido muestra exactamente estos cursos:
      | curso                        |
      | Cálculo diferencial          |
      | Fundamentos de programación  |
      | Metodología de investigación |
      | Bases de datos               |
