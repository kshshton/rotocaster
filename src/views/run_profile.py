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
            active_profile = self.__settings.profiles_manager.active_profile
            active_profile_steps = self.__settings.profiles_manager.active_profile_steps
            self.__settings.steps_manager.update_steps(profile_name=active_profile, steps=active_profile_steps)
            
            for step_number, step_content in active_profile_steps.items():
                self.__settings.engine.current_profile_speed = step_content.get("speed")
                self.__settings.engine.update_direction(direction=step_content.get("direction"))
                self.__settings.engine.operation(SpeedOperator.INCREMENT)
                last_step_number = self.__settings.steps_manager.last_step_number(profile_name=active_profile)

                time_label = CTkLabel(master=window)
                time_label.place(relx=0.025, rely=0)            

                timer = Timer(
                    master=master,
                    start_time=step_content.get("time"),
                    update_time=lambda time: time_label.configure(text=time),
                    on_complete=lambda: (
                        self.__settings.close_window_and_reset_speed(window) if step_number == last_step_number else None
                    )
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
