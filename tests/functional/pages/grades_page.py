from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class GradesPage(BasePage):
    VIEW = (By.ID, "view-notas")
    TABLE_HEADERS = (By.CSS_SELECTOR, "#view-notas thead th")
    ROWS = (By.CSS_SELECTOR, "#grades-body tr")

    def is_visible(self):
        return self.wait_visible(self.VIEW).is_displayed()

    def headers(self):
        return [header.text for header in self.driver.find_elements(*self.TABLE_HEADERS)]

    def row_count(self):
        self.wait_visible(self.ROWS)
        return len(self.driver.find_elements(*self.ROWS))

    def grades_for(self, course_name):
        for row in self.driver.find_elements(*self.ROWS):
            cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            if cells[0] == course_name:
                return {"t1": cells[2], "t2": cells[3], "t3": cells[4], "final": cells[5]}
        raise AssertionError(f"No se encontró la fila de '{course_name}'.")
