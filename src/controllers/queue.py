from customtkinter import CTk

from src.controllers.timer import Timer
from src.utils.context import Context


class Queue:
    def __init__(self, master: CTk, context: Context):
        self.__master = master
        self.__context = context
        self.__active_profile_steps = self.__context.profiles_manager.get_active_profile_steps()
        self.__steps = iter(self.__active_profile_steps.values())
        self.__previous_speed: int = 0
        self.__previous_direction: str = None

    def __next__(self):
        step = next(self.__steps)
        self.__context.engine.current_profile_speed = step["speed"]

        if self.__previous_direction and self.__previous_direction != step["direction"]:
            self.__context.engine.reset(wait_until_end=True)
            self.__previous_speed = 0

        self.__context.engine.direction = step["direction"]

        if self.__previous_speed > self.__context.engine.current_profile_speed:
            self.__context.engine.decrement(wait_until_end=True)
        else:
            self.__context.engine.increment(wait_until_end=True)

        self.__previous_speed = step["speed"]
        self.__previous_direction = step["direction"]

        return Timer(
            master=self.__master,
            start_time=step["time"],
        )

    def stop(self):
        self.__steps = None
