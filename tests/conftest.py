import os
from collections.abc import Generator
from uuid import uuid4

import pytest

from disk_client import YandexDiskClient


@pytest.fixture
def disk_client() -> YandexDiskClient:
    token = os.environ.get("YANDEX_DISK_TOKEN")
    if not token:
        pytest.fail("Для запуска тестов задайте переменную YANDEX_DISK_TOKEN.")
    return YandexDiskClient(token)


@pytest.fixture
def unique_folder_path() -> str:
    return f"app:/qa_test_{uuid4().hex}"


@pytest.fixture
def created_paths(disk_client: YandexDiskClient) -> Generator[list[str], None, None]:
    paths: list[str] = []
    yield paths

    cleanup_errors = []
    for path in paths:
        delete_response = disk_client.delete_resource(path)
        if delete_response.status_code != 204:
            cleanup_errors.append(
                f"DELETE {path}: ожидался 204, получен {delete_response.status_code}"
            )
            continue

        get_response = disk_client.get_resource(path)
        if get_response.status_code != 404:
            cleanup_errors.append(
                f"GET {path} после удаления: ожидался 404, получен "
                f"{get_response.status_code}"
            )

    if cleanup_errors:
        pytest.fail("Очистка тестовых данных завершилась ошибкой:\n" + "\n".join(cleanup_errors))
