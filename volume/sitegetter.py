'''
Run this to get html files

This file contains code to obtain html data from oslo bors and yahoo finance
'''
import argparse
import re
import threading
import time
from pprint import pprint
from typing import List
import sys
import pathlib
import os

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas import DataFrame, to_numeric
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

def dump_assert(file: str):
    assert file is not None, 'File parameter must be specified when dump=True'

def get_osebx_htmlfile(url: str, timeout: int=2, wait_target_class: str=None,
                       verbose: int=1, dump: bool=True, file: str=None) -> str:
    '''Load OSEBX html files using selenium'''

    if verbose >= 1: print(f'Gathering data from {url}')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    if verbose >= 2: print('Initialized chromedriver')

    driver.get(url)

    if verbose >= 2: print('Waiting for target HTML class to appear')

    # If the webpage dynamically loads the table with the stock information. This code will force the webdriver
    # wait until the wanted element is loaded.
    if not wait_target_class is None:
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, wait_target_class))
            )
        except:
            print(f'Timeout: Could not load class {wait_target_class} from {url}')
            driver.quit()
            exit()

    if verbose >= 2: print('Element located')

    page_src = driver.page_source
    driver.quit()

    if dump:
        if verbose >= 1: print(f'Dumping HTML file: {file}')
        dump_assert(file)
        with open(file, 'w+') as file:
            file.write(page_src)

    return page_src

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get("google.com")
