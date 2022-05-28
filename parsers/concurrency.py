from threading import Thread
from typing import List
from itertools import repeat
from multiprocessing import Pool
import time
from parsers.wiki_parser import wiki_parser


def single_parse(url: str, depth: int, base_path='data/'):
    """ Однопоточная версия парсера """

    # если глубина 0, то это конец рекурсии
    if depth == 0:
        return

    # рекурсивно обрабатываем в глубину
    links = wiki_parser(url, base_path)
    for link in links:
        single_parse(link, depth-1, base_path)


def threading_parse(url: str, depth: int, base_path='data/'):
    """ Версия парсера с использованием threading (без Pool) """
    if depth == 0:
        return

    links = wiki_parser(url, base_path)
    threads = [Thread(target=threading_parse, args=(link, depth-1, base_path)) for link in links]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def multiprocessing_parse(urls: [List[str] or str], depth: int, base_path='data/'):
    """ Параллельная версия парсера с использованием multiprocessing (c Pool) """
    if depth == 0:
        return

    if isinstance(urls, str):
        urls = [urls]

    with Pool(8) as executor:
        links = []
        for link_list in executor.starmap(wiki_parser, zip(urls, repeat(base_path))):
            links.extend(link_list)
        multiprocessing_parse(links, depth-1, base_path)


if __name__ == '__main__':
    url = 'https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D1%84%D0%B0%D0%BB%D1%8C%D1%8F'

    t1 = time.time()
    single_parse(url, 2)
    print(f'Single: {time.time()-t1} sec')

    t1 = time.time()
    threading_parse(url, 2)
    print(f'Threading: {time.time()-t1} sec')

    t1 = time.time()
    multiprocessing_parse(url, 2)
    print(f'Multiprocessing: {time.time()-t1} sec')


