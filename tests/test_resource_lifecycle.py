import pytest

from disk_client import YandexDiskClient
from conftest import wait_operation_success


@pytest.mark.scenario
def test_tc008_resource_lifecycle(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    moved_path = f"{unique_folder_path}_moved"

    create_response = disk_client.create_folder(unique_folder_path)
    assert create_response.status_code == 201, create_response.text
    created_paths.append(unique_folder_path)

    get_created_response = disk_client.get_resource(unique_folder_path)
    assert get_created_response.status_code == 200, get_created_response.text

    move_response = disk_client.move_resource(unique_folder_path, moved_path)
    assert move_response.status_code == 201, move_response.text
    created_paths.remove(unique_folder_path)
    created_paths.append(moved_path)

    get_old_response = disk_client.get_resource(unique_folder_path)
    assert get_old_response.status_code == 404, get_old_response.text

    get_moved_response = disk_client.get_resource(moved_path)
    assert get_moved_response.status_code == 200, get_moved_response.text

    delete_response = disk_client.delete_resource(moved_path)
    assert delete_response.status_code == 204, delete_response.text
    created_paths.remove(moved_path)

    get_deleted_response = disk_client.get_resource(moved_path)
    assert get_deleted_response.status_code == 404, get_deleted_response.text


@pytest.mark.scenario
def test_tc009_move_non_empty_folder(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    child_path = f"{unique_folder_path}/child"
    destination_path = f"{unique_folder_path}_moved"

    create_parent_response = disk_client.create_folder(unique_folder_path)
    assert create_parent_response.status_code == 201, create_parent_response.text
    created_paths.append(unique_folder_path)

    create_child_response = disk_client.create_folder(child_path)
    assert create_child_response.status_code == 201, create_child_response.text

    move_response = disk_client.move_resource(
        unique_folder_path,
        destination_path,
        force_async=True,
    )
    assert move_response.status_code in (201, 202), move_response.text

    if move_response.status_code == 202:
        operation_url = move_response.json()["href"]
        operation_status = wait_operation_success(disk_client, operation_url)
        assert operation_status == "success"

    created_paths.append(destination_path)
    created_paths.remove(unique_folder_path)

    old_resource_response = disk_client.get_resource(unique_folder_path)
    assert old_resource_response.status_code == 404, old_resource_response.text

    new_resource_response = disk_client.get_resource(destination_path)
    assert new_resource_response.status_code == 200, new_resource_response.text

    child_resource_response = disk_client.get_resource(f"{destination_path}/child")
    assert child_resource_response.status_code == 200, child_resource_response.text


@pytest.mark.scenario
def test_tc011_repeated_resource_lifecycle(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
    created_paths: list[str],
) -> None:
    for index in range(2):
        source_path = f"{unique_folder_path}_repeat_{index}"
        moved_path = f"{source_path}_moved"

        create_response = disk_client.create_folder(source_path)
        assert create_response.status_code == 201, create_response.text
        created_paths.append(source_path)

        get_created_response = disk_client.get_resource(source_path)
        assert get_created_response.status_code == 200, get_created_response.text
        assert get_created_response.json()["type"] == "dir"

        move_response = disk_client.move_resource(source_path, moved_path)
        assert move_response.status_code == 201, move_response.text
        created_paths.remove(source_path)
        created_paths.append(moved_path)

        get_old_response = disk_client.get_resource(source_path)
        assert get_old_response.status_code == 404, get_old_response.text

        get_moved_response = disk_client.get_resource(moved_path)
        assert get_moved_response.status_code == 200, get_moved_response.text
        assert get_moved_response.json()["type"] == "dir"

        delete_response = disk_client.delete_resource(moved_path)
        assert delete_response.status_code == 204, delete_response.text
        created_paths.remove(moved_path)

        get_deleted_response = disk_client.get_resource(moved_path)
        assert get_deleted_response.status_code == 404, get_deleted_response.text
