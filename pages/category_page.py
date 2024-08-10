from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class CategoryPage(BasePage):

    SECOND_PAGE_BUTTON = (By.XPATH, "(//*[@class='s-pagination-item s-pagination-button'])[1]")
    SECOND_PAGE_TITLE = (By.XPATH, "//*[contains(text(), 'sonuç arasından 49-96')]")
    FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
    ADD_TO_CART = (By.ID, "add-to-cart-button")
    GO_TO_CART = (By.ID, "sw-gtc")

    def navigate_to_second_page(self):
        second_page_button = self.find(*self.SECOND_PAGE_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", second_page_button)
        second_page_button.click()

    def select_product(self):
        product_element = self.find(*self.FIFTH_ROW_FIRST_COLOUMN)
        product_name = product_element.get_attribute("alt").lower().strip()
        product_element.click()
        return product_name

    def add_product_to_cart(self):
        self.click_element(*self.ADD_TO_CART)

    def go_to_cart(self):
        self.click_element(*self.GO_TO_CART)

    def is_second_page_displayed(self):
        return " 49-96 arası" in self.find(*self.SECOND_PAGE_TITLE).text

