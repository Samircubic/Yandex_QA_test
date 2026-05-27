import requests


class YandexDiskClient:
    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, token: str, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"OAuth {token}"})

    def create_folder(self, path: str) -> requests.Response:
        return self.session.put(
            f"{self.BASE_URL}/resources",
            params={"path": path},
            timeout=self.timeout,
        )

    def get_resource(self, path: str) -> requests.Response:
        return self.session.get(
            f"{self.BASE_URL}/resources",
            params={"path": path},
            timeout=self.timeout,
        )

    def move_resource(
        self,
        source_path: str,
        destination_path: str,
        *,
        overwrite: bool = False,
        force_async: bool = False,
    ) -> requests.Response:
        return self.session.post(
            f"{self.BASE_URL}/resources/move",
            params={
                "from": source_path,
                "path": destination_path,
                "overwrite": str(overwrite).lower(),
                "force_async": str(force_async).lower(),
            },
            timeout=self.timeout,
        )

    def delete_resource(self, path: str) -> requests.Response:
        return self.session.delete(
            f"{self.BASE_URL}/resources",
            params={"path": path},
            timeout=self.timeout,
        )

    def get_operation_status(self, operation_url: str) -> requests.Response:
        return self.session.get(operation_url, timeout=self.timeout)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "YandexDiskClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
