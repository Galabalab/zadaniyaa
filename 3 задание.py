import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class SauceDemoTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.implicitly_wait(10)  
        self.driver.get("https://www.saucedemo.com/")

    def test_login(self):
        username_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()

       
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Products')]"))) # Добавлен xpath для проверки
            print("Авторизация прошла успешно.")
        except TimeoutException:
            print("Авторизация не удалась.")
            self.fail("Авторизация не прошла")
    
    def test_sort_and_prices(self):
        self.test_login() 

        
        sort_select = self.driver.find_element(By.CSS_SELECTOR, "#product_sort_container > select")
        products = self.driver.find_elements(By.CSS_SELECTOR, "div.product-inventory-item")

        
        sort_select.find_element(By.XPATH, "//option[@value='lohi']").click()
        time.sleep(2)  

       
        try:
            product1_price = float(products[0].find_element(By.CLASS_NAME, "inventory_item_price").text.split("$")[1])
            productN_price = float(products[-1].find_element(By.CLASS_NAME, "inventory_item_price").text.split("$")[1])
            self.assertLessEqual(product1_price, productN_price) # Корректная проверка
            print("Сортировка по возрастанию пройдена.")
        except (NoSuchElementException, IndexError):
            print("Ошибка при извлечении цен.")
            self.fail("Ошибка при извлечении цен.")

        
        sort_select.find_element(By.XPATH, "//option[@value='hilo']").click()
        time.sleep(2)

        
        try:
            product1_price = float(products[0].find_element(By.CLASS_NAME, "inventory_item_price").text.split("$")[1])
            productN_price = float(products[-1].find_element(By.CLASS_NAME, "inventory_item_price").text.split("$")[1])
            self.assertGreaterEqual(product1_price, productN_price) 
            print("Сортировка по убыванию пройдена.")
        except (NoSuchElementException, IndexError):
            print("Ошибка при извлечении цен.")
            self.fail("Ошибка при извлечении цен.")


    def test_add_to_cart_and_order(self):
        self.test_login()  

        
        add_button1 = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_button2 = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
        add_button1.click()
        add_button2.click()


        
        cart_link = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Checkout']"))) # Ожидаем загрузку страницы корзины
            print("Переход в корзину прошел успешно")
        except TimeoutException:
            print("Ошибка при переходе в корзину")
            self.fail("Ошибка перехода в корзину")

        #TODO: 
        checkout = self.driver.find_element(By.LINK_TEXT, "Checkout")
        checkout.click()

        print("Заказ создан успешно.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()