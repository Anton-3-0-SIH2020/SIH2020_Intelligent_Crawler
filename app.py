from google_search import google_search
from scraper import scrape
from constants import LIMIT_WEBSITES
# import json


def app(company_name):
    search_data = google_search(company_name)
    urls = search_data.get('urls', [])
    urls = urls
    textual_data = []
    currently_scraped = 0
    for url in urls:
        if currently_scraped == LIMIT_WEBSITES:
            break
        try:
            data = scrape(url)
            if len(data) == 0:
                continue
            textual_data.append({
                'url': url,
                'data': data
            })
            currently_scraped += 1
        except Exception as err:
            print(err)
            print(company_name)
            print(f"Error occured while scraping {url}")
#    with open('test.json', 'w') as t:
#        json.dump(textual_data, t)
    return textual_data
