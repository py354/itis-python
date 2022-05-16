import requests
from typing import List


def get_emails(username: str) -> List[str]:
    """
    1. Получаем UserID по username
    2. Получаем все посты по UserID
    3. Получаем все email по комментариям
    """
    user_id = get_user_id(username)
    post_ids = get_post_ids(user_id)

    emails = []
    for post_id in post_ids:
        emails.extend(get_post_emails(post_id))

    return emails


def get_user_id(username: str) -> int:
    r = requests.get('https://jsonplaceholder.typicode.com/users', params={'username': username})
    return r.json()[0]['id']


def get_post_ids(user_id: int) -> List[int]:
    r = requests.get('https://jsonplaceholder.typicode.com/posts', params={'userId': user_id})
    return [post['id'] for post in r.json()]


def get_post_emails(post_id: int) -> List[str]:
    r = requests.get('https://jsonplaceholder.typicode.com/comments', params={'postId': post_id})
    return [comment['email'] for comment in r.json()]


if __name__ == '__main__':
    print(get_emails('Antonette'))
