import os
import time
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
        if delete_response.status_code == 202:
            operation_url = delete_response.json()["href"]
            operation_status = wait_operation_success(disk_client, operation_url)
            if operation_status != "success":
                cleanup_errors.append(
                    f"DELETE {path}: операция завершилась статусом {operation_status}"
                )
                continue
        elif delete_response.status_code != 204:
            cleanup_errors.append(
                f"DELETE {path}: ожидался 204 или 202, получен "
                f"{delete_response.status_code}"
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


def wait_operation_success(
    disk_client: YandexDiskClient,
    operation_url: str,
    *,
    attempts: int = 30,
    interval: float = 1.0,
) -> str:
    for _ in range(attempts):
        status_response = disk_client.get_operation_status(operation_url)
        if status_response.status_code != 200:
            pytest.fail(
                "Не удалось получить статус операции: "
                f"{status_response.status_code} {status_response.text}"
            )

        status = status_response.json()["status"]
        if status in ("success", "failed"):
            return status

        time.sleep(interval)

    pytest.fail("Операция не завершилась за отведённое время.")
