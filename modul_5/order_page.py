import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modul_5.config import catalog_name, catalog_price, product
from modul_5.basket_page import BasketPage


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.basket_page = BasketPage

    @staticmethod
    def order_list(driver):
        """
        :param driver:
        :return:
        """
        # Проверяем равенство количеству 1
        order_item = driver.find_elements(By.XPATH, "//div[@data-test='inventory-item']")
        assert len(order_item) == 1, 'В листе заказов больше 1 позиции'

    def count_position_order(self):
        """
        :return:
        """
        order_item = self.driver.find_element(By.XPATH, "//div[@class='cart_quantity']").text
        assert order_item == '1', "Позиция добавлена больше 1 раза в корзину"
        print('Проверили количество')

    def order_check_name(self):
        """
        :return:
        """
        order_name = self.driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
        assert order_name == catalog_name.get(product), 'Название товара не соответствует'
        print('Проверили название товара')

    def order_check_price(self):
        """
        :return:
        """
        order_price = self.driver.find_element(By.XPATH, "//div[@class='inventory_item_price']").text
        assert catalog_price.get(product) == order_price, 'Цены на товар различаются'
        print('Проверили стоимость')
        return order_price

    def total_order(self):
        """
        :return:
        """
        # Производим расчет для определения стоимости заказа
        total = self.driver.find_element(By.CLASS_NAME, 'summary_subtotal_label').text
        total = total.replace("Item total: ", "")
        assert total == self.order_check_price, 'Сумма заказа не совпадает'

    def submit_checkout(self):
        """
        :return:
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        time.sleep(0.3)
