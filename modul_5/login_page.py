from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def authorization(self, user_name, password):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-name'))).send_keys(user_name)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="login-button"]'))).click()
