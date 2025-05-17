from typing import Optional, Union


class StepsManager:
    def __init__(self):
        self.__steps: dict[dict] = {}
        self.__active_step_number: Optional[str] = None

    def get_active_step_number(self) -> Optional[str]:
        return self.__active_step_number

    def set_active_step_number(self, number: Optional[Union[int, str]]) -> None:
        self.__active_step_number = str(number) or None

    def delete_active_step(self) -> None:
        del self.__steps[self.__active_step_number]

    def get_steps(self) -> dict:
        return self.__steps

    def set_steps(self, profile_steps: dict) -> None:
        """
        Example: {'1': {'speed': 46, 'time': '0:0:5', 'direction': 'LEWO'}, '2': {'speed': 62, 'time': '0:0:5', 'direction': 'PRAWO'}}
        """
        self.__steps = profile_steps or {}

    def get_step_content(self, step_number: Union[str, int]) -> dict:
        return self.__steps[str(step_number)]

    def set_step_content(self, step_number: Union[str, int], step: dict) -> None:
        assert step["time"] != "0:0:0", "Step should last at least 1 second!"
        self.__steps[str(step_number)] = step

    def get_active_step_content(self) -> dict:
        return self.__steps[self.__active_step_number]

    def set_active_step_content(self, step: dict) -> None:
        assert step["time"] != "0:0:0", "Step should last at least 1 second!"
        self.__steps[self.__active_step_number] = step

    def is_step_active(self) -> bool:
        return bool(self.__active_step_number)

    def create_step(self, step_number: Union[str, int]) -> None:
        self.__steps[str(step_number)] = {}

    def delete_step(self, step: str) -> None:
        del self.__steps[step]

    def reset_numbers(self) -> None:
        steps = list(self.__steps.values())
        temp_dict = {}

        for index in range(len(steps)):
            temp_dict[str(index + 1)] = steps[index]

        self.__steps = temp_dict

    def list_steps(self) -> list:
        steps = (int(key) for key in self.__steps.keys())
        steps = sorted(steps)
        return [str(step) for step in steps]

    def last_step(self) -> Optional[str]:
        try:
            steps = list(self.__steps.keys())
            return steps[-1]
        except:
            return None
