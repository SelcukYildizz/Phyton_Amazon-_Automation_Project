from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):

    CART_PAGE = (By.NAME, "proceedToRetailCheckout")

    def is_cart_page_displayed(self):
        return self.find(*self.CART_PAGE).is_displayed()