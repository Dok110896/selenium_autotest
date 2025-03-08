from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modul_5.login_page import LoginPage
from modul_5.inventory_page import InventoryPage
from modul_5.basket_page import BasketPage
from modul_5.customer_page import CustomerPage
from modul_5.order_page import OrderPage


class Test1:
    """
    This class
    """
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def validate_url(self, expected_url):
        """
        Checks if the
        :param expected_url:
        :return:
        """
        assert self.driver.current_url == expected_url, 'Адрес страницы не совпадает'

    def test_authorization(self):
        """
        :return:
        """
        self.driver.get('https://www.saucedemo.com')
        login = LoginPage(self.driver)
        login.authorization('standard_user', 'secret_sauce')
        self.validate_url('https://www.saucedemo.com/inventory.html')
        print('Проверили url авторизованной страницы')

        inventory = InventoryPage(self.driver)
        inventory.select_product(self.driver)
        inventory.save_product_price(self.driver)
        inventory.add_to_cart(self.driver)
        inventory.check_basket_count(self.driver)

        basket = BasketPage(self.driver)
        self.validate_url('https://www.saucedemo.com/cart.html')
        basket.check_list_position(1)
        basket.check_quantity('1')
        basket.submit_basket()

        customer = CustomerPage(self.driver)
        self.validate_url('https://www.saucedemo.com/checkout-step-one.html')

        customer.send_name()
        customer.send_lastname()
        customer.send_postal_code()
        customer.submit_continue()

        order = OrderPage(self.driver)
        self.validate_url('https://www.saucedemo.com/checkout-step-two.html')
        order.order_list(self.driver)
        order.count_position_order()
        order.order_check_name()
        order.order_check_price()
        order.submit_checkout()

        self.validate_url('https://www.saucedemo.com/checkout-complete.html')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'complete-header')))
        print('Тест пройден успешно!')
        self.driver.close()


test = Test1()
test.test_authorization()
