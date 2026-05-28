from disk_client import YandexDiskClient


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


def test_tc003_get_missing_resource(
    disk_client: YandexDiskClient,
    unique_folder_path: str,
) -> None:
    response = disk_client.get_resource(unique_folder_path)

    assert response.status_code == 404, response.text
