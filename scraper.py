from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

KEYWORDS = ['split', 'dividend', 'merger',
            'ex-split', 'bonus' 'right', 'equity', 'shares']
TEST_URL = 'https://www.bloombergquint.com/stock/226036/nestle-india-ltd/corporate-actions'


def process_text(all_text):
    processed_text = []
    for text in all_text:
        if any(word in text.lower() for word in KEYWORDS):
            text = text.strip()
            if len(text) > 50:
                processed_text.append(text)
    return processed_text


def clean_text(text):
    text = text.strip()
    return text


def scrape(url):
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_text = soup.get_text()
    driver.quit()
    if soup is None:
        return []
    # This will get all data stored in p, h1..h6 tags
    processed_text = process_text(all_text)
    # Get data stored in the form of tables
    all_tables = soup.find_all('table')
    for table in all_tables:
        table_column = table.find_all('th')
        thead = []
        for head in table_column:
            thead.append(clean_text(head.get_text()))
        if len(thead) == 0:
            continue
        table_row = table.find_all('tr')
        for row in table_row:
            table_data = row.find_all(re.compile('^td'))
            if len(table_data) == 0:
                continue
            trow = []
            for index, data in enumerate(table_data):
                trow.append(f'{thead[index]} {clean_text(data.get_text())}')
            text = ' '.join(trow)
            if any(word in text.lower() for word in KEYWORDS):
                processed_text.append(text)
    return processed_text
