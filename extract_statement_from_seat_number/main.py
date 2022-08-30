import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import json

seats = [121432, 312452, 325562, 235456, ...]

current_dir = pathlib.Path(__file__).parent.absolute()

driver: webdriver.Chrome = webdriver.Chrome()
driver.get('https://rtmnu.digitaluniversity.ac/SearchDuplicateResult.aspx?ID=1091')

captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_CaptchaControll_captchaImage')))

exam_input = Select(driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ExEv_ID'))

# 1 == WINTER 2021
exam_input.select_by_value('1')


seat_no_input = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TxtPrn')
seat_no_input.clear()


input('Complete Captcha Then press submit then press enter here...')

for id in [000000] + seats:
    seat_no_input = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TxtPrn')
    seat_no_input.clear()
    seat_no_input.send_keys(id)
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_btnSearch')))
    submit_button.click()
    table_thing = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_oGridViewExmdetails > tbody > tr:nth-child(2) > td:nth-child(5) > a')))
    table_thing.click()
    required_thing = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'divHTMLPrint')))
    with open(str(current_dir /f'{id}.html'), 'w', encoding="utf-8") as f:
        f.write(required_thing.get_attribute('outerHTML'))


driver.quit()

