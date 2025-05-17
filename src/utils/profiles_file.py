import json
import os


class ProfilesFile:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.create()

    def create(self) -> None:
        if not os.path.exists(f"data/{self.filename}.json"):
            with open(f"{self.filename}.json", "w") as file:
                json.dump({"profiles": {}}, file, indent=4)

    def load(self) -> dict:
        try:
            with open(f"data/{self.filename}.json", "r") as file:
                return json.load(file)["profiles"]
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def update(self, profiles: dict) -> None:
        with open(f"data/{self.filename}.json", "w") as file:
            content = {"profiles": profiles}
            file.write(json.dumps(obj=content, indent=4))
