import requests
import pprint
from tqdm import tqdm


def main():
    url = 'http://5.159.103.105:4000/api/v1/logs'
    params = {
        'page': 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_json = response.json()
    max_page = round(response_json['totalEntries']/200+1)
    content = []
    with requests.session() as session:
        for page in tqdm(range(1, max_page), colour='BLUE', desc='Fetching data outside loop:'):
            params['page'] = page
            response = session.get(url, params=params)
            response.raise_for_status()
            content.append(response.json())

    with open('file.json', 'a') as file:
        file.write(content)


if __name__ == '__main__':
    main()