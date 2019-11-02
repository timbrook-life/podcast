import yaml
from dataclasses import dataclass


@dataclass(frozen=True)
class DBConnection:
    host: str
    port: int
    username: str
    password: str


class DynamicConfig:
    def __init__(self):
        with open("./config.yaml") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def db_connection(self) -> DBConnection:
        # Reload every fetch... for now
        with open("./config.yaml") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)
        return DBConnection(
            host=self.data["db"]["host"],
            port=self.data["db"]["port"],
            username=self.data["db"]["username"],
            password=self.data["db"]["password"],
        )

