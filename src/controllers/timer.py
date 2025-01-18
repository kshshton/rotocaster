import threading
from datetime import timedelta


class Timer:
    def __init__(
        self,
        master: any,
        start_time: str,
        update_time: callable,
        on_complete: callable
    ) -> None:
        hours, minutes, seconds = [int(num) for num in start_time.split(":")]
        self.start_time: timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.current_time: timedelta = self.start_time
        self.__master = master
        self.__update_time: callable = update_time
        self.__on_complete: callable = on_complete

    def __formatted_time(self) -> str:
        total_seconds = int(self.current_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def __time_countdown(self) -> None:
        while self.current_time.total_seconds() > 0:
            self.current_time -= timedelta(seconds=1)
            if self.__update_time:
                self.__master.after(0, self.__update_time, self.__formatted_time())
            threading.Event().wait(1)
        else:
            self.__master.after(0, self.__on_complete)

    def start(self) -> None:
        if self.current_time.total_seconds() > 0:
            threading.Thread(target=self.__time_countdown, daemon=True).start()

    def stop(self) -> None:
        self.current_time = timedelta(seconds=0)
