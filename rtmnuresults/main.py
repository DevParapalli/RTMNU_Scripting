import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import json


seats = range(149712, 149788)

current_dir = pathlib.Path(__file__).parent.absolute()

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : r"C:\DevParapalli\Projects\RTMNU_Scripting\rtmnuresults\result_images"}
chrome_options.add_experimental_option('prefs', prefs)


with webdriver.Chrome(chrome_options=chrome_options) as driver:
    driver.get('https://rtmnuresults.org/')
    driver.maximize_window()
    html = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    driver.execute_script("document.body.style.zoom='125 %'")
    faculty_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddlselectfaculty')))
    Select(faculty_select).select_by_value('1')
    exam_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ddlselectexam')))
    # Select(exam_select).select_by_value('10492')
    # Select(exam_select).select_by_value('10557')
    # Select(exam_select).select_by_value('10510')
    # Select(exam_select).select_by_value('10514')
    Select(exam_select).select_by_value('10508')
    roll_no_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtrollno')))
    roll_no_input.send_keys(str(seats[0]))
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'imgbtnviewmarksheet')))
    submit_button.click()
    for seat in seats:
        # go back
        driver.execute_script("window.history.go(-1)")
        roll_no_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtrollno')))
        roll_no_input.clear()
        roll_no_input.send_keys(str(seat))
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'imgbtnviewmarksheet')))
        submit_button.click()
        # wait for the image to load
        image_frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_ifrm')))
        driver.switch_to.frame(image_frame)
        image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
        image.screenshot(str(current_dir / 'result_images' / f'{seat}.png'))
        driver.switch_to.default_content()
