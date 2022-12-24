from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# get cwd of file
import pathlib

import os

# loading env
from dotenv import load_dotenv

from loguru import logger

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

FILE_DIR = pathlib.Path(__file__).parent.parent
logger.info(f"The file path of the current file is {FILE_DIR}")

load_dotenv()

HELLO_FRESH_USER = os.getenv('HELLO_FRESH_USER')
HELLO_FRESH_PASSWORD = os.getenv('HELLO_FRESH_PASSWORD')

# logger.info(f"e: {os.environ[HELLO_FRESH_USER]}, p: {os.environ[HELLO_FRESH_PASSWORD]}")
# for i,v in os.environ.items():
#     if i.startswith("HELLO"):
#         print(i,v)
# exit()
HF_WEB = "https://www.hellofresh.co.uk/my-account/deliveries/past-deliveries?subscriptionId=6007853&week=2023-W04"
# If you want to open Chrome
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(HF_WEB)


# frame = driver.find_element(By.XPATH, "//input[@name='username']")
# driver.switch_to.frame(frame)
username = driver.find_element(By.XPATH, "//input[@name='username']")
password = driver.find_element(By.XPATH, "//input[@name='password']")

username.send_keys(HELLO_FRESH_USER)
password.send_keys(HELLO_FRESH_PASSWORD)
driver.find_element(By.XPATH,"//button[@type='submit']").click()