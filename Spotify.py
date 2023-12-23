import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from random import randint
import requests
import openpyxl

# Load the Excel file
file_path = r"C:\Users\aarya\Desktop\Spotify.xlsx"
workbook = openpyxl.load_workbook(file_path)

# Select the specific worksheet in the workbook
worksheet_name = 'Sheet1'  # Replace with the name of your worksheet
worksheet = workbook[worksheet_name]

SCRAPEOPS_API_KEY = 'a4fe4707-ad1a-4824-bfbe-8e312b1fb8e5'

def get_user_agent_list():
  response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY)
  json_response = response.json()
  return json_response.get('result', [])



def get_random_user_agent(user_agent_list):
  random_index = randint(0, len(user_agent_list) - 1)
  return user_agent_list[random_index]



def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

emails = []
passwords = []


i= 400
while i < 405:

    ## Retrieve User-Agent List From ScrapeOps
    user_agent_list = get_user_agent_list()
    user_agent_list
    ua = get_random_user_agent(user_agent_list)

    chrome_driver_path = r"C:\Users\aarya\Downloads\Programs\chrome-win64\chrome-win64\chrome.exe"

    options = webdriver.ChromeOptions()

    options.binary_location = r"C:\Users\aarya\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\chrome.lnk"

    options.add_argument(f"user-agent={ua}")


    # Initialize the WebDriver with the updated ChromeDriver
    web = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    # Open the desired URL
    web.get('https://www.spotify.com/in-en/signup?flow_id=6391c6c5-3877-4221-b9f8-93001f3fc28c%3A1690389682&forward_url=https%3A%2F%2Fopen.spotify.com%2F%3Fflow_ctx%3D6391c6c5-3877-4221-b9f8-93001f3fc28c%253A1690389682')
    
    # Wait for the email input field to be clickable
    email_fill = WebDriverWait(web, random.randint(1,5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    email = random_char(7) + "@gmail.com"
    email_fill.send_keys(email)

    # Wait for the password input field to be clickable
    password_fill = WebDriverWait(web, random.randint(1,5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    num = random.randint(400,2000)
    password = random_char(5) + str(num) + "*"
    password_fill.send_keys(password)

    # Fill in name, year of birth, month of birth, and date of birth in a similar way as above
    name = random_char(5)
    name_fill = WebDriverWait(web, random.randint(1,5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="displayname"]')))
    name_fill.send_keys(name)

    year_of_birth = random.randint(1980, 2005)
    year_of_birth_fill = WebDriverWait(web, random.randint(1,5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="year"]')))
    year_of_birth_fill.send_keys(year_of_birth)

    
    month_of_birth_fill = web.find_element(By.XPATH,f'//*[@id="month"]/option[2]').click()

    date_of_birth = random.randint(1, 30)
    date_of_birth_fill =    WebDriverWait(web, random.randint(1,5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="day"]')))
    date_of_birth_fill.send_keys(date_of_birth)


    # Execute JavaScript to click the gender radio button
    gender_script = 'document.querySelector("#__next > main > div > div > form > fieldset > div > div:nth-child(1) > label > span:nth-child(2)").click();'
    web.execute_script(gender_script)

    # Wait for the sign-up button to be clickable before executing the script
    sign_up_button = WebDriverWait(web, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/form/div[7]/div/button/span[1]')))
    sign_up_button.click()
    time.sleep(2)
    landing_page_substring = "open.spotify.com"
    wait = WebDriverWait(web, 10)

    if wait.until(lambda driver: landing_page_substring in driver.current_url):
        # If the landing page URL is found, you can proceed with the next steps
        row_number_email = i
        column_letter_email = 'A'
        cell_email = worksheet[column_letter_email + str(row_number_email)]
        cell_email.value = email

        row_number_password = i
        column_letter_password = 'B'
        cell_password = worksheet[column_letter_password + str(row_number_password)]
        cell_password.value = password
        # Save the changes back to the Excel file
        workbook.save(file_path)

        # Close the workbook
        workbook.close()
    else:
        # If the landing page URL is not found within the timeout, run your desired code here
        i = i - 1
        wait = WebDriverWait(web, 10)
        # For example, you might want to log this issue or take some other action


    time.sleep(2)
    web.delete_all_cookies()

    web.quit()

    
    if i % 5 == 0:
        time.sleep(random.randint(5,10))

    i = i + 1