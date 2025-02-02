from threading import Event, Thread

from customtkinter import CTk

from src.types.axis_direction import AxisDirection


class Engine(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.__wait: int = 0.1
        self.__event = Event()
        self.__stop: bool = False
        self.__thread: Thread = None
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

    def __listen_output(self) -> None:
        while True:
            print({"speed": self.speed, "direction": self.direction})
            self.__event.wait(self.__wait)

    def run(self) -> None:
        thread = Thread(target=self.__listen_output)
        thread.start()

    def __thread_wrapper(self, operation: callable, wait_until_end: bool=False) -> None:
        self.__stop = False
        self.__thread = Thread(target=operation)
        self.__thread.start()
        if wait_until_end:
            self.__thread.join()

    def increment(self, wait_until_end: bool=False) -> None:
        self.__thread_wrapper(
            operation=self.__increment_to_current_profile_value, 
            wait_until_end=wait_until_end
        )

    def decrement(self, wait_until_end: bool=False) -> None:
        self.__thread_wrapper(
            operation=self.__decrement_to_current_profile_value, 
            wait_until_end=wait_until_end
        )
    
    def reset(self, wait_until_end: bool=False) -> None:
        self.__thread_wrapper(
            operation=self.__reset_value, 
            wait_until_end=wait_until_end
        )
