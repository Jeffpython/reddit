import pytest
import httpx

from sensitive_data import client_id, client_secret, username, password
from main import (get_token, get_latest_posts, get_authors, count_items_in_list, sort_list_by_second_element,
                  get_top_authors, get_first_items, get_comments)


@pytest.fixture
def token():
    return get_token(client_id, client_secret, username, password)


@pytest.fixture
def subreddit():
    return 'learnpython'


@pytest.fixture
def posts(token, subreddit):
    return get_latest_posts(token, subreddit)


def test__get_token__returns_string():
    assert isinstance(get_token(client_id, client_secret, username, password), str)


def test__get_token__returns_exception_with_blank_client_id():
    with pytest.raises(KeyError):
        get_token(client_id='', client_secret=client_secret, username=username, password=password)


def test__get_token__returns_exception_with_blank_client_secret():
    with pytest.raises(KeyError):
        get_token(client_id=client_id, client_secret='', username=username, password=password)


def test__get_token__returns_exception_with_blank_username():
    with pytest.raises(KeyError):
        get_token(client_id=client_id, client_secret=client_secret, username='', password=password)


def test__get_token__returns_exception_with_blank_password():
    with pytest.raises(KeyError):
        get_token(client_id=client_id, client_secret=client_secret, username=username, password='')


def test__get_latest_posts__returns_list(token, subreddit):
    assert isinstance(get_latest_posts(token, subreddit), list)


def test__get_latest_posts__returns_exception_with_blank_token(subreddit):
    with pytest.raises(httpx.LocalProtocolError):
        get_latest_posts(token='', subreddit=subreddit)


def test__get_latest_posts__returns_exception_with_blank_subreddit(token):
    with pytest.raises(KeyError):
        get_latest_posts(token=token, subreddit='')


def test__get_authors__returns_authors_list():
    data = [{'data': {'author': 'author1'}},
            {'data': {'author': 'author2'}}]
    assert get_authors(data) == ['author1', 'author2']


@pytest.mark.parametrize(('data', 'expected_result'), [
    ([{'data': {'author': 'author1'}}], ['author1']),
    ([{'data': {'author': 'author1'}}, {'data': {'author': 'author2'}}], ['author1', 'author2'])
])
def test__get_authors__returns_authors_list(data, expected_result):
    assert get_authors(data) == expected_result


@pytest.mark.parametrize(('items', 'expected_result'), [
    (['author'], [('author', 1)]),
    (['author', 'author'], [('author', 2)]),
    (['author1', 'author2'], [('author1', 1), ('author2', 1)]),
])
def test__count_items_in_list__returns_count_items(items, expected_result):
    assert count_items_in_list(items) == expected_result


@pytest.mark.parametrize(('items', 'expected_result'), [
    ([], []),
    ([('author', 1), ('author', 1)], [('author', 1), ('author', 1)]),
    ([('author', 1), ('author', 2)], [('author', 2), ('author', 1)]),
])
def test__sort_list_by_second_element__returns_sorted_items(items, expected_result):
    assert sort_list_by_second_element(items) == expected_result


@pytest.mark.parametrize(('tuples_list', 'expected_result'), [
    ([], []),
    ([('author1', 2), ('author2', 1)], ['author1', 'author2']),
])
def test__get_first_items__returns_first_items(tuples_list, expected_result):
    assert get_first_items(tuples_list) == expected_result


