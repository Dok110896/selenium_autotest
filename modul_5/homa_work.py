import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


users = ['standard_user', 'locked_out_user', 'problem_user', 'performance_glitch_user', 'error_user', 'visual_user']



# class TestSauceDemoTest:
#     def __init__(self):
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()


def test_open_website():
    print('Открываем сайт')
    driver.get('https://www.saucedemo.com/')


def test_login(username='standard_user', password='secret_sauce'):
    print('Выполняем авторизацию')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-name'))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="login-button"]'))).click()


def locked():
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "error-message-container error"), "Epic sadface: Sorry, this user has been locked out."))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'error-button'))).click()
    # time.sleep(3)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-name'))).clear()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).clear()
    # time.sleep(3)

for user in users:
    test_open_website()
    test_login(username=user, password='secret_sauce')
    if user == user[1]:
        locked()
    time.sleep(3)
    print(f'авторизовали пользователя {user}')
