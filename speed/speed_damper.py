import time

from customtkinter import CTk

from speed.speed_operator import SpeedOperator


class SpeedDamper(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.actual_speed: int = 0
        self.current_profile_speed: int = 0

    def __reset_speed_value(self) -> None:
        if self.actual_speed == 0:
            return self.actual_speed
        self.actual_speed -= 1
        self.after(ms=100, func=self.__reset_speed_value)

    def __reach_current_profile_speed(self) -> None:
        if self.actual_speed == self.current_profile_speed:
            return self.actual_speed
        self.actual_speed += 1
        self.after(ms=100, func=self.__reach_current_profile_speed)

    def _listen_output_speed(self) -> None:
        print(self.actual_speed)
        self.after(ms=100, func=self._listen_output_speed)

    def speed_operation(self, operator: SpeedOperator) -> None:
        match operator:
            case SpeedOperator.INCREMENT:
                self.__reach_current_profile_speed()
            case SpeedOperator.DECREMENT:
                self.__reset_speed_value()
