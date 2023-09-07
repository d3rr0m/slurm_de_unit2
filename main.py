import requests
import pprint


def main():
    url = 'http://5.159.103.105:4000/api/v1/logs'
    params = {
        'page': 3
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_json = response.json()
    max_page = round(response_json['totalEntries']/200+1)
    with open('file.json', 'a') as file:
        for page in range(1, 100+1):
            params['page'] = page
            response = requests.get(url, params=params)
            response.raise_for_status()
            response_json = response.json()
            file.write(str(response_json))


if __name__ == '__main__':
    main()