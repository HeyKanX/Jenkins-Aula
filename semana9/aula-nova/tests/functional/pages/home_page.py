from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    GREETING = (By.CSS_SELECTOR, "#view-inicio h1")
    HOME_VIEW = (By.ID, "view-inicio")
    SUMMARY_CARDS = (By.CSS_SELECTOR, "#view-inicio .stats-grid .stat-card")
    DASHBOARD_COURSES = (
        By.CSS_SELECTOR,
        "#dashboard-courses .course-row .course-main strong",
    )
    COURSES_LINK = (By.CSS_SELECTOR, "a[data-view='cursos']")
    GRADES_LINK = (By.CSS_SELECTOR, "a[data-view='notas']")
    PROFILE_SHORTCUT = (By.ID, "profile-shortcut")
    OPEN_MESSAGE = (By.CSS_SELECTOR, "#view-inicio [data-open-message]")

    def open_home(self):
        self.open("/")
        self.wait_visible(self.GREETING)

    def greeting_text(self):
        return self.driver.find_element(*self.GREETING).text

    def is_home_visible(self):
        return self.driver.find_element(*self.HOME_VIEW).is_displayed()

    def summary_card_count(self):
        return len(self.driver.find_elements(*self.SUMMARY_CARDS))

    def summary_value(self, label):
        cards = self.driver.find_elements(*self.SUMMARY_CARDS)

        for card in cards:
            card_label = card.find_element(
                By.CSS_SELECTOR, ".stat-label"
            ).text

            if card_label == label:
                value = card.find_element(
                    By.CSS_SELECTOR, ".stat-value"
                ).text
                return "".join(value.split())

        raise AssertionError(f"No se encontró la tarjeta '{label}'.")

    def dashboard_course_names(self):
        self.wait_visible(self.DASHBOARD_COURSES)
        return [
            course.text
            for course in self.driver.find_elements(*self.DASHBOARD_COURSES)
        ]

    def open_courses(self):
        self.wait_clickable(self.COURSES_LINK).click()

    def open_grades(self):
        self.wait_clickable(self.GRADES_LINK).click()

    def open_profile(self):
        self.wait_clickable(self.PROFILE_SHORTCUT).click()

    def open_message_dialog(self):
        self.wait_clickable(self.OPEN_MESSAGE).click()
