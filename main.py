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
MAX_PAGE = 1310
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
    urls = [create_url(page) for page in range(1, MAX_PAGE)]

    async with aiohttp.ClientSession() as session:
        status = await download_page(session, urls[0])
        print(f'{status} status had been returned')


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))

