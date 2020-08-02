from google_search import google_search
from scraper import scrape
from constants import LIMIT_WEBSITES


def app(company_name):
    search_data = google_search(company_name)
    urls = search_data.get('urls', [])
    urls = urls
    textual_data = []
    structured_ca_data = []
    currently_scraped = 0
    for url in urls:
        if currently_scraped == LIMIT_WEBSITES:
            break
        try:
            unstructured_data, structured_data = scrape(url)
            if len(unstructured_data) == 0 and len(structured_data) == 0:
                continue
            if len(unstructured_data) != 0:
                textual_data.append({
                    'url': url,
                    'data': unstructured_data
                })
            if len(structured_data) != 0:
                structured_ca_data.append({
                    'url': url,
                    'data': structured_data
                })
            currently_scraped += 1
        except Exception as err:
            print(err)
            print(company_name)
            print(f"Error occured while scraping {url}")
    return textual_data, structured_ca_data


"""
textual_data : 
[
    {
        'url':......,
        'data': [
            'text1',
            'text2',
        ]
    },
    {
        'url':......,
        'data': [
            'text1',
            'text2',
        ]
    },
]


structured_ca_data :
[
    {
        'url':......,
        'data': [
            {
                param1: val,
                param2: val,
            },
            {
                param1: val,
                param2: val,
            },
        ]
    },
    {
        'url':......,
        'data': [
            {
                param1: val,
                param2: val,
            },
        ]
    },
]
"""
