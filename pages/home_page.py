from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class HomePage(BasePage):

    SEARCH_TEXTBOX = (By.ID, "twotabsearchtextbox")
    COOKIE_ACCEPT = (By.ID, "sp-cc-accept")
    MAIN_LOGO = (By.ID, "nav-logo-sprites")
    def click_cookie(self):
        self.click_element(*self.COOKIE_ACCEPT)

    def search_for_product(self, product_name):
        search_box = self.find(*self.SEARCH_TEXTBOX)
        search_box.click()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.ENTER)

    def go_to_homepage(self):
        self.click_element(*self.MAIN_LOGO)