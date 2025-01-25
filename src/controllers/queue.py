from customtkinter import CTk

from src.controllers.timer import Timer
from src.types.speed_operator import SpeedOperator
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

    def __next__(self):
        step = next(self.__steps)
        self.__settings.engine.current_profile_speed = step["speed"]
        self.__settings.engine.update_direction(direction=step["direction"])
        self.__settings.engine.operation(SpeedOperator.INCREMENT)
        return Timer(
            master=self.__master,
            start_time=step["time"],
        )

    def stop(self):
        self.__steps = None
