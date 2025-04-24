import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager


# Инициализация драйвера и открытие сайта
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install())
)
driver.get("https://www.chitai-gorod.ru/")

try:
    # CSS-селектор кнопки входа
    btn_login = ".header-controls__icon"
    button_login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, btn_login))
    )
    button_login.click()

    # Ожидание появления поля ввода номера телефона
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.ui-input-phone__input")
        )
    )

    # Ввод номера телефона
    phone_number = input("Введите номер телефона: +7 9 ")
    phone_input.send_keys(phone_number)
    print(f"Номер телефона '{phone_number}' успешно введен.")

    # Нажатие на кнопку отправки номера телефона
    btn_content = ".auth-modal-content__button"
    button_content = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, btn_content))
    )
    button_content.click()

    try:
        print("Ожидаю появление поля для ввода кода...")

        # Ожидание появления поля для ввода кода
        code_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "otp"))
        )
        print("Поле для ввода кода найдено.")

        # Ввод кода из SMS
        code_number = input("Введите код из SMS: ").strip()
        if code_number:
            code_input.send_keys(code_number)
            print(f"Код '{code_number}' успешно введен.")

        # Ожидание и нажатие следующего элемента после ввода кода
        btn_login_1 = ".header-controls__icon"
        button_login_1 = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, btn_login_1))
        )
        button_login_1.click()

        # Нажатие кнопки профиля
        button_profile = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "profile-page__sub-title"))
        )
        button_profile.click()
        print("Кнопка профиля успешно найдена и нажата.")

        # Проверка загрузки страницы профиля
        title_profile = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".app-input__wrapper"))
        )
        print("Страница профиля успешно загружена.")

        # Ввод отчества
        middle_name_input_text = input("Введите отчество: ").strip()
        input_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#__layout > div > div.app-wrapper__content "
                    "> div.profile-page-container "
                    "> div.personal-data.profile-page-container__content "
                    "> form > div:nth-child(2) > div:nth-child(1) > div > label > input[type=text]",
                )
            )
        )
        input_field.clear()
        input_field.send_keys(middle_name_input_text)
        print(f"Текст '{middle_name_input_text}' успешно введен в элемент.")

        # Ввод нового имени
        new_name = input("Введите новое имя: ").strip()
        name_input_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#__layout > div > div.app-wrapper__content "
                    "> div.profile-page-container "
                    "> div.personal-data.profile-page-container__content "
                    "> form > div:nth-child(1) > div:nth-child(2) > div > label > input[type=text]",
                )
            )
        )
        name_input_field.clear()
        name_input_field.send_keys(new_name)
        print(f"Новое имя '{new_name}' успешно введено в элемент.")

        # Проверка ввода
        entered_value = name_input_field.get_attribute("value")
        if entered_value == new_name:
            print(f"Новое имя '{new_name}' успешно подтверждено.")
        else:
            print(f"Ошибка: в поле отображается '{entered_value}', ожидалось '{new_name}'")

        # Одобрение на получение рассылок
        content = (
            "#__layout > div > div.app-wrapper__content > div.profile-page-container "
            "> div.personal-data.profile-page-container__content > form > div:nth-child(3) "
            "> div.item-data > label > span > span.chg-app-checkbox__control > svg"
        )
        button_content = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, content))
        )
        button_content.click()

        # Нажатие на кнопку сохранения
        save_button_selector = (
            "#__layout > div > div.app-wrapper__content "
            "> div.profile-page-container "
            "> div.personal-data.profile-page-container__content "
            "> form > section > div > button > div > div"
        )
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, save_button_selector))
        )
        if save_button.is_displayed() and save_button.is_enabled():
            save_button.click()
            print("Кнопка сохранения успешно найдена и нажата.")
        else:
            print("Кнопка сохранения недоступна для клика.")

    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except TimeoutException:
        print("Ошибка: не удалось найти поле для ввода имени")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при вводе нового имени: {e}")

except Exception as e:
    print(f"Общая ошибка: {e}", file=sys.stderr)

finally:
    if driver:
        driver.quit()
        print("Браузер закрыт.")