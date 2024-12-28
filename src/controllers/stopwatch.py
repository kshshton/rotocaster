import threading
from datetime import timedelta


class Stopwatch:
    def __init__(self, callback=None) -> None:
        self.seconds: int = 0
        self.time: str = "00:00:00"
        self.running: bool = False
        self.callback: callable = callback # For widget update

    def start(self) -> None:
        if not self.running:
            self.running = True
            threading.Thread(target=self.__measure_time, daemon=True).start()

    def stop(self) -> None:
        self.running = False

    def __measure_time(self) -> None:
        while self.running:
            self.seconds += 1
            self.time = str(timedelta(seconds=self.seconds))
            if self.callback:
                self.callback(self.time)
            threading.Event().wait(1)
