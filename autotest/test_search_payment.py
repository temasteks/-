import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    time.sleep(1)
    try:
        driver.quit()
    except:
        pass


@allure.title("Поиск товара в Яндекс Лавке")
@allure.feature("Пользовательский сценарий")
def test_search_product(driver):
    with allure.step("Открыть Яндекс Лавку"):
        driver.get("https://lavka.yandex.ru/")
        time.sleep(3)

    wait = WebDriverWait(driver, 20)

    with allure.step("Найти поле поиска"):
        try:
            search_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
            )
        except:
            try:
                search_field = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'input')]"))
                )
            except:
                search_field = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Найти')]"))
                )

    with allure.step("Ввести 'молоко' и нажать Enter"):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_field)
        time.sleep(0.5)
        driver.execute_script("arguments[0].focus();", search_field)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", search_field)
        time.sleep(0.5)

        search_field.clear()
        search_field.send_keys("молоко")
        time.sleep(0.5)
        search_field.send_keys(Keys.RETURN)

    with allure.step("Проверить, что поиск выполнен"):
        time.sleep(3)
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # ✅ Удаляем мягкие переносы
        page_text = page_text.replace("\xad", "")
        
        assert "молоко" in page_text, "Товар 'молоко' не найден"