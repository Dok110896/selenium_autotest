import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestSauceDemoTest():
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.faker = Faker("en_US")
        self.catalog_name = {
            1: "Sauce Labs Backpack",
            2: "Sauce Labs Bike Light",
            3: "Sauce Labs Bolt T-Shirt",
            4: "Sauce Labs Fleece Jacket",
            5: "Sauce Labs Onesie",
            6: "Test.allTheThings() T-Shirt (Red)"
        }

    def test_open_website(self):
        print('Открываем сайт')
        self.driver.get('https://www.saucedemo.com/')

    def test_login(self, username='standard_user', password='secret_sauce'):
        print('Выполняем авторизацию')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-name'))).send_keys(username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="login-button"]'))).click()

    def validate_url(self, expected_url):
        assert self.driver.current_url == expected_url, 'Адрес страницы не совпадает'

    def select_product(self, product_index):
        print(f'Выбираем товар №{product_index}')
        position = self.driver.find_elements(By.XPATH, "//div[@class='inventory_item_name ']")[product_index - 1].text
        cost_price = self.driver.find_elements(By.XPATH, '//div[@class="inventory_item_price"]')[product_index - 1].text
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'(//button[@name])[{product_index}]'))).click()
        return position, cost_price

    def verify_cart(self):
        print('Проверяем, что товар добавлен в корзину')
        basket_count = self.driver.find_element(By.CLASS_NAME, 'shopping_cart_badge').text
        assert basket_count == '1', 'В корзине больше 1 товара'

    def go_to_cart(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'shopping_cart_container'))).click()
        print('Переходим в корзину. Проверяем url и содержимое')
        self.validate_url('https://www.saucedemo.com/cart.html')

    def verify_cart_contents(self, expected_name, expected_price):
        print('Проверяем количество, наименование и цену товара')
        assert len(self.driver.find_elements(By.XPATH, "//div[@class='cart_item']")) == 1, 'Добавлено больше 1 товара'
        basket_quantity = self.driver.find_element(By.XPATH, "//div[@class='cart_quantity']").text
        assert basket_quantity == '1', "Позиция добавлена больше 1 раза в корзину"
        basket_name = self.driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
        assert basket_name == expected_name, 'Наименование номенклатуры отличается от каталога'
        basket_cost = self.driver.find_element(By.XPATH, "//div[@class='inventory_item_price']").text
        assert basket_cost == expected_price, 'Цены на товар различаются'

    def fill_checkout_info(self):
        print('Заполняем данные пользователя для заказа')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "first-name"))).send_keys(self.faker.first_name())
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "last-name"))).send_keys(self.faker.last_name())
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "postal-code"))).send_keys(self.faker.unique.random_int())
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()

    def verify_order_summary(self, expected_price):
        print('Проверка заказа перед завершением покупки')
        self.validate_url('https://www.saucedemo.com/checkout-step-two.html')
        assert len(self.driver.find_elements(By.XPATH, "//div[@data-test='inventory-item']")) == 1, 'В листе заказов больше 1 позиции'
        total = self.driver.find_element(By.CLASS_NAME, 'summary_subtotal_label').text.replace("Item total: ", "")
        assert total == expected_price, 'Сумма заказа не совпадает'

    def finish_order(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        self.validate_url('https://www.saucedemo.com/checkout-complete.html')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'complete-header')))
        print('Тест пройден успешно!')

    def run_test(self):
        print("Приветствуем тебя в нашем интернет магазине")
        print("Выбери один из следующих товаров и укажи его номер:\n",
              f"1) {self.catalog_name.get(1)}\n",
              f"2) {self.catalog_name.get(2)}\n",
              f"3) {self.catalog_name.get(3)}\n",
              f"4) {self.catalog_name.get(4)}\n",
              f"5) {self.catalog_name.get(5)}\n",
              f"6) {self.catalog_name.get(6)}")

        product = int(input())
        if 1 <= product <= 6:
            self.open_website()
            self.login()
            self.validate_url('https://www.saucedemo.com/inventory.html')
            position, cost_price = self.select_product(product)
            self.verify_cart()
            self.go_to_cart()
            self.verify_cart_contents(position, cost_price)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
            time.sleep(3)  # Optionally, consider removing this sleep
            self.fill_checkout_info()
            self.verify_order_summary(cost_price)
            self.finish_order()
            self.driver.quit()
        else:
            self.driver.quit()
            print('Такой позиции в каталоге нет')


if __name__ == "__main__":
    test = TestSauceDemoTest()
    test.run_test()