from typing import Optional


class StepsManager:
    def __init__(self):
        self.__steps: dict[str, dict] = {}
        self.__active_step: Optional[str] = None

    def get_active_step(self) -> Optional[str]:
        return self.__active_step

    def set_active_step(self, number: int) -> None:
        self.__active_step = str(number) or None

    def delete_active_step(self) -> None:
        del self.__active_step

    def get_steps(self, profile_name: str) -> dict:
        return self.__steps.get(profile_name, {})

    def update_steps(self, profile_name: str, steps: dict) -> None:
        self.__steps[profile_name] = steps

    def get_active_step_content(self, profile_name: str) -> dict:
        return self.__steps[profile_name][self.__active_step]

    def update_active_step_content(self, profile_name: str, content: dict) -> None:
        assert content["time"] != "0:0:0", "Step should last at least 1 second!"
        self.__steps[profile_name][self.__active_step] = content

    def create_step(self, profile_name: str) -> None:
        steps = self.sequence(profile_name)
        next_number = len(steps) + 1
        self.__active_step = str(next_number)
        self.__steps[profile_name][self.__active_step] = {}

    def is_step_active(self) -> bool:
        return bool(self.__active_step)

    def get_step(self, profile_name: str, step: str) -> dict:
        return self.__steps[profile_name][step]

    def get_active_step_content(self, profile_name: str) -> dict:
        return self.__steps[profile_name][self.__active_step]

    def delete_step(self, profile_name: str, step: str) -> None:
        del self.__steps[profile_name][step]

    def reset_numbers(self, profile_name: str) -> None:
        steps = list(self.__steps[profile_name].values())
        temp_dict = {}

        for index in range(len(steps)):
            temp_dict[str(index + 1)] = steps[index]

        self.__steps[profile_name] = temp_dict

    def select_step(self, step: str) -> None:
        self.__active_step = step

    def sequence(self, profile_name: str) -> list:
        steps = list(self.__steps[profile_name].keys())
        return sorted(steps)

    def last_step_number(self, profile_name: str) -> str:
        steps = self.sequence(profile_name)[::-1]
        last_step = next(iter(steps), "")
        return last_step
