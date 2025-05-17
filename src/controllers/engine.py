from threading import Event, Thread

from customtkinter import CTk

from src.types.axis_direction import AxisDirection
from src.utils.utility_functions import UtilityFunctions


class Engine(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.__stop: bool = False
        self.__thread: Thread = None
        self.delay: int = 0.1
        self.event = Event()
        self.current_profile_speed: int = 0
        self.speed: int = 0
        self.direction: str = AxisDirection.LEFT.value

    def __reset_value(self) -> None:
        if self.speed == 0:
            return self.speed
        elif self.speed > 10:
            self.speed -= int(self.speed * 0.1)
        self.speed -= 1
        self.event.wait(self.delay)
        self.__reset_value()

    def __increment_to_current_profile_value(self) -> None:
        if self.speed == self.current_profile_speed or self.__stop:
            return self.speed
        elif self.current_profile_speed - self.speed > self.current_profile_speed // 3:
            self.speed += int(self.current_profile_speed * 0.1)
        else:
            self.speed += 1
        self.event.wait(self.delay)
        self.__increment_to_current_profile_value()

    def __decrement_to_current_profile_value(self) -> None:
        if self.speed == self.current_profile_speed or self.__stop:
            return self.speed
        elif self.speed - self.current_profile_speed > self.current_profile_speed // 3:
            self.speed -= int(self.current_profile_speed * 0.1)
        else:
            self.speed -= 1
        self.event.wait(self.delay)
        self.__decrement_to_current_profile_value()

    def __thread_wrapper(self, operation: callable, wait_until_end: bool = False) -> None:
        self.__thread = Thread(target=operation)
        self.__thread.start()
        if wait_until_end:
            self.__thread.join()

    def __engine_daemon(self) -> None:
        message = None
        while True:
            message = f"engine:{self.direction};{self.speed}"
            print(self.speed)
            UtilityFunctions.send_message_to_board(message)
            self.event.wait(self.delay)

    def increment(self, wait_until_end: bool = False) -> None:
        self.__stop = False
        self.__thread_wrapper(
            operation=self.__increment_to_current_profile_value,
            wait_until_end=wait_until_end
        )

    def decrement(self, wait_until_end: bool = False) -> None:
        self.__stop = False
        self.__thread_wrapper(
            operation=self.__decrement_to_current_profile_value,
            wait_until_end=wait_until_end
        )

    def reset(self, wait_until_end: bool = False) -> None:
        self.__stop = True
        self.__thread_wrapper(
            operation=self.__reset_value,
            wait_until_end=wait_until_end
        )

    def stream_output_to_board(self) -> None:
        self.__thread_wrapper(operation=self.__engine_daemon)

    def close_event(self) -> None:
        self.reset(wait_until_end=True)
        self.event.set()
