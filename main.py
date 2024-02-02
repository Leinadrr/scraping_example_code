from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time

# Constantes y header que usaremos durante el proyecto #
FILE = "web1.html"
GOOGLE_FORM = "https://forms...com"
URL = "https://webexample.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}

# Configuracion del webdriver de selenium y sus opciones #
chrome_driver_path = "E:/Escritorio/Python projects/chromedriver/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)


# Funciones: get_web() donde guardamos la web a scrappear en local, y read_web() donde la cargamos para utilizarla #
# def get_web():
#     with open("web1.html", "w", encoding="utf-8") as file:
#         file.write(driver.page_source)


def read_web():
    with open(FILE, mode="r", encoding="utf-8") as fp:
        content = fp.read()
    return content

# Carga de la ruta web local dentro de selenium #
html_file = os.getcwd() + "//" + "web1.html"
driver.get("file:///" + html_file)


# Obtención y procesamiento de las 3 listas de datos que conformaran el form de google (address, link, price) #
a = driver.find_element(By.CLASS_NAME, "search-page-list-header")
actions = ActionChains(driver)
actions.move_to_element(a).click().perform()
time.sleep(5)

for _ in range(20):
    actions.send_keys(Keys.SPACE).perform()
    time.sleep(0.5)

prices_list = driver.find_elements(By.CSS_SELECTOR, "[data-test='property-card-price']")
address_list = driver.find_elements(By.CSS_SELECTOR, ".property-card-link")
link_list = driver.find_elements(By.CLASS_NAME, "property-card-link")

final_links = []
for n in link_list:
    g = n.get_attribute("href")
    if g not in final_links:
        final_links.append(g)
    else:
        pass

final_address = []
for n in address_list:
    if "CA" in n.text:
        address = n.text
        final_address.append(address)

final_prices = []
for prices in prices_list:
    strip_price = prices.text.split("+")
    final_prices.append(strip_price[0].strip("/mo"))

# Conectamos con google form e introducimos los datos obtenidos anteriormente #
driver.get(GOOGLE_FORM)


final_answers = [final_address, final_prices, final_links]

# Creamos 2 generadores para que iteren sobre el index de los 3 formularios y las 40 respuestas #
answer_1 = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd")
generator = 0
index = 0
while True:
    answer_1 = driver.find_elements(By.CSS_SELECTOR, "input.whsOnd")
    index = 0
    for n in answer_1:
        n.click()
        time.sleep(0.5)
        n.send_keys(final_answers[index][generator])
        index += 1
        print(generator)
        if index == 3:
            driver.find_element(By.CSS_SELECTOR, "span.NPEfkd").click()
            time.sleep(0.5)
            driver.find_element(By.LINK_TEXT, "Enviar otra respuesta").click()
            generator += 1
    if generator == len(final_links):
        break



