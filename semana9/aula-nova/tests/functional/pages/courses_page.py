from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CoursesPage(BasePage):
    VIEW = (By.ID, "view-cursos")
    COURSE_CARDS = (By.CSS_SELECTOR, "#all-courses .course-tile")
    BREADCRUMB = (By.ID, "breadcrumb-current")

    def is_visible(self):
        return self.wait_visible(self.VIEW).is_displayed()

    def breadcrumb(self):
        return self.driver.find_element(*self.BREADCRUMB).text

    def course_count(self):
        self.wait_visible(self.COURSE_CARDS)
        return len(self.driver.find_elements(*self.COURSE_CARDS))

    def course_details(self, course_name):
        for card in self.driver.find_elements(*self.COURSE_CARDS):
            if card.find_element(By.TAG_NAME, "h2").text == course_name:
                code_and_teacher = card.find_element(By.TAG_NAME, "p").text.split(" · ")
                return {
                    "codigo": code_and_teacher[0],
                    "docente": code_and_teacher[1],
                    "aula": card.find_element(
                        By.XPATH, ".//div[normalize-space(text())='Aula']/strong"
                    ).text,
                    "creditos": card.find_element(
                        By.XPATH, ".//div[normalize-space(text())='Créditos']/strong"
                    ).text,
                }
        raise AssertionError(f"No se encontró el curso '{course_name}'.")
