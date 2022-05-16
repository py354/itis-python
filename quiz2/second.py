from typing import Dict, Set


class NewsPortal:
    def __init__(self):
        self.__topics: Dict[str, Set[int]] = {}

    def create_topic(self, name: str):
        if name in self.__topics:
            print(f'panic: Топик {name} уже существует')

        self.__topics[name] = set()

    def subscribe(self, user_id: int, topic: str):
        if topic not in self.__topics:
            print(f'panic: Топик {topic} не существует')

        if user_id in self.__topics[topic]:
            print(f'Пользователь {user_id} уже подписан на {topic}')

        self.__topics[topic].add(user_id)

    def post_feed(self, topic: str, feed_id: int):
        if topic not in self.__topics:
            print(f'panic: Топик {topic} не существует')

        for user_id in self.__topics[topic]:
            print(f'Пользователь {user_id} получил новость {feed_id}')


if __name__ == '__main__':
    portal = NewsPortal()

    portal.create_topic('кино')
    portal.subscribe(1, 'кино')
    portal.subscribe(2, 'кино')

    portal.create_topic('сериалы')
    portal.subscribe(1, 'сериалы')

    portal.post_feed('кино', 100)
    portal.post_feed('сериалы', 200)