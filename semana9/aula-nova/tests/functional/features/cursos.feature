Feature: Cursos del aula virtual
  Como estudiante
  Quiero consultar mis cursos
  Para conocer mi información académica

  @tc04
  Scenario: TC-04 - Navegación a Mis cursos
    Given que abro Aula Nova
    When selecciono "Mis cursos" en el menú
    Then se muestra la vista Mis cursos
    And la URL termina en "#cursos"
    And el breadcrumb muestra "Mis cursos"

  @tc05
  Scenario: TC-05 - Información detallada de cursos
    Given que abro Aula Nova
    When selecciono "Mis cursos" en el menú
    Then se muestran 4 tarjetas de curso
    And el curso "Cálculo diferencial" muestra código "MAT-201", docente "Dra. Elena Torres", aula "B-204" y créditos "4"
