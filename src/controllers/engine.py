from threading import Event, Thread

from customtkinter import CTk

from src.types.axis_direction import AxisDirection
from src.types.speed_operator import SpeedOperator


class Engine(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.__wait: int = 0.1
        self.__event = Event()
        self.__stop: bool = False
        self.current_profile_speed: int = 0
        self.speed: int = 0
        self.direction: str = AxisDirection.LEFT.value

    def __reset_value(self) -> None:
        if self.speed == 0:
            return self.speed
        self.speed -= 1
        self.__event.wait(self.__wait)
        self.__reset_value()

    def __increment_to_current_profile_value(self) -> None:
        if self.speed == self.current_profile_speed or self.__stop:
            return self.speed
        self.speed += 1
        self.__event.wait(self.__wait)
        self.__increment_to_current_profile_value()

    def __decrement_to_current_profile_value(self) -> None:
        if self.speed == self.current_profile_speed or self.__stop:
            return self.speed
        self.speed -= 1
        self.__event.wait(self.__wait)
        self.__decrement_to_current_profile_value()

    def listen_output(self) -> None:
        while True:
            print({"speed": self.speed, "direction": self.direction})
            self.__event.wait(self.__wait)

    def run(self) -> None:
        thread = Thread(target=self.listen_output)
        thread.start()

    def update_direction(self, direction: str):
        self.direction = direction

    def operation(self, operator: SpeedOperator) -> None:
        thread = None
        match operator:
            case SpeedOperator.INCREMENT:
                self.__stop = False
                thread = Thread(target=self.__increment_to_current_profile_value)
                thread.start()
            case SpeedOperator.DECREMENT:
                self.__stop = False
                thread = Thread(target=self.__decrement_to_current_profile_value)
                thread.start()
            case SpeedOperator.RESET:
                self.__stop = True
                thread = Thread(target=self.__reset_value)
                thread.start()
