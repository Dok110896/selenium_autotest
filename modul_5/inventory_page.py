from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from modul_5.config import product, count, catalog_name, catalog_price


class InventoryPage:
    """
    InventoryPage class
    """
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def select_product(driver):
        """
        :param driver:
        :return:
        """
        print(f'Выбрали товар №{product}')
        position = driver.find_element(By.XPATH, f"(//div[@class='inventory_item_name '])[{product}]").text
        assert position == catalog_name.get(product), 'Название товара не соответствует'
        return position

    @staticmethod
    def save_product_price(driver):
        """
        :param driver:
        :return:
        """
        print('Сохраняем цену товара')
        cost_price = driver.find_element(By.XPATH, f'(//div[@class="inventory_item_price"])[{product}]').text
        assert cost_price == catalog_price.get(product), 'Цена товара не соответствует'
        return cost_price

    @staticmethod
    def add_to_cart(driver):
        """
        :param driver:
        :return:
        """
        print('Добавляем товар в корзину')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'(//button[@name])[{product}]'))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@name, 'remove')]")))

    @staticmethod
    def check_basket_count(driver):
        """
        :param driver:
        :return:
        """
        print('Проверяем добавление в корзину')
        basket_count = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge').text
        assert basket_count == count, f'В корзине больше {count} товаров'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'shopping_cart_container'))).click()
