from collections.abc import Callable, Iterable, Mapping
from typing import Any
import aiohttp
from aiohttp import ClientSession
import asyncio
import urllib
from collections import namedtuple
from urllib.parse import urlunparse, urlencode
import queue
from threading import Thread
import time



URL = 'http://5.159.103.105:4000/api/v1/logs'
#MAX_PAGE = 131962
MAX_PAGE = 13000
result = []


async def download_page(session: ClientSession, url: str):
    async with session.get(url) as response:
        return response.status
    #response.raise_for_status()
    #if response.status_code != 200:
        #print(f'starts {url}')
        #response_json = response.json()
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


async def main():
    start_url_time = time.time()
    urls = [create_url(page) for page in range(1, MAX_PAGE)]
    print("--- %s seconds ---" % (time.time() - start_url_time))
    
    async with aiohttp.ClientSession() as session:
        requests = [download_page(session, url) for url in urls]
        #statuses = await asyncio.gather(*requests)
        for done_task in asyncio.as_completed(requests):
            try:
                result = await done_task
                if result != 200:
                    print(f'Status is {result}')
            except asyncio.TimeoutError:
                print("timeout")
            except aiohttp.ServerDisconnectedError:
                print('disc')
        
        #for task in asyncio.all_tasks():
            #print(task)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))

