from customtkinter import CTk, CTkButton

from custom_components.custom_top_level import CustomTopLevel
from settings import Settings
from speed.speed_operator import SpeedOperator
from utils import Utils


class RunProfile:
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master)

    def __render(self, master) -> None:
        try:
            assert self.__settings._manager.is_profile_active()
            window = CustomTopLevel(
                master=master,
                title=f"Uruchomiono: {self.__settings._manager.active_profile}",
                geometry="300x100"
            )
            Utils.center_window(master=window)
            self.__settings._damper.current_profile_speed = self.__settings._manager.active_profile_value
            self.__settings._damper.speed_operation(SpeedOperator.INCREMENT)
            stop_button = CTkButton(
                master=window,
                text="Zatrzymaj",
                command=lambda:
                    self.__settings._close_window(
                        window=window,
                        callback=self.__settings._damper.speed_operation(SpeedOperator.DECREMENT)
                    ),
            )
            stop_button.place(relx=0.5, rely=0.5, anchor="center")
        except AssertionError:
            pass
