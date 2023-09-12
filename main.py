from collections.abc import Callable, Iterable, Mapping
from typing import Any
import requests
import urllib
from collections import namedtuple
from urllib.parse import urlunparse, urlencode
import queue
from threading import Thread
import time


URL = 'http://5.159.103.105:4000/api/v1/logs'
#MAX_PAGE = 131962
MAX_PAGE = 13100
result = []


class DownloadThread(Thread):

    def __init__(self, queue, name):
        super().__init__()
        self.queue = queue
        self.name = name


    def run(self):
        while True:
            url = self.queue.get()
            response = requests.get(url)
            #response.raise_for_status()
            if response.status_code != 200:
                print(f'==============={response.status_code}==={self.name}')
            #print(f'starts {url}')
            #response_json = response.json()
            result.append(response.json())
            self.queue.task_done()
            #with open('file.json', 'a') as file:
            #    file.write(str(response.json()))


def create_url(page):
    Components = namedtuple(
    typename='Components', 
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
    )
    params = {
        'page': f'{page}',
    }
    url = urlunparse(
        Components(
            scheme='http',
            netloc='5.159.103.105:4000',
            query=urlencode(params),
            path='',
            url='/api/v1/logs',
            fragment='',
        )
    )
    return url


def main():
    urls = [create_url(page) for page in range(1, MAX_PAGE)]
    q = queue.Queue()
    threads = [DownloadThread(q, f'Thread {i+1}') for i in range(500)]

    for t in threads:
        t.daemon = True
        t.start()

    for url in urls:
        q.put(url)

    q.join()
    with open('file.json', 'a') as file:
        file.write(str(result))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))