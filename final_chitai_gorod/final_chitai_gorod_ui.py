import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService


@pytest.fixture(scope="module")
def driver():
    # Шаг для инициализации драйвера
    with allure.step("Инициализация WebDriver"):
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        yield driver
        driver.quit()


@allure.feature("Тест входа на сайт по номеру телефона")
@allure.story("Тест входа на сайт по номеру телефона")
def test_positive_login(driver):
    try:

        with allure.step("Открытие страницы входа"):
            driver.get("https://www.chitai-gorod.ru/")


        btn_login = ".header-controls__icon"


        with allure.step(
            f"Ожидание появления и нажатие на кнопку логина "
            f"(селектор: '{btn_login}') в течение 10 секунд"
        ):
            button_login = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, btn_login))
            )
            button_login.click()


        with allure.step("Ожидание появления поля ввода номера телефона"):
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input.ui-input-phone__input")
                )
            )


        with allure.step("Ввод номера телефона"):
            phone_input.send_keys("035484994")
            allure.attach(
                "Номер телефона '055722360' успешно введен.",
                name="Logging",
                attachment_type=allure.attachment_type.TEXT,
            )


        with allure.step("Нажатие на кнопку отправки номера телефона"):
            content_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".auth-modal-content__button")
                )
            )
            content_button.click()
            allure.attach(
                "Нажатие на кнопку выполнено.",
                name="Logging",
                attachment_type=allure.attachment_type.TEXT,
            )


        with allure.step("Ожидание появления поля для ввода кода"):
            code_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "otp"))
            )
            print("Поле для ввода кода найдено.")
            allure.attach(
                "Поле для ввода кода успешно найдено.",
                name="Logging",
                attachment_type=allure.attachment_type.TEXT,
            )


            assert code_input.is_displayed(), "Поле для ввода кода не отображается!"

    except Exception as e:

        with allure.step(f"Ошибка во время выполнения теста: {e}"):
            allure.attach(
                str(e),
                name="Error Log",
                attachment_type=allure.attachment_type.TEXT,
            )
        raise


@allure.feature("Тест поиска книг по имени, отчеству и фамилии автора через строку поиска")
@allure.story("Тест поиска книг по имени, отчеству и фамилии автора через строку поиска")
def test_positive_checkout(driver):
    with allure.step("Открытие страницы входа"):
        driver.get("https://www.chitai-gorod.ru/")


    with allure.step("Ожидание появления строки поиска"):

        search_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-form__input.search-form__input--search"))
        )


    with allure.step("Ввод имени отчества и фамилии автора"):
        search_form.send_keys("Агния Львовна Барто")

    search_form.send_keys(Keys.RETURN)


    with allure.step("Проверка наличия результатов поиска"):
        try:

            search_results = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))

            )


            assert len(search_results) > 0, "Книги не найдены"


            print(f"Найдено книг: {len(search_results)}")

        except TimeoutException:

            assert False, "Результаты поиска не появились"


@allure.feature("Тест добавления товара в корзину")
@allure.story("Тест дДобавления товара в корзину")
def test_add_first_book_to_cart(driver):
    with allure.step("Открытие страницы поиска"):
        driver.get("https://www.chitai-gorod.ru/")
        driver.maximize_window()

    with allure.step("Ожидание появления поля ввода 'Найти'"):
        search_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".search-form__input.search-form__input--search")
            )
        )

    with allure.step("Ввод имени отчества и фамилии автора"):
        search_form.send_keys("Агния Львовна Барто")
        search_form.send_keys(Keys.RETURN)

    first_book_xpath = "//*[@id='__nuxt']/div/div[3]/div[1]/div/div[1]/div/div/div/div/div/div[2]/article[1]/div[5]/button[1]"

    with allure.step("Выбор первой книги из результатов поиска"):
        first_book = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, first_book_xpath))
        )
        first_book.click()



    with allure.step("Добавление выбранной книги в корзину"):
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".product-buttons__main-action")
            )
        )
        add_to_cart_button.click()


