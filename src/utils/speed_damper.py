from customtkinter import CTk

from src.types.speed_operator import SpeedOperator


class SpeedDamper(CTk):
    def __init__(self, refresh_rate: int = 100) -> None:
        super().__init__()
        self.__refresh_rate = refresh_rate
        self.actual_speed: int = 0
        self.current_profile_speed: int = 0

    def __reset_speed_value(self) -> None:
        if self.actual_speed == 0:
            return self.actual_speed
        self.actual_speed -= 1
        self.after(ms=self.__refresh_rate, func=self.__reset_speed_value)

    def __reach_current_profile_speed(self) -> None:
        if self.actual_speed == self.current_profile_speed:
            return self.actual_speed
        self.actual_speed += 1
        self.after(ms=self.__refresh_rate, func=self.__reach_current_profile_speed)

    def _listen_speed_value(self) -> None:
        print(self.actual_speed)
        self.after(ms=self.__refresh_rate, func=self._listen_speed_value)

    def speed_operation(self, operator: SpeedOperator) -> None:
        match operator:
            case SpeedOperator.INCREMENT:
                self.__reach_current_profile_speed()
            case SpeedOperator.DECREMENT:
                self.__reset_speed_value()
