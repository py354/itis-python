""" Модуль для парсинга wikipedia """

from typing import List
from os.path import join
from os import makedirs
import re
import uuid
import requests
from bs4 import BeautifulSoup

from maps.hash_map import HashMap

WIKI_DOMAIN = "https://ru.wikipedia.org"
WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"


def get_content(url: str = WIKI_RANDOM) -> bytes:
    """ Получение файла и url по ссылке """
    page = requests.get(url)
    return page.content


def get_text(content: bytes) -> str:
    """ Парсинг текста с content, без тегов """
    html = content.decode('utf-8')
    soup = BeautifulSoup(html, 'html5lib')
    for item in soup.find_all('script'):
        item.extract()
    for item in soup.find_all('style'):
        item.extract()
    return soup.get_text()


def get_wiki_urls(content: bytes) -> List[str]:
    """ Получение ссылок на wiki с html-текста """
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', str(content))
    filtered_urls = filter(lambda u: u.startswith('/wiki/'), urls)
    corrected_urls = map(lambda u: WIKI_DOMAIN + u, filtered_urls)
    return list(corrected_urls)


def words_count(text: str) -> HashMap:
    """ Сбор количества встречи слов """
    data = HashMap()
    words = text.split()
    for word in words:
        word = word.lower()
        if word in data:
            data[word] += 1
        else:
            data[word] = 1

    return data


def wiki_parser(url: str, base_path: str) -> List[str]:
    """
        Функция для парсинга страницы:
        1) В директории base_path проверяет файл url.txt (мапа спаршенных страниц)
        1.1) Если страница уже спаршена, возвращает список ссылок с этой страницы
        1.2) Иначе добавляет url в url.txt, создает папку и начинаете парсинг
        2) Сохраняет content
        3) Сохраняет words (кол-во слов в тексте страницы)
    """

    urls_filename = join(base_path, 'urls.txt')

    try:
        urls = HashMap.read(urls_filename)
    except FileNotFoundError:
        urls = HashMap()

    # если страница уже спаршена
    if url in urls:
        page_dir = join(base_path, urls[url])
        with open(join(page_dir, 'content'), 'rb') as file:
            content = file.read()
            return get_wiki_urls(content)

    # создаем папку под данные
    page_dir = uuid.uuid4().hex
    urls[url] = page_dir
    page_dir = join(base_path, page_dir)
    makedirs(page_dir)

    # получаем данные с вики
    content = get_content(url)
    text = get_text(content)
    words = words_count(text)
    links = get_wiki_urls(content)

    # сохраняем данные в папку
    with open(join(page_dir, 'content'), 'wb') as file:
        file.write(content)
    words.write(join(page_dir, 'words.txt'))

    # сохраняем url в список спаршенных url и возвращаем ссылки
    urls.write(urls_filename)
    return links


if __name__ == '__main__':
    # для теста
    # при каждом запуске будет создаваться только одна папка,
    # т.к. ссылка всегда одна и та же (WIKI_RANDOM)
    print(wiki_parser(WIKI_RANDOM, 'data/'))
