import pytest

from disk_client import YandexDiskClient


@pytest.mark.positive
def test_tc001_create_folder(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    response = disk_client.create_folder(unique_folder_path)

    assert response.status_code == 201, response.text
    created_paths.append(unique_folder_path)

    resource_response = disk_client.get_resource(unique_folder_path)
    assert resource_response.status_code == 200, resource_response.text

    resource = resource_response.json()
    assert resource["path"].endswith(unique_folder_path.removeprefix("app:"))
    assert resource["type"] == "dir"


@pytest.mark.positive
def test_tc002_get_existing_folder(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    create_response = disk_client.create_folder(unique_folder_path)
    assert create_response.status_code == 201, create_response.text
    created_paths.append(unique_folder_path)

    response = disk_client.get_resource(unique_folder_path)
    assert response.status_code == 200, response.text

    resource = response.json()
    assert resource["type"] == "dir"
    assert resource["path"].endswith(unique_folder_path.removeprefix("app:"))


@pytest.mark.positive
def test_tc004_move_empty_folder(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    destination_path = f"{unique_folder_path}_moved"

    create_response = disk_client.create_folder(unique_folder_path)
    assert create_response.status_code == 201, create_response.text

    response = disk_client.move_resource(unique_folder_path, destination_path)
    assert response.status_code == 201, response.text
    created_paths.append(destination_path)

    old_resource_response = disk_client.get_resource(unique_folder_path)
    assert old_resource_response.status_code == 404, old_resource_response.text

    new_resource_response = disk_client.get_resource(destination_path)
    assert new_resource_response.status_code == 200, new_resource_response.text

    resource = new_resource_response.json()
    assert resource["type"] == "dir"
    assert resource["path"].endswith(destination_path.removeprefix("app:"))


@pytest.mark.positive
def test_tc006_delete_empty_folder(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
) -> None:
    create_response = disk_client.create_folder(unique_folder_path)
    assert create_response.status_code == 201, create_response.text

    delete_response = disk_client.delete_resource(unique_folder_path)
    assert delete_response.status_code == 204, delete_response.text

    get_response = disk_client.get_resource(unique_folder_path)
    assert get_response.status_code == 404, get_response.text
