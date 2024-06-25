import os
from functools import lru_cache
from pprint import pprint
from typing import Any
from urllib.parse import urlencode, urlparse

import requests


@lru_cache
def get_netbox_item_recursion(path: str, query: str = "") -> list[dict[str, Any]]:
    """получение данных из netbox, в ENV необходимы переменные NB_URL и NB_TOKEN
    например:
      - export NB_URL=http://10.211.55.7:8000
      - export NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f

    Args:
        path (str): ресурс вида '/api/dcim/devices/'
        query (str, optional): параметры запроса

    Returns:
        list[dict[str, Any]]: список словарей с результатами
    """
    url = os.environ.get("NB_URL", "")
    token = os.environ.get("NB_TOKEN", "")
    if not all([url, token]):
        raise ValueError("отсутсвуют параметры подключения к серверу")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(
        url=url + path,
        params=query,
        headers=headers,
    )
    response.raise_for_status()
    result_json = response.json()

    if "count" not in result_json and "results" not in result_json:
        return [result_json]

    result: list = result_json.get("results", [])
    next_page = result_json.get("next")

    if next_page is None:
        return result
    else:
        next_query = urlparse(next_page).query
        result.extend(get_netbox_item_recursion(path, next_query))
    return result


@lru_cache
def get_netbox_item_flat(path: str, query: str = "") -> list[dict[str, Any]]:
    """получение данных из netbox, в ENV необходимы переменные NB_URL и NB_TOKEN
    например:
      - export NB_URL=http://10.211.55.7:8000
      - export NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f

    Args:
        path (str): ресурс вида '/api/dcim/devices/'
        query (str, optional): параметры запроса

    Returns:
        list[dict[str, Any]]: список словарей с результатами
    """

    def _make_request(path: str, query: str) -> dict[str, Any]:
        # так как запрос делается несколько раз, то он и проверка ответа вынесена в отдельную функцию
        response = requests.get(url=url + path, params=query, headers=headers)
        response.raise_for_status()
        return response.json()

    # параметры подключения к серверу
    url = os.environ.get("NB_URL")
    token = os.environ.get("NB_TOKEN")
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    # проверка, что определены токен и адрес
    if not all([url, token]):
        raise ValueError("отсутсвуют параметры подключения к серверу")

    # первый запрос
    response = _make_request(path, query)

    # если запрашивался один конкретный ресурс, тогда в ответ в виде списка с параметрами ресурса
    # и в нем нет ключей count (всего ресурсов) и results (список ресурсов), поэтому в таком случае
    # оборачиваем в список наш один ресурс и сразу возвращаем
    if "count" not in response and "results" not in response:
        return [response]

    # если запрашивалась выборка ресурсов, тогда её можно получить по ключу results
    result: list = response.get("results", [])

    # и если включена пагинация, тогда адрес следующей страницы
    next_page = response.get("next")
    # пока не дойдем до последней страницы, делаем запросы со смещением
    while next_page is not None:
        # сами параметры запросы получаем из адреса следующей страницы
        query = urlparse(next_page).query
        # выполняем запрос следующей страницы
        response = _make_request(path, query)
        # обновляем адрес следующей страницы, важно не забыть, иначе получится бесконечный цикл
        next_page = response.get("next")
        # дополняем результат первого запроса (вне цикла который был) очередными ресурсами
        result.extend(response.get("results"))

    return result


q = [
    ("role", "access-switch"),
    ("limit", 2),
    ("brief", True),
]

nb_devices = get_netbox_item_flat(
    path="/api/dcim/devices/",
    query=urlencode(q),
)

print(f"{'№':>3}: {'id':>3} - device name")
for indx, device in enumerate(nb_devices, 1):
    print(f"{indx:>3}: {device.get('id'):>3} - {device.get('name')}")
    # print(f"{indx:>3}: {device.get('name')}")
