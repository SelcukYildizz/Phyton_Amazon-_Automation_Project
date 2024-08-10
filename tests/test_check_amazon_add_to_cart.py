import time
from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
from pages.cart_page import CartPage
from pages.category_page import CategoryPage
from pages.home_page import HomePage
from tests.base_test import BaseTest


class TestCheckAmazonAddToCart(BaseTest):

    def test_check_amazon_add_to_cart(self):
        home_page = HomePage(self.driver)
        category_page = CategoryPage(self.driver)
        cart_page = CartPage(self.driver)

        self.assertEqual(self.base_url, home_page.get_current_url(), "Amazon Anasayfa Açılmadı")
        home_page.click_cookie()
        home_page.search_for_product("samsung")
        self.assertIn("samsung", self.driver.current_url, "URL 'samsung' içermiyor.")

        time.sleep(2)
        category_page.navigate_to_second_page()
        self.assertTrue(category_page.is_second_page_displayed(), "İkinci sayfa açılmadı.")

        time.sleep(2)
        selected_product_name = category_page.select_product()
        product_title_element = self.driver.find_element(By.ID, "productTitle")
        opened_product_name = product_title_element.text.lower().strip()

        similarity_ratio = SequenceMatcher(None, selected_product_name, opened_product_name).ratio()
        threshold = 0.8
        assert similarity_ratio >= threshold, f"Tıklanan ürün ile açılan ürün yeterince benzer değil (%{similarity_ratio*100:.2f})."

        category_page.add_product_to_cart()
        category_page.go_to_cart()

        self.assertTrue(cart_page.is_cart_page_displayed(), "Sepetim sayfasında değilsin.")

        home_page.go_to_homepage()

