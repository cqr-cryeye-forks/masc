import os

import requests

from Constants import PATH_TO_CONTENT_FOLDER


def load_links():
    with open("output.txt", 'r') as f:
        links = f.readlines()

    for link in links:
        if not link.startswith('http'):
            continue

        resource_response = requests.get(link, verify=False)
        print(link)

        filename = os.path.join(PATH_TO_CONTENT_FOLDER, os.path.basename(link))
        if resource_response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(resource_response.content)
            print(f"Resource {filename} downloaded.")
        else:
            print(f"Resource {filename} not downloaded: {resource_response.status_code}")
