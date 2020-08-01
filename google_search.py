from googleapiclient.discovery import build
from configparser import ConfigParser

configure = ConfigParser()
configure.read("secret.ini")

KEY = configure.get("GOOGLE", "developerKey")
CX = configure.get("GOOGLE", "cx")

def google_search(company_name):
    service = build("customsearch", "v1",
                    developerKey=KEY)

    res = service.cse().list(
        q=f'{company_name} corporate actions',
        cx=CX
    ).execute()
    response = res.get('items', [])
    link_list = []
    for resp in response:
        link = resp.get('link', None)
        if link is None:
            continue
        link_list.append(link)
    response_dict = {
        'company': company_name,
        'urls': link_list
    }
    return response_dict