from collections.abc import Callable, Iterable, Mapping
from typing import Any
import aiohttp
from aiohttp import ClientSession
import asyncio
import os
import urllib
from collections import namedtuple
from urllib.parse import urlunparse, urlencode
import queue
from threading import Thread
import time, datetime



URL = 'http://5.159.103.105:4000/api/v1/logs'
MAX_PAGE = 131962
#MAX_PAGE = 5000
CHUNK_SIZE = 1000
FILE_NAME = 'file.json'
result = []


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


async def save_to_disc(response):
    with open('file.json', 'ab') as file:
        async for chunk in response.content.iter_chunked(2048):
            file.write(chunk)


async def download_page(session: ClientSession, url: str):
    async with session.get(url) as response:
        with open('file.json', 'ab') as file:
            async for chunk in response.content.iter_chunked(1024):
                file.write(chunk)
        return response.status
    #response.raise_for_status()
    #if response.status_code != 200:
        #print(f'starts {url}')
        #response_json = response.json()
    


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


def test_list():
    urls = [page for page in range(1, 70)]
    while urls:
        requests = urls[:50]
        urls = urls[50:]
        print(requests)
        print(urls)


async def main():
    remove_file(FILE_NAME)
    urls = [create_url(page) for page in range(1, MAX_PAGE)]
    conn = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=conn) as session:
        while urls:
            start_time = time.time()
            urls_chunk = urls[:CHUNK_SIZE]
            urls = urls[CHUNK_SIZE:]
        
            requests = [download_page(session, url) for url in urls_chunk]
            
            responses = await asyncio.gather(*requests, return_exceptions=True)
            """ for done_task in asyncio.as_completed(requests, timeout=1000):
                try:
                    result = await done_task
                    if result != 200:
                        print(f'Status is {result}')
                except aiohttp.ClientConnectionError:
                    print('disc')
                    #asyncio.sleep(1)
                except asyncio.TimeoutError:
                    print(f'{result}timeout')
                        """
            #for task in asyncio.all_tasks():
                #print(task)
            ok_status = 0
            notok_status = 0
            exceptions = [res for res in responses if isinstance(res, Exception)]
            successful_results = [res for res in responses if not isinstance(res, Exception)]
            for response in responses:
                if response == 200:
                    ok_status+=1 
                else:
                    notok_status+=1
            print (f'ok - {ok_status}')
            print (f'not ok - {notok_status}')
            #print (f'ok - {successful_results}')
            print (f'not ok - {exceptions}')
            print(datetime.datetime.utcnow())
            print("--- %s seconds ---" % (time.time() - start_time))
            await asyncio.sleep(10)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    #test_list()
    print("--- %s seconds ---" % (time.time() - start_time))

