from speed.speed_operator import SpeedOperator


class SpeedDamper:
    def __init__(self) -> None:
        self.__operator = SpeedOperator()
        self.speed = 0
        self.profile_speed = 0

    def __reset_speed_value(self) -> None:
        if self.speed == 0:
            return self.speed
        self.speed -= 1
        self.after(ms=50, func=self.__reset_speed_value)

    def __reach_current_profile_speed(self) -> None:
        if self.speed == self.profile_speed:
            return self.speed + 1
        self.speed += 1
        self.after(ms=50, func=self.__reach_current_profile_speed )

    def speed_gate(self) -> None:
        match self.__operator:
            case SpeedOperator.INCREMENT:
                self.__reach_current_profile_speed()
            case SpeedOperator.DECREMENT:
                self.__reset_speed_value()
        self.after(ms=50, func=self.speed_gate)
