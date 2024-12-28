from customtkinter import CTk, CTkButton

from src.components.custom_top_level import CustomTopLevel
from src.types.speed_operator import SpeedOperator
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions


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
            UtilityFunctions.center_window(master=window)
            self.__settings._damper.current_profile_speed = self.__settings._manager.active_profile_content
            self.__settings._damper.speed_operation(SpeedOperator.INCREMENT)
            stop_button = CTkButton(
                master=window,
                text="Zatrzymaj",
                command=lambda: self.__settings.close_window(window=window),
            )
            stop_button.place(relx=0.5, rely=0.5, anchor="center")
        except AssertionError:
            pass
