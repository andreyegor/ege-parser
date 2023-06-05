from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import solver
    
def login(driver, key,data):
    surname = driver.find_element(By.ID, "surname")
    name = driver.find_element(By.ID, "name")
    patr = driver.find_element(By.ID, "patr")
    code = driver.find_element(By.ID, "regNum")
    doc = driver.find_element(By.ID, "passNum")
    checkbox = driver.find_element(By.ID, "agreeNum")
    captcha_image = driver.find_element(By.ID, "captcha-img")
    captcha_field = driver.find_element(By.ID, "captcha")
    captcha_btn = driver.find_element(By.ID, "reset-captcha")
    btn = driver.find_element(By.ID, "submit-btn")
    region = driver.find_element(By.XPATH, """//*[@id="region_chosen"]/a/div""")
    
    
    surname.send_keys(data['surname'])
    name.send_keys(data['name'])
    patr.send_keys(data['patronymic'])
    if data['code']:
        code.send_keys(data['code'])
    else:
        doc.send_keys(data['passport'])
    # checkbox.click()
    region.click()
    driver.find_element(By.XPATH, f"""//*[@id="region_chosen"]/div/ul/li[{data['regionid']}]""").click()

    while driver.current_url == key:
        captcha_btn.click()
        path = 'captcha.png'
        captcha_image.screenshot(path)
        line = solver.solve(path)
        if len(line) == 6:
            captcha_field.send_keys(solver.solve(path))
            btn.click()
        else:
            pass

def get_data(driver):
    path = 'out.png'
    tabel = driver.find_element(By.XPATH,f"""//*[@id="table-container"]/table""")
    tabel.screenshot(path)
    text = tabel.get_attribute('innerHTML')
    driver.close()
    return {'tabel': text, 'image': path}

def check(data, silent=False):
    options = Options()
    if silent:
        options.headless = True
    for i in range(10):
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        driver.get("https://checkege.rustest.ru/")
        try:
            if driver.current_url == 'https://checkege.rustest.ru/':
                sleep(1)
                login(driver, 'https://checkege.rustest.ru/', data)
            if driver.current_url == 'https://checkege.rustest.ru/?':
                sleep(1)
                login(driver, 'https://checkege.rustest.ru/?', data)
            break
        except:
            driver.close()
    else:
        return False
            

    if driver.current_url == 'https://checkege.rustest.ru/exams':
        sleep(1)
        return get_data(driver)

