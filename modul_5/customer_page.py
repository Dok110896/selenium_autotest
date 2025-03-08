from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker


class CustomerPage:
    """
    This class
    """
    def __init__(self, driver):
        self.driver = driver
        self.faker = Faker("en_US")

    def send_name(self):
        """
        :return:
        """
        print('Заполняем данные пользователя для заказа')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "first-name"))).send_keys(self.faker.first_name())
        check_name = self.driver.find_element(By.ID, 'first-name').get_attribute("value")
        assert check_name != ""

    def send_lastname(self):
        """
        :return:
        """
        print('Заполняем фамилию')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "last-name"))).send_keys(self.faker.last_name())
        check_last_name = self.driver.find_element(By.ID, 'last-name').get_attribute("value")
        assert check_last_name != ""

    def send_postal_code(self):
        """
        :return:
        """
        print('Заполняем почтовый индекс')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "postal-code"))).send_keys(self.faker.unique.random_int())
        check_postal_code = self.driver.find_element(By.ID, 'postal-code').get_attribute("value")
        assert check_postal_code != ""

    def submit_continue(self):
        """
        :return:
        """
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()
