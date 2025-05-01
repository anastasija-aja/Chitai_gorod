import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests


def get_access_token():
    # Инициализация Firefox WebDriver
    driver = None  # Инициализируем переменную для корректного закрытия в finally
    try:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # Переход на целевую страницу
        driver.get("https://www.chitai-gorod.ru")

        try:
            # Ожидание загрузки страницы
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("Страница успешно загружена")
        except TimeoutException:
            print("Страница не загрузилась в течение отведенного времени")
            raise

        # Получение cookies
        cookies = driver.get_cookies()
        access_token = None

        # Поиск токена в cookies
        for cookie in cookies:
            if cookie['name'] == 'access-token':
                # Убираем первые 9 символов из значения токена
                access_token = cookie['value'][9:]
                break

        if access_token:
            print(f"Access Token без первых 9 символов: {access_token}")
        else:
            print("Токен не найден")
            raise ValueError("Access token не найден в cookies")

        yield access_token  # Возвращаем токен как результат фикстуры

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise  # Перебрасываем исключение дальше для отчетности pytest

    finally:
        # Закрытие браузера в любом случае
        if driver:
            driver.quit()
            print("Браузер успешно закрыт")

# Тест поиска товаров для художников
def test_search_facet_with_token():
    try:
        # Получение токена
        access_token = get_access_token()
        assert access_token, "Access Token не был получен"

        # Новый URL для запроса
        url = "https://web-gate.chitai-gorod.ru/api/v2/products/facet"
        params = {
            'forceFilters[categories]': 110659,
            'forceFilters[onlyNotOnSale]': 1,
            'customerCityId': 213
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Content-Type': 'application/json'
        }

        with requests.Session() as session:
            response = session.get(url, params=params, headers=headers)

            # Логирование полного ответа для отладки
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            # Проверка статуса HTTP-ответа
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
            )

            # Попытка распарсить JSON
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Ответ не является JSON: {response.text}")

            # Проверка наличия товаров в ответе
            assert 'products' in data and data['products'], "Товары не найдены в ответе API"

            # Возвращаем результат
            return {
                'total': data.get('total'),
                'products': data['products']
            }
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None


# Тест перехода на страницу 'Скидки и акции'
def test_page_constructor_with_token():
    try:
        # Получение токена
        access_token = get_access_token()
        assert access_token, "Access Token не был получен"

        # Новый URL для запроса
        url = "https://web-gate.chitai-gorod.ru/api/v1/page-constructor/page"
        params = {
            'project': 1,
            'path': '/articles',
            'include': 'blocks,seo,seo.files,files,pages,productSets'
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Content-Type': 'application/json'
        }

        with requests.Session() as session:
            response = session.get(url, params=params, headers=headers)

            # Логирование полного ответа для отладки
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            # Проверка статуса HTTP-ответа
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
            )

            # Попытка распарсить JSON
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Ответ не является JSON: {response.text}")

            # Проверка наличия необходимых данных в ответе
            assert 'data' in data, "Ключ 'data' не найден в ответе API"
            assert data['data'], "Данные не найдены в ответе API"

            # Возвращаем результат
            return {
                'data': data.get('data'),
                'included': data.get('included', [])
            }
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None


# Тест перехода на страницу 'Доставка и оплата'
def test_tinkoff_percentage_auth():
    try:
        # URL для запроса
        url = "https://web-gate.chitai-gorod.ru/api/v1/tinkoff-percentage-auth"

        # Заголовки запроса
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Content-Type': 'application/json'
        }

        with requests.Session() as session:
            response = session.get(url, headers=headers)

            # Логирование полного ответа для отладки
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            # Проверка статуса HTTP-ответа
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
            )

            print("Тест успешно пройден: получен статус код 200")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Запуск тестов.")
    parser.add_argument(
        "--test",
        choices=["search_facet", "page_constructor", "tinkoff_auth"],
        required=True,
        help="Выберите тест для запуска."
    )
    args = parser.parse_args()

    if args.test == "search_facet":
        result = test_search_facet_with_token()
        if result:
            print(f"Найдено товаров: {result['total']}")
            for product in result['products']:
                print(f"- {product['name']} ({product['price']} руб.)")

    elif args.test == "page_constructor":
        result = test_page_constructor_with_token()
        if result:
            print("Полученные данные:")
            for item in result['data']:
                print(f"- ID: {item.get('id')}, Type: {item.get('type')}")

            print("\nВключенные данные:")
            for included_item in result['included']:
                print(f"- ID: {included_item.get('id')}, Type: {included_item.get('type')}")

    elif args.test == "tinkoff_auth":
        test_tinkoff_percentage_auth()

# Тест поиска товаров 'Планшеты'
def test_product_collections_with_token():
    try:
        # Получение токена
        access_token = get_access_token()
        assert access_token, "Access Token не был получен"

        # Новый URL для запроса
        url = "https://web-gate.chitai-gorod.ru/api/v2/product-collections"
        params = {
            'page': 1,
            'per-page': 48,
            'filters[onlyNonFocus]': 1
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Content-Type': 'application/json'
        }

        with requests.Session() as session:
            response = session.get(url, params=params, headers=headers)

            # Логирование полного ответа для отладки
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            # Проверка статуса HTTP-ответа
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
            )

            # Попытка распарсить JSON
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Ответ не является JSON: {response.text}")

            # Проверка наличия коллекций в ответе
            assert 'collections' in data and data['collections'], "Коллекции не найдены в ответе API"

            # Возвращаем результат
            return {
                'total': data.get('total'),
                'collections': data['collections']
            }
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

# Тест поиска книг по фио автора
def test_new_endpoint_with_token():
    try:
        # Получение токена
        access_token = get_access_token()
        assert access_token, "Access Token не был получен"

        # Новый URL для запроса
        url = "https://web-gate.chitai-gorod.ru/api/v2/new-endpoint"
        params = {
            'page': 1,
            'per-page': 20,
            'filters[isActive]': 1
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
            'Content-Type': 'application/json'
        }

        with requests.Session() as session:
            response = session.get(url, params=params, headers=headers)

            # Логирование полного ответа для отладки
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

            # Проверка статуса HTTP-ответа
            assert response.status_code == 200, (
                f"Ожидался статус 200, но получен {response.status_code}: {response.text}"
            )

            # Попытка распарсить JSON
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Ответ не является JSON: {response.text}")

            # Проверка наличия данных в ответе
            assert 'items' in data and data['items'], "Элементы не найдены в ответе API"

            # Возвращаем результат
            return {
                'total': data.get('total'),
                'items': data['items']
            }
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None