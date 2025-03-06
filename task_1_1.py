import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

catalog_name = {
    1: "Sauce Labs Backpack",
    2: "Sauce Labs Bike Light",
    3: "Sauce Labs Bolt T-Shirt",
    4: "Sauce Labs Fleece Jacket",
    5: "Sauce Labs Onesie",
    6: "Test.allTheThings() T-Shirt (Red)"}

print("Приветствуем тебя в нашем интернет магазине")
print("Выбери один из следующих товаров и укажи его номер:\n",
      f"1) {catalog_name.get(1)}\n",
      f"2) {catalog_name.get(2)}\n",
      f"3) {catalog_name.get(3)}\n",
      f"4) {catalog_name.get(4)}\n",
      f"5) {catalog_name.get(5)}\n",
      f"6) {catalog_name.get(6)}")
product = int(input())
if product >= 1 and product <= 6:

    print('Открыли сайт')
    driver.get('https://www.saucedemo.com/')

    print('Выполнили авторизацию')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-name'))).send_keys('standard_user')
    driver.find_element(By.CSS_SELECTOR, '[value="standard_user"]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys('secret_sauce')
    driver.find_element(By.CSS_SELECTOR, '[value="secret_sauce"]')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="login-button"]'))).click()

    print('Проверили url авторизованной страницы')
    assert driver.current_url == 'https://www.saucedemo.com/inventory.html', 'Адрес страницы не совпадает'

    print(f'Выбрали товар №{product}')
    # Сохраняем название товара
    position = driver.find_elements(By.XPATH, "//div[@class='inventory_item_name ']")[product - 1].text
    assert position == catalog_name.get(product), 'Название товара не соответствует'

    # Сохраняем цену товара
    cost_price = driver.find_elements(By.XPATH, '(//div[@class="inventory_item_price"])')[product - 1].text
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'(//button[@name])[{product}]'))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@name, 'remove')]")))

    print('Проверяем добавление в корзину')
    basket_count = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge').text
    assert basket_count == '1', 'В корзине больше 1 товара'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'shopping_cart_container'))).click()

    print('Проверяем количество, наименование и цену товара')
    assert driver.current_url == 'https://www.saucedemo.com/cart.html'
    # Проверяем, что количество == 1
    count = driver.find_elements(By.XPATH, "//div[@class='cart_item']")
    assert len(count) == 1, 'Добавлено больше 1 товара'

    basket_quantity = driver.find_element(By.XPATH, "//div[@class='cart_quantity']").text
    assert basket_quantity == '1', "Позиция добавлена больше 1 раза в корзину"

    # Проверяем соответствие наименования товара по каталогу
    basket_name = driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
    assert basket_name == position, 'Наименование номенклатуры отличается от каталога'

    # Проверяем соответствие цены по каталогу
    basket_cost = driver.find_element(By.XPATH, "//div[@class='inventory_item_price']").text
    assert basket_cost == cost_price, 'Цены на товар различаются'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    print('Заполняем данные пользователя для заказа')
    assert driver.current_url == 'https://www.saucedemo.com/checkout-step-one.html'
    fake = Faker("en_US")

    # Заполняем имя
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "first-name"))).send_keys(fake.first_name())
    check_name = driver.find_element(By.ID, 'first-name').get_attribute("value")
    assert check_name != ""

    # Заполняем фамилию
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "last-name"))).send_keys(fake.first_name())
    check_last_name = driver.find_element(By.ID, 'last-name').get_attribute("value")
    assert check_last_name != ""

    # Заполняем почтовый индекс
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "postal-code"))).send_keys(fake.unique.random_int())
    check_postal_code = driver.find_element(By.ID, 'postal-code').get_attribute("value")
    assert check_postal_code != ""
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "continue"))).click()

    print('Проверяем данные заказа')
    assert driver.current_url == 'https://www.saucedemo.com/checkout-step-two.html'

    # Проверяем равенство количеству 1
    order_item = driver.find_elements(By.XPATH, "//div[@data-test='inventory-item']")
    assert len(order_item) == 1, 'В листе заказов больше 1 позиции'

    # Проверяем соответствие количества, наименования и цены
    assert basket_quantity == '1', "Позиция добавлена больше 1 раза в корзину"
    assert basket_name == position, 'Название товара не соответствует'
    assert basket_cost == cost_price, 'Цены на товар различаются'
    # Производим расчет для определения стоимости заказа
    total = driver.find_element(By.CLASS_NAME, 'summary_subtotal_label').text
    total = total.replace("Item total: ", "")
    assert total == cost_price, 'Сумма заказа не совпадает'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "finish"))).click()
    time.sleep(3)

    assert driver.current_url == 'https://www.saucedemo.com/checkout-complete.html'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'complete-header')))
    print('Тест пройден успешно!')
    driver.close()
else:
    driver.close()
    print('Такой позиции в каталоге нет')
