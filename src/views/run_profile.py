from customtkinter import CTk, CTkButton, CTkLabel

from src.components.custom_top_level import CustomTopLevel
from src.controllers.timer import Timer
from src.types.speed_operator import SpeedOperator
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions


class RunProfile:
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master)

    def __render(self, master) -> None:
        try:
            assert self.__settings.profiles_manager.is_profile_active()
            window = CustomTopLevel(
                master=master,
                title=f"Uruchomiono: {self.__settings.profiles_manager.active_profile}",
                geometry="300x100"
            )
            UtilityFunctions.center_window(master=window)
            profile_content = self.__settings.profiles_manager.active_profile_content

            self.__settings.suspension.current_profile_speed = profile_content.get("speed")
            self.__settings.suspension.operation(SpeedOperator.INCREMENT)

            label = CTkLabel(master=window)
            label.place(relx=0.025, rely=0)            
            
            timer = Timer(
                master=master,
                start_time=profile_content.get("time"),
                update_time=lambda time: label.configure(text=time),
                on_complete=lambda: self.__settings.close_window_and_reset_speed(window)
            )
            timer.start()

            stop_button = CTkButton(
                master=window,
                text="Zatrzymaj",
                command=lambda: (
                    timer.stop(),
                    self.__settings.close_window_and_reset_speed(window)
                )
            )
            stop_button.place(relx=0.5, rely=0.5, anchor="center")
        except AssertionError:
            pass
