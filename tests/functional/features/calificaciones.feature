Feature: Calificaciones del aula virtual
  Como estudiante
  Quiero consultar mis calificaciones
  Para conocer mi avance académico

  @tc06
  Scenario: TC-06 - Navegación a Calificaciones
    Given que abro Aula Nova
    When selecciono "Calificaciones" en el menú
    Then se muestra la vista Calificaciones
    And la tabla de calificaciones muestra 4 cursos
    And la tabla contiene las columnas "T1", "T2", "T3" y "Final"

  @tc07
  Scenario: TC-07 - Valores de notas de Cálculo diferencial
    Given que abro Aula Nova
    When selecciono "Calificaciones" en el menú
    Then el curso "Cálculo diferencial" tiene T1 "17.0", T2 "16.0", T3 "18.0" y Final "17.2"

  @tc08
  Scenario: TC-08 - Evaluación pendiente sin nota
    Given que abro Aula Nova
    When selecciono "Calificaciones" en el menú
    Then el curso "Metodología de investigación" tiene T3 "—" y Final "15.5"

  @tc09
  Scenario: TC-09 - Acceso a calificaciones mediante progreso
    Given que abro Aula Nova
    When selecciono "Ver mi progreso"
    Then se muestra la vista Calificaciones
    And la URL termina en "#notas"
