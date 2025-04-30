from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
image_locator = (By.CSS_SELECTOR, ".col-12.py-2")
image_container = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located(image_locator))
WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#landscape"))
    )
third_image = driver.find_element(By.ID, "award")
src_source = third_image.get_attribute("src")


print(src_source)
driver.quit()