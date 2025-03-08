from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modul_5 import inventory_page


class BasketPage:

    def __init__(self, driver):
        self.driver = driver
        self.inventory_page = inventory_page

    def check_list_position(self, current_count):
        """
        Проверяем количество позиций в заказе
        :param current_count:
        :return:
        """
        count = self.driver.find_elements(By.XPATH, "//div[@class='cart_item']")
        assert len(count) == current_count, f'Добавлено больше {current_count} товаров'

    def check_quantity(self, quantity):
        """
        Проверяем количество товара
        :param quantity:
        :return:
        """
        basket_quantity = self.driver.find_element(By.XPATH, "//div[@class='cart_quantity']").text
        assert basket_quantity == quantity, f"Позиция добавлена больше {quantity} раз в корзину"
        return basket_quantity

    def check_name(self, product):
        """
        Проверяем соответствие наименования товара по каталогу
        :param product:
        :return:
        """
        basket_name = self.driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
        selected_product_name = self.inventory_page.select_product(self.driver, product)
        assert basket_name == selected_product_name, 'Наименование номенклатуры отличается от каталога'
        
    def check_price(self):
        """
        Проверяем соответствие цены по каталогу
        :return:
        """
        basket_cost = self.driver.find_element(By.XPATH, "//div[@class='inventory_item_price']").text
        check_price_position = self.inventory_page.save_product_price(self.driver, basket_cost)
        assert basket_cost == check_price_position, 'Цены на товар различаются'

    def submit_basket(self):
        """
        Подтверждаем переход на следующую страницу
        :return:
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
