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
        SECOND_PAGE_TITLE = (By.XPATH, "//*[contains(text(), 'sonuç arasından 49-96')]")
        text = self.driver.find_element(*SECOND_PAGE_TITLE).text
        self.assertIn(" 49-96 arası", text)

        # Simdi taskımızda bizden istendigi uzere 5. satır ve 1. sutundaki elementi locate edip tiklayalaim.
        FIFTH_ROW_FIRST_COLOUMN = (By.XPATH, "(//img[@class='s-image'])[21]")
        product_element = self.driver.find_element(*FIFTH_ROW_FIRST_COLOUMN)

        # Elementin locatini aldık fakat gorevde bizden tikalanan urun ile sepete eklenen urunun aynı oldugunun
        # dogrulanmasi isteniyor. Bu yuzden urun tıklanmadan once attribute nu alip, kucuk harfe cevirip,
        # bosluklardan temizliyoruz ve sonra tikliyoruz.
        product_name = product_element.get_attribute("alt").lower().strip()
        product_element.click()

        # Bu asamada ise acılan urun sayfasindaki basligi aliyoruz ve acilan urun ismi olarak
        # atiyoruz boylece karsilastirma yapabilecegiz.
        self.driver.implicitly_wait(20)
        product_title_element = self.driver.find_element(By.ID, "productTitle")
        opened_product_name = product_title_element.text.lower().strip()

        # Daha onceki denemelerde hatalar aldım cunku illa ki urun isminde bazı farkliliklar oluyordu.
        # Bu yüzden arastırma yapıp benzerlik oranından yaralanmaya karar verdim. Yani % 80 i benzer ise geciyor.
        similarity_ratio = SequenceMatcher(None, product_name, opened_product_name).ratio()

        # Burada da karsilastirma yapip dogruluyoruz.
        threshold = 0.8
        assert similarity_ratio >= threshold, f"Tıklanan ürün ile açılan ürün  yeterince benzer değil)."

        # Urunu de dogruladiktan sonra sepetimize ekleyelim.
        ADD_TO_CART = (By.ID, "add-to-cart-button")
        self.driver.find_element(*ADD_TO_CART).click()

        # Sonraki adimda sepet sayfasinda oldugumuzun dogrulanmasi isteniyor. Bunun icin once sepete gidelim.
        GO_TO_CART = (By.ID, "sw-gtc")
        self.driver.find_element(*GO_TO_CART).click()

        # Simdi de sepet sayfasinda oldugumuzu dogrulayalim. Bunun icin "Alısverisi Tamamla" butonunun locatini alalım
        # ve gorunur olup olmadigi ile dogrulayalim.
        self.driver.implicitly_wait(5)
        CART_PAGE = self.driver.find_element(By.NAME, "proceedToRetailCheckout")
        assert CART_PAGE.is_displayed(), "Sepetim sayfasinda degilsin."

        # Son adim olarak da anasayfaya donelim ve tarayicidan cikalim.
        MAIN_LOGO = (By.ID, "nav-logo-sprites")
        self.driver.find_element(*MAIN_LOGO).click()
        self.driver.quit()





















