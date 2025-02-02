from customtkinter import CTk

from src.controllers.timer import Timer
from src.utils.settings import Settings


class Queue:
    def __init__(self, master: CTk, settings: Settings):
        self.__master = master
        self.__settings = settings
        self.__active_profile = self.__settings.profiles_manager.active_profile
        self.__active_profile_steps = self.__settings.profiles_manager.active_profile_steps
        self.__settings.steps_manager.update_steps(
            profile_name=self.__active_profile, 
            steps=self.__active_profile_steps
        )
        self.__steps = iter(self.__active_profile_steps.values())
        self.__previous_speed: int = 0
        self.__previous_direction: str = None

    def __next__(self):
        step = next(self.__steps)
        self.__settings.engine.current_profile_speed = step["speed"]

        if self.__previous_direction and self.__previous_direction != step["direction"]:
            self.__settings.engine.reset(wait_until_end=True)
            self.__previous_speed = 0

        self.__settings.engine.direction = step["direction"]

        if self.__previous_speed > self.__settings.engine.current_profile_speed:
            self.__settings.engine.decrement(wait_until_end=True)
        else:
            self.__settings.engine.increment(wait_until_end=True)

        self.__previous_speed = step["speed"]
        self.__previous_direction = step["direction"]

        return Timer(
            master=self.__master,
            start_time=step["time"],
        )

    def stop(self):
        self.__steps = None
