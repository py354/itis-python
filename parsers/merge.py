from maps.hash_map import HashMap


def merge_files(*filenames, output_file: str = 'result.txt'):
    """ Объединяет счетчики слов со страниц wiki """

    # создается общаяю мапа
    result = HashMap()
    maps = [HashMap.read(filename) for filename in filenames]

    # туда складываются значения с других мап
    for m in maps:
        for k, v in m:
            if k in result:
                result[k] += v
            else:
                result[k] = v

    # результат записывается в файл
    result.write(output_file)


if __name__ == '__main__':
    merge_files(
        '/home/danis/projects/itis-python/parsers/data/3bac801cc0ec4ec8909121a567c69e8c/words.txt',
        '/home/danis/projects/itis-python/parsers/data/3d22638d0a9c4c31bf9dbcc748f26250/words.txt',
        '/home/danis/projects/itis-python/parsers/data/4bafaa73de7f4b18b238f3e8d68c9caf/words.txt'
    )