@allure.feature("Тест поиска товаров для художников")
@allure.story("Тест поиска товаров для художников")
def test_positive_checkout(driver):

    with allure.step("Открытие страницы входа"):
        driver.get("https://www.chitai-gorod.ru/")
        driver.maximize_window()


        with allure.step("Ожидание кнопки и подтверждение местонахождения"):
            css_selector = ("#tippy-1 > div > div > div > div > "
                           "button.chg-app-button.chg-app-button--primary."
                           "chg-app-button--l.chg-app-button--brand-blue."
                           "chg-app-button--block")
            chg_app_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            chg_app_button.click()

    with allure.step("Ожидание кнопки и переход в каталог"):

        catalog_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#__nuxt > div > header > div > div.header__catalog > button > div > svg"))
        )
        catalog_button.click()

        with allure.step("Выбор категории 'Товары для художников'"):
            categories_level_menu = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     ".categories-level-menu__item-root-icon."
                     "categories-level-menu__item-root-icon--arrow")
                )
            )
            categories_level_menu.click()

            drawing_boards_css = ("body > div.ui-modal.vfm.vfm--fixed.vfm--inset > "
                                  "div.vfm__content.vfm--outline-none.ui-modal__content."
                                  "ui-modal__content--view-sideLeft > div.ui-modal__slot-wrapper > "
                                  "div > div:nth-child(2) > div:nth-child(2) > div.categories-level-menu > a > span")
            drawing_boards_category = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, drawing_boards_css))
            )
            drawing_boards_category.click()

    with allure.step("Проверка наличия результатов поиска"):
        search_results = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card"))
        )

        product_count = len(search_results)
        print(f"Найдено товаров: {product_count}")

        assert product_count > 0, "Товары не найдены"

    with allure.step("Завершение теста"):
        driver.quit()


@allure.feature("Тест удаления товара из корзины")
@allure.story("Тест удаления товара из корзины")
def test_add_first_book_to_cart(driver):
    with allure.step("Открытие страницы поиска"):
        driver.get("https://www.chitai-gorod.ru/")
        driver.maximize_window()


        with allure.step("Ожидание кнопки и подтверждение местонахождения"):
            css_selector = ("#tippy-1 > div > div > div > div > "
                            "button.chg-app-button.chg-app-button--primary."
                            "chg-app-button--l.chg-app-button--brand-blue."
                            "chg-app-button--block")
            chg_app_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            chg_app_button.click()


    with allure.step("Ожидание появления поля ввода 'Найти'"):
        search_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".search-form__input.search-form__input--search")
            )
        )

    with allure.step("Ввод имени отчества и фамилии автора"):
        search_form.send_keys("Агния Львовна Барто")
        search_form.send_keys(Keys.RETURN)

    with allure.step("Ожидание появления кнопки 'Поиск'"):
        search_icon = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".search-form__icon-search")
            )
        )
        search_icon.click()

        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".app-search--opened")))

    first_book_xpath = "//*[@id='__nuxt']/div/div[3]/div[1]/div/div[1]/div/div/div/div/div/div[2]/article[1]/div[5]/button[1]"

    with allure.step("Выбор первой книги из результатов поиска"):
        first_book = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, first_book_xpath))
        )
        first_book.click()


    with allure.step("Добавление выбранной книги в корзину"):
        add_to_cart_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".product-buttons__main-action")
            )
        )
        add_to_cart_button.click()
        WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".app-search--opened")))

        with allure.step("Переход в корзину"):

            cart_controls = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#__nuxt > div > header > div > div.header-controls.header__controls > button:nth-child(4) > span.header-controls__text"))
            )
            cart_controls.click()


        with allure.step("Очистка корзины"):

            clear_cart = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#__nuxt > div > div.app-wrapper__content > div > div > div > div.cart-page__head > div > div.cart-page__delete-many > span"))
            )
            clear_cart.click()

            with allure.step("Переход в корзину для проверки отсутствия содержимого"):
                cart_controls = WebDriverWait(driver, 40).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    "#__nuxt > div > header > div > div.header-controls.header__controls > button:nth-child(4) > span.header-controls__text"))
                )
                cart_controls.click()

                with allure.step("Ожидание появления элемента, который показывает, что корзина очищена"):
                    empty_cart_message = WebDriverWait(driver, 40).until(
                        EC.text_to_be_present_in_element(
                            (By.CSS_SELECTOR,
                             "#__nuxt > div > div.app-wrapper__content > div:nth-child(1) > div > div > section > p.cart-multiple-delete__title"),
                            "Корзина очищена"
                        )
                    )
                    # Проверка, что сообщение действительно появилось
                    assert empty_cart_message, "Сообщение 'Корзина очищена' найдено"

                    print("Проверка прошла успешно: Корзина очищена.")