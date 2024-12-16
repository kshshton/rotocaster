import json
import os


class ProfilesFile:
    def __init__(self, filename: str) -> None:
        self.filename = filename if filename.endswith(".json") else f"{filename}.json"
        
    def create(self) -> None:
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                data = {}
                json.dump(data, file, indent=4)

    def load(self) -> None:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def update(self) -> None:
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.__profiles, indent=4))
