import re
import ssl

import requests
from bs4 import BeautifulSoup

from Constants import OUTPUT_FILE


def get_links(url):
    ssl._create_default_https_context = ssl._create_unverified_context

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'}

    session = requests.Session()
    session.verify = False
    html_page = session.get(url, headers=headers).content

    soup = BeautifulSoup(html_page, "lxml")
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
        links.append(link.get('href'))

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    links = list(dict.fromkeys(links))
    with open(OUTPUT_FILE, 'w') as f:
        for item in links:
            f.write("%s\n" % item)
    f.close()
