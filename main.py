import threading
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import aiohttp
from aiohttp import ClientSession
import asyncio
from aiocsv import AsyncDictWriter
import aiofiles
import os
import httpx
import argparse
from collections import namedtuple
from urllib.parse import urlunparse, urlencode
from codetiming import Timer
from threading import Thread
import time, datetime
import csv



URL = 'http://5.159.103.105:4000/api/v1/logs'

MAX_PAGE = 13
#MAX_PAGE = 5000
FILENAME = 'file.json'


def init():
    init_url = 'http://5.159.103.105:4000/api/v1/structure'
    response = httpx.get(init_url)
    response.raise_for_status()
    fieldnames = [item['field_name'] for item in response.json()['items']]
    
    with open('file.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        writer.writeheader()
    return fieldnames


async def async_write_csv(rows, fieldnames):
    with aiofiles.open('file.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = AsyncDictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n', delimiter=';')
        await writer.writerows(rows['items'])
    print(200)


def test_write(rows, fieldnames):
    with open('file.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        writer.writerows(rows['items'])


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


async def save_to_disc(response):
    with open('file.json', 'ab') as file:
        async for chunk in response.content.iter_chunked(2048):
            file.write(chunk)


async def download_page(name, queue, fieldnames):
    #timer = Timer(text=f'{name} elapsed time: {{:.3f}}')
    async with aiohttp.ClientSession() as session: 
        while not queue.empty():
            url = await queue.get()
            #print(f'Task {name} is fetching {url}')
            #timer.start()
            async with session.get(url) as response:
                if response.status == 429:
                    print (f'429 error, {url}')
                    await asyncio.sleep(5)
                    await queue.put(url)
                if response.status != 200:
                    print('NOT OK')
                elif response.status == 200:
                    rows = await response.json()
                    test_write(rows, fieldnames)
            #timer.stop()


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
    parser = argparse.ArgumentParser(
        description='Программа получает данные из сервиса API'\
        ' http://5.159.103.105:4000/ и сохраняет полученный датасет в файл в'\
        ' формате csv.'
    )
    parser.add_argument(
        '-s',
        '--start_page',
        default=1,
        type=int,
        help='Номер стартовой страницы с которой начнется выборка данных. '\
            'Значение по умолчанию - 1.',
        )
    parser.add_argument(
        '-e',
        '--end_page',
        default=131962,
        type=int,
        help='Номер последней страницы на которой выборка данных закончится. '\
            'Значение по умолчанию - масимально доступное кол-во страниц.',
        )
    parser.add_argument(
        '-t',
        '--tasks',
        default=1,
        type=int,
        help='Количевство одновременно работающих task '\
            'Значение по умолчанию - масимально доступное кол-во страниц.',
        )
    args = parser.parse_args()
    
    remove_file(FILENAME)
    fieldnames = init()
    queue = asyncio.Queue()
    urls = [create_url(page) for page in range(args.start_page, args.end_page+1)]
    for url in urls:
        await queue.put(url)
    
    tasks = (asyncio.create_task(download_page(f'{worker}', queue, fieldnames)) for worker in range(args.tasks))
    with Timer(text='\nTotal elapse time: {:.1f}'):
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    
    start_time = time.time()
    asyncio.run(main())
    #test_list()
    print("--- %s seconds ---" % (time.time() - start_time))
