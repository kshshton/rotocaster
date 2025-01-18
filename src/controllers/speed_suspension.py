from customtkinter import CTk

from src.types.speed_operator import SpeedOperator


class SpeedSuspension(CTk):
    def __init__(self, refresh_rate: int = 100) -> None:
        super().__init__()
        self.__refresh_rate = refresh_rate
        self.__stop: bool = False
        self.current_profile_speed: int = 0
        self.speed: int = 0

    def __reset_value(self) -> None:
        if self.speed == 0:
            return self.speed
        self.speed -= 1
        self.after(ms=self.__refresh_rate, func=self.__reset_value)

    def __reach_current_profile_value(self) -> None:
        if self.speed == self.current_profile_speed or self.__stop:
            return self.speed
        self.speed += 1
        self.after(ms=self.__refresh_rate, func=self.__reach_current_profile_value)

    def listen_value(self) -> None:
        print(self.speed)
        self.after(ms=self.__refresh_rate, func=self.listen_value)

    def operation(self, operator: SpeedOperator) -> None:
        match operator:
            case SpeedOperator.INCREMENT:
                self.__stop = False
                self.__reach_current_profile_value()
            case SpeedOperator.DECREMENT:
                self.__stop = True
                self.__reset_value()
