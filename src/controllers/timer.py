from datetime import timedelta
from threading import Event, Thread

from customtkinter import CTk


class Timer:
    def __init__(self, master: CTk, start_time: str) -> None:
        hours, minutes, seconds = [int(num) for num in start_time.split(":")]
        self.start_time: timedelta = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)
        self.current_time: timedelta = self.start_time
        self.next: bool = False
        self.__master = master
        self.__event = Event()
        self.update_time: callable = None
        self.on_complete: callable = None

    def __formatted_time(self) -> str:
        total_seconds = int(self.current_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def __time_countdown(self) -> None:
        while self.current_time.total_seconds() > 0:
            if self.update_time:
                self.__master.after(
                    0,
                    self.update_time,
                    self.__formatted_time()
                )
            self.__event.wait(1)
            self.current_time -= timedelta(seconds=1)
        else:
            self.__master.after(0, self.update_time, "Korekcja prędkości...")
            self.__event.wait(1)
            self.__master.after(0, self.on_complete)

    def start(self) -> None:
        thread = Thread(target=self.__time_countdown)
        thread.start()

    def stop(self) -> None:
        self.current_time = timedelta(seconds=0)
