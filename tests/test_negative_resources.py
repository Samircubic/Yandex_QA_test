import pytest

from disk_client import YandexDiskClient


@pytest.mark.negative
def test_tc003_get_missing_resource(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
) -> None:
    response = disk_client.get_resource(unique_folder_path)

    assert response.status_code == 404, response.text


@pytest.mark.negative
def test_tc005_move_missing_resource(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
) -> None:
    destination_path = f"{unique_folder_path}_moved"

    response = disk_client.move_resource(unique_folder_path, destination_path)

    assert response.status_code == 404, response.text


@pytest.mark.negative
def test_tc007_delete_missing_resource(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
) -> None:
    response = disk_client.delete_resource(unique_folder_path)

    assert response.status_code == 404, response.text


@pytest.mark.negative
def test_tc010_move_to_existing_folder_conflict(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    source_path = f"{unique_folder_path}_source"
    target_path = f"{unique_folder_path}_target"

    create_source_response = disk_client.create_folder(source_path)
    assert create_source_response.status_code == 201, create_source_response.text
    created_paths.append(source_path)

    create_target_response = disk_client.create_folder(target_path)
    assert create_target_response.status_code == 201, create_target_response.text
    created_paths.append(target_path)

    move_response = disk_client.move_resource(
        source_path,
        target_path,
        overwrite=False,
    )
    assert move_response.status_code == 409, move_response.text

    source_response = disk_client.get_resource(source_path)
    assert source_response.status_code == 200, source_response.text
    assert source_response.json()["type"] == "dir"

    target_response = disk_client.get_resource(target_path)
    assert target_response.status_code == 200, target_response.text
    assert target_response.json()["type"] == "dir"
