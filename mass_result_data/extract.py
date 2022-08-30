import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def init(): 
    """
    Initializes the driver with optimized defaults, and returns it.
    """
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver: webdriver.Chrome = webdriver.Chrome(chrome_options=options)
    
    driver.get('https://rtmnu.digitaluniversity.ac/SearchDuplicateResult.aspx?ID=1091')
    
    captcha_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_CaptchaControll_captchaImage')))
    
    exam_input = Select(driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ExEv_ID'))
    
    exam_input.select_by_value('1')
    
    seat_no_input = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TxtPrn')
    seat_no_input.clear()

    input('Complete the procedure until the marksheet is shown, \033[1m DO NOT PRINT THE MARKSHEET \033[0m ...')
    return driver


def extract_html_from_seat_numbers(driver: webdriver.Chrome, seats: list[int|str]):
    # Extracts the html from the driver, and yeilds to the caller.
    # The driver should be initialized with init().

    seat_no_input = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TxtPrn')
    seat_no_input.clear()

    for id in [000000] + seats:
        seat_no_input = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TxtPrn')
        seat_no_input.clear()
        seat_no_input.send_keys(id)
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_btnSearch')))
        submit_button.click()
        table_thing = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_oGridViewExmdetails > tbody > tr:nth-child(2) > td:nth-child(5) > a')))
        table_thing.click()
        required_thing = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'divHTMLPrint')))
        if id == 000000:
            # Remove the data from the initial thing, it usually contains something else
            yield None, None

        yield required_thing.get_attribute('outerHTML'), id



def cleanup(driver: webdriver.Chrome):
    # Cleans up the driver.
    driver.quit()
    


def convert(html: str) -> dict:
    data = {}

    soup = BeautifulSoup(html, 'html5lib')
    bold_text = soup.find_all('b')

    field_student_name = bold_text[1]
    data['name'] = field_student_name.text.strip().split(':')[1].strip()

    field_mother_name = bold_text[2]
    data['mother_name'] = field_mother_name.text.strip().split(':')[1].strip()

    field_prn = bold_text[3]
    data['prn'] = field_prn.text.strip().split(':')[1].strip()

    field_exam_category = bold_text[4]
    data['exam_category'] = field_exam_category.text.strip().split(':')[
        1].strip()

    field_roll_number = bold_text[5]
    data['roll_number'] = field_roll_number.text.strip().split(':')[1].strip()

    field_date = bold_text[6]
    data['date'] = field_date.text.strip().split(':')[1].strip()

    field_center_code = bold_text[7]
    data['center_code'] = field_center_code.text.strip().split(':')[1].strip()

    field_medium = bold_text[8]
    data['medium'] = field_medium.text.strip().split(':')[1].strip()

    field_PL = bold_text[9]
    data['pl'] = field_PL.text.strip().split(':')[1].strip()

    field_college = bold_text[10]
    data['college'] = field_college.text.strip().split(':')[1].strip()

    result_table = soup.find_all('table')[6]
    result_table_body = result_table.find('tbody')
    result_rows = result_table_body.find_all('tr')

    data['__raw_result'] = []
    for row in result_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # Get rid of empty values
        data['__raw_result'].append([ele for ele in cols if ele])

    data['__raw_result'] = data['__raw_result'][2:]
    data['result'] = []
    for result_row in data['__raw_result']:
        am = 'undef'
        if 'TH' in result_row[2]:
            am = 'theory'
        elif 'PR' in result_row[2]:
            am = 'practical'

        data['result'].append({
            'assessment_method': am,
            'abbreviation': result_row[0],
            'subject_name': result_row[1],
            'university_assessment': {
                'min_marks': result_row[3].split('/')[0],
                'max_marks': result_row[3].split('/')[1] if '/' in result_row[3] else result_row[3],
                'marks_obtained': result_row[4]
            },
            'college_assessment': {
                'min_marks': result_row[5].split('/')[0],
                'max_marks': result_row[5].split('/')[1] if '/' in result_row[5] else result_row[5],
                'marks_obtained': result_row[6]
            },
            'total': {
                'min_marks': result_row[7].split('/')[0],
                'max_marks': result_row[7].split('/')[1] if '/' in result_row[7] else result_row[7],
                'marks_obtained': result_row[8]
            },
            'credits': result_row[9],
            'grade': result_row[10],
            'grade_point': result_row[11],
            'grade_point_value': result_row[12],
            # 'remarks': result_row[13]
            # The remarks are blank, being removed from the
        })

    # Handing the final data table at the end
    data_table = soup.find_all('table')[7]

    data['summary'] = {}
    data_row = data_table.find_all('tr')[1]
    cols = data_row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    cols = [ele for ele in cols if ele]

    data['summary']['incentive'] = cols[0]
    data['summary']['total_credits'] = cols[1]
    data['summary']['sum_grade_point_value'] = cols[2]
    data['summary']['sgpa'] = cols[3]
    data['summary']['out_of'] = cols[4]
    data['summary']['total_marks_obtained'] = cols[5]
    data['summary']['out_of_marks'] = cols[6]
    data['summary']['result'] = cols[7]
    # data['summary']['remark'] = cols[8]
    # remove the internal state management fields
    del data['__raw_result']

    return data