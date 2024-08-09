import time
import unittest
from difflib import SequenceMatcher
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class TestCheckAmazonAddToCart(unittest.TestCase):
    def test_check_amazon_add_to_cart(self):

        # Oncelikle genel tarayici tanimlamalarini yapip, bildirimleri kapatıp  diğer ayarlarimizi yapalim.
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        # Sonra driver i Amazon anasayfasina gonderelim.
        self.driver.get('http://www.amazon.com.tr')

        # Kısa bir bekleme ekliyoruz.
        self.driver.implicitly_wait(10)

        # Burada karsimiza cikan cookie yi gecmek icin "Kabul" butonun locatini alip, tikliyoruz.
        COOKIE_ACCEPT = (By.ID, "sp-cc-accept")
        self.driver.find_element(*COOKIE_ACCEPT).click()

        # Simdi ise Amazon anasayfasinda olup olmadigimizi assert ediyoruz, acilmamasi durumunda mesajimizi ekliyoruz.
        self.assertEqual('https://www.amazon.com.tr/', self.driver.current_url, "Amazon Anasayfa Açılmadı")

        # Anasayfamizin acildigini dogruladik, bu adimda arama yapabilmek icin arama kutusunun locatini alalim.
        SEARCH_TEXTBOX = (By.ID, "twotabsearchtextbox")

        # Simdi arama kutusuna metin girebilmek icin uzerine tiklayalim.
        self.driver.find_element(*SEARCH_TEXTBOX).click()

        # Bu adimda arama kutusuna "samsung" metnini giriyoruz ve "Enter" tusuna basiyoruz.
        # " Enter" tusuna basabilmek icin, class seviyesine "Keys" class ını import ediyoruz ve kodumuza ekliyoruz.
        textbox_element = self.driver.find_element(*SEARCH_TEXTBOX)
        textbox_element.send_keys("samsung")
        textbox_element.send_keys(Keys.ENTER)

        # Simdi de acilan sayfadaki sonucların "samsung" aramasına ait oldugunu onaylayalım.
        # Bunun farklı yontemleri var fakat ben burada URL in "samsung" icermesi uzerinden assert edecegim.
        self.assertIn("samsung", self.driver.current_url, "URL 'samsung' içermiyor.")

        # Task da 2. sayfaya gitmemiz istendiginden, sayfa altında bulunan "2" butonunun locatini alıp tıklıyoruz.
        time.sleep(2)
        SECOND_PAGE_BUTTON = (By.XPATH, "(//*[@class='s-pagination-item s-pagination-button'])[1]")
        element = self.driver.find_element(*SECOND_PAGE_BUTTON)
        # Burada aldigimiz locate sayfanın altında oldugundan, JavaScript yardimiyla sayfayı kaydiriyoruz.
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

        # Simdi de bu sayfanin gosterimde olup olmadıgını dogrulayalım.
        # Bu islemi sayfanın sol ust kosesinde bulunan ve 2. sayfaya ait olan
        # "30.000 üzeri sonuç arasından 49-96 arası gösteriliyor. Aranan ürün:" yazısını assert ederek yapacagım.
        # Tarayıcıda bir sayfada 48 urun gosteriliyor, bu baglamda 2. sayfa 49+ urunleri gosterecek.
        # Guven Hoca'nın dersinde iken benzer dogrulamayı assertIn ile yapmıştık, ben burada assertTrue kullanacagım.
        time.sleep(2)
        SECOND_PAGE_TITLE = (By.XPATH, "//*[text()= '30.000 üzeri sonuç arasından 49-96 arası gösteriliyor. Aranan ürün:']")
        text = self.driver.find_element(*SECOND_PAGE_TITLE).text
        self.assertIn(" 49-96 arası", text)

        # Simdi taskımızda bizden istendigi uzere 5. satır ve 1. sutundaki elementi locate edip tiklayalaim.

        FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
        product_element = self.driver.find_element(*FIFTH_ROW_FIRST_COLOUMN)
        product_name = product_element.get_attribute("alt").lower().strip()  # Küçük harf ve boşluk kırpma işlemi
        product_element.click()

        self.driver.implicitly_wait(20)  # 20 saniyelik implicit wait
        product_title_element = self.driver.find_element(By.ID, "productTitle")

        opened_product_name = product_title_element.text.lower().strip()  # Küçük harf ve boşluk kırpma işlemi

        # Benzerlik oranını hesapla
        similarity_ratio = SequenceMatcher(None, product_name, opened_product_name).ratio()

        # 4. Karşılaştırma yapmak (Benzerlik oranı %80'in üzerinde mi?)
        threshold = 0.8
        assert similarity_ratio >= threshold, f"Tıklanan ürün ({product_name}) ile açılan ürün ({opened_product_name}) yeterince benzer değil (benzerlik oranı: {similarity_ratio:.2f})."



















        # FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
        # product_element = self.driver.find_element(*FIFTH_ROW_FIRST_COLOUMN)
        # product_name = product_element.get_attribute("alt")
        # product_element.click()
        #
        # self.driver.implicitly_wait(20)  # 10 saniyelik implicit wait
        # product_title_element = self.driver.find_element(By.ID, "productTitle")
        #
        # opened_product_name = product_title_element.text.strip()
        #
        # # 4. Karşılaştırma yapmak
        # assert product_name in opened_product_name, f"Tıklanan ürün ({product_name}) ile açılan ürün ({opened_product_name}) eşleşmiyor."



        # FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
        # product_element = self.driver.find_element(*FIFTH_ROW_FIRST_COLOUMN)
        # product_name = product_element.get_attribute("alt")
        #
        # # 2. Ürüne tıklamak
        # product_element.click()
        #
        # # 3. Yeni sayfada ürün metnini almak (Örneğin, ürün başlığı)
        # # Bekleme kullanarak sayfanın yüklenmesini sağlıyoruz
        # time.sleep(2)
        # product_title_element = self.driver.find_element(By.ID, "productTitle")
        # opened_product_name = product_title_element.text.strip()

       # self.assertEqual(product_name, opened_product_name, "Ürün adları eşleşmiyor.")





        # time.sleep(2)
        # FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
        # element = self.driver.find_element(*FIFTH_ROW_FIRST_COLOUMN)
        # self.driver.execute_script("arguments[0].scrollIntoView();", element)
        # element.click()





        #



        # CATEGORY_ERKEK = (By.LINK_TEXT, "ERKEK")
        # erkek = self.driver.find_element(*CATEGORY_ERKEK)
        # hover = ActionChains(self.driver).move_to_element(erkek)
        # hover.perform()
        # CATEGORY_KAZAK = (By.LINK_TEXT, "Kazak")
        # self.driver.find_element(*CATEGORY_KAZAK).click()
        # KAZAK_BREADCRUMB = (By.LINK_TEXT, "Erkek Kazak")
        # kazak = self.driver.find_element(*KAZAK_BREADCRUMB).text
        # self.assertIn('Kazak', kazak, 'Kazak kategorisinde değilsin.')
        # QUICKFILTER_NEW = (By.CLASS_NAME, 'quick-filters__item--newest')
        # self.driver.find_element(*QUICKFILTER_NEW).click()
        # PROCUCT_IMAGE = (By.CLASS_NAME, 'product-image__image')
        # self.driver.find_element(*PROCUCT_IMAGE).click()
        # BEDEN_SECENEKLERI = (By.CSS_SELECTOR, 'a:not(.disabledNotSelected)[data-tracking-label="BedenSecenekleri"]')
        # self.driver.find_element(*BEDEN_SECENEKLERI).click()
        # ADD_TO_CART = (By.ID, 'pd_add_to_cart')
        # self.driver.find_element(*ADD_TO_CART).click()
        # CART_COUNT = (By.CLASS_NAME, 'badge-circle')
        # self.assertEqual('1', self.driver.find_element(*CART_COUNT).text,
        #                  "Sepete eksik veya hiç ürün eklenmedi")
        # self.driver.find_element(*CART_COUNT).click()
        # self.assertIn('sepetim', self.driver.current_url, "Sepet sayfasında değilsin.")
        # MAIN_LOGO = (By.CLASS_NAME, 'main-header-logo')
        # self.driver.find_element(*MAIN_LOGO).click()
        # self.driver.quit()
        #