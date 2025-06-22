from pywinauto import Application
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import os
from settings import *

def initBrowser(headless = True, local_profile = CHROME_LOCAL_PROFILE, local_profile_path = CHROME_LOCAL_PROFILE_PATH):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299")  # Set user agent
        # options.add_argument("window-size=1024,768")  # Set virtual screen size
    # options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=1')
    if local_profile and os.path.exists(local_profile_path) and os.path.exists(os.path.join(local_profile_path, local_profile)):
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument("user-data-dir=" + local_profile_path)
        options.add_argument('--profile-directory=' + local_profile)
    elif local_profile != CHROME_LOCAL_PROFILE or local_profile_path != CHROME_LOCAL_PROFILE_PATH:
        print(f"Указанный профиль не найден, использован профиль по умолчанию")
    return webdriver.Chrome(service=service, options=options)

def wait_server(driver, timeout = 1, timeout_max = 30):
    while timeout_max > 0:
        try:
            time.sleep(timeout)
            driver.find_element(By.XPATH, "//div[@id='init_loading']")
            timeout_max -= 1
        except (AttributeError, NoSuchElementException, StaleElementReferenceException):
            break

def authenticate(url):
    el_path = "//div[@id='AreaBlock']" #"//span[@class='header_username' and text()='Arabezar']"
    driver = initBrowser()
    driver.get(url)
    wait_server(driver)
    try:
        driver.find_element(By.XPATH, el_path)
    except (AttributeError, NoSuchElementException, StaleElementReferenceException):
        driver.quit()
        driver = initBrowser(False)
        driver.get(url)
        wait_server(driver)
        while True:
            try:
                driver.find_element(By.XPATH, el_path)
                driver.quit()
                break
            except (AttributeError, NoSuchElementException, StaleElementReferenceException):
                print(f'   Необходимо залогиниться')
                time.sleep(3)
        driver = initBrowser()
        driver.get(url)
        wait_server(driver)
    return driver

def find_address_field_url(win):
    edit_ctrls = win.descendants(control_type="Edit")
    for ctrl in edit_ctrls:
        if 'text_block' in dir(ctrl):
            text = ctrl.text_block()
            if text == "Поле адреса" or \
               text.endswith(" или введите адрес"):
                return ctrl.get_value()

if __name__ == '__main__':
    app = Application(backend='uia')
    try:
        app.connect(title_re=r"Игра #[\d]* - Minesweeper Online")
    except:
        print("Откройте страницу игры перед запуском программы")
        exit(255)

    win = app.window(title_re=r"Игра #[\d]* - Minesweeper Online")
    url = find_address_field_url(win)
    if not url:
        print("Не получилось найти игру, сообщите, пожалуйста, разработчику версию браузера")
        exit(254)

    driver = authenticate(url)
    # driver = initBrowser(False)
    # driver.get(url)

    mines_100_found = driver.find_element(By.XPATH, "//div[@id='top_area_mines_100']").get_attribute('class')
    mines_10_found = driver.find_element(By.XPATH, "//div[@id='top_area_mines_10']").get_attribute('class')
    mines_1_found = driver.find_element(By.XPATH, "//div[@id='top_area_mines_1']").get_attribute('class')
    if not (mines_100_found and mines_10_found and mines_1_found):
        print("Не удалось найти элементы с количеством мин")
        exit(253)

    mines_100_num = re.search(r'hd?d_top-area-num([\d])', mines_100_found)
    mines_10_num = re.search(r'hd?d_top-area-num([\d])', mines_10_found)
    mines_1_num = re.search(r'hd?d_top-area-num([\d])', mines_1_found)
    if not (mines_100_num and mines_10_num and mines_1_num):
        print("Не удалось найти количество мин в элементах")
        exit(252)

    mines_100 = mines_100_num.group(1)
    mines_10 = mines_10_num.group(1)
    mines_1 = mines_1_num.group(1)

    mines_100 = mines_100 if mines_100 else '0'
    mines_10 = mines_10 if mines_10 else '0'
    mines_1 = mines_1 if mines_1 else '0'

    mines_total = int(mines_100) * 100 + \
                  int(mines_10) * 10 + \
                  int(mines_1)
    area = driver.find_element(By.XPATH, "//div[@id='AreaBlock']")

    not_hit_count = len(area.find_elements(By.XPATH, "//div[contains(@class, 'd_closed')]")) # 'hd_closed')]"))
    mines_count = len(area.find_elements(By.XPATH, "//div[contains(@class, 'd_flag')]")) # 'hd_closed hd_flag')]"))
    mines_opened = len(area.find_elements(By.XPATH, "//div[contains(@class, 'd_type10')]")) #'hd_opened hd_type10')]"))
    # for cell in area.find_elements(By.TAG_NAME, 'div'):
        # if cell.get_attribute('class')

    if mines_opened:
        print(f"Количество ненажатых клеток: {not_hit_count}, из них мин: {mines_count}, всего неоткрытых мин: {mines_total}, открытых мин: {mines_opened}")
    else:
        print(f"Количество ненажатых клеток: {not_hit_count}, из них мин: {mines_count}, всего мин: {mines_total}, осталось открыть: {not_hit_count - mines_count - mines_total}")
