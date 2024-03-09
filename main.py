import datetime

import httpx
from sensitive_data import client_id, client_secret, username, password

subreddit = 'learnpython'


def get_token(client_id: str, client_secret: str, username: str, password: str) -> str:
    ''' получить токен '''
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": "User-Agent"}
    response = httpx.post("https://www.reddit.com/api/v1/access_token",
                          auth=(client_id, client_secret), data=post_data, headers=headers)
    return response.json()['access_token']


def get_latest_posts(token: str, subreddit: str) -> list:
    ''' получить публикации субреддита за последние 3 дня '''
    latest_posts = []
    today = datetime.date.today()

    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": "User-Agent"}

    response = httpx.get(f"https://oauth.reddit.com/r/{subreddit}/top.json?t=week", headers=headers)
    for post in response.json()['data']['children']:
        created = int(post['data']['created'])
        if datetime.date.fromtimestamp(created) > today - datetime.timedelta(days=3):
            latest_posts.append(post)
    return latest_posts


def get_authors(posts: list[dict]) -> list:
    ''' получить авторов публикаций '''
    return [post['data']['author'] for post in posts]


def count_items_in_list(authors: list[str]) -> list[tuple[str, int]]:
    ''' посчитать количество публикаций авторами '''
    posts_by_authors = {}
    for author in authors:
        if author not in posts_by_authors:
            posts_by_authors[author] = 1
        else:
            posts_by_authors[author] = posts_by_authors[author] + 1

    return list(posts_by_authors.items())


def sort_list_by_second_element(list_for_sort: list[tuple[str, int]]) -> list[tuple[str, int]]:
    return sorted(list_for_sort, key=lambda item: item[1], reverse=True)


def get_first_items(temp_list: list[tuple[str, int]]) -> list[str]:
    return [item[0] for item in temp_list]


def get_top_authors(posts: list[dict]) -> list[str]:
    authors = get_authors(posts)
    counted_posts_by_author = count_items_in_list(authors)
    sorted_authors_by_count_posts = sort_list_by_second_element(counted_posts_by_author)
    return get_first_items(sorted_authors_by_count_posts)


def get_commentators(data: dict, commentators: list[str]) -> None:
    for comment_data in data['data']['children']:
        author = comment_data['data']['author']
        commentators.append(author)
        if comment_data['data']['replies']:
            get_commentators(comment_data['data']['replies'], commentators)


def get_comments(token: str, post_id: str) -> dict:
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    response = httpx.get(f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}/comment.json", headers=headers)
    return response.json()[1]


def get_top_commentators(token: str, posts: list) -> list:
    commentators: list[str] = []

    for post in posts:
        post_id = post['data']['id']
        comments = get_comments(token, post_id)
        get_commentators(comments, commentators)

    counted_comments_by_author = count_items_in_list(commentators)
    sorted_authors_by_count_comments = sort_list_by_second_element(counted_comments_by_author)
    return get_first_items(sorted_authors_by_count_comments)


def main():
    token = get_token(client_id, client_secret, username, password)
    posts = get_latest_posts(token, subreddit)
    top_authors = get_top_authors(posts)
    top_commentators = get_top_commentators(token, posts)

    print(top_authors)
    print(top_commentators)


if __name__ == '__main__':
    main()
