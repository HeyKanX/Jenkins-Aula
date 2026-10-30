Feature: Perfil del estudiante
  Como estudiante
  Quiero consultar mi perfil
  Para confirmar mi información académica

  @tc10
  Scenario: TC-10 - Consulta de perfil desde menú
    Given que abro Aula Nova
    When selecciono "Mi perfil" en el menú
    Then se muestra la vista Mi perfil
    And el perfil muestra nombre "María García López", código "202310458", correo "maria.garcia@universidad.edu" y programa "Ingeniería de Sistemas"

  @tc11
  Scenario: TC-11 - Acceso a perfil desde encabezado
    Given que abro Aula Nova
    When selecciono el perfil desde el encabezado
    Then se muestra la vista Mi perfil
    And la URL termina en "#perfil"
    And el breadcrumb de perfil muestra "Mi perfil"
