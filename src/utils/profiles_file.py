import json
import os


class ProfilesFile:
    def __init__(self, filename: str) -> None:
        self.filename = filename if filename.endswith(".json") else f"{filename}.json"
        self.create()
        
    def create(self) -> None:
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump({"profiles": {}}, file, indent=4)

    def load(self) -> dict:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)["profiles"]
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def update(self, profiles: dict) -> None:
        with open(self.filename, "w") as file:
            content = {"profiles": profiles}
            file.write(json.dumps(obj=content, indent=4))
