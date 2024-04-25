import os

import requests

from Constants import PATH_TO_CONTENT_FOLDER, OUTPUT_FILE


def load_links():
    with open(OUTPUT_FILE, 'r') as f:
        links = f.readlines()

    counter = 0
    for link in links:
        link = link.strip()
        if not link.startswith('http'):
            continue

        resource_response = requests.get(link, verify=False)
        print(link)

        name = link.split('/')[-1]
        if not name:
            name = str(counter)
        filename = os.path.join(PATH_TO_CONTENT_FOLDER, name)
        if resource_response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(resource_response.content)
            print(f"Resource {filename} downloaded.")
        else:
            print(f"Resource {filename} not downloaded: {resource_response.status_code}")

        counter += 1
