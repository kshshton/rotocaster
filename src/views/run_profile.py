from customtkinter import CTk, CTkButton, CTkLabel

from src.components.custom_top_level import CustomTopLevel
from src.controllers.queue import Queue
from src.controllers.timer import Timer
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions


class RunProfile:
    def __init__(self, master: CTk, context: Context) -> None:
        self.__master = master
        self.__context = context
        self.__window = None
        self.__queue = Queue(
            master=self.__master,
            context=self.__context
        )
        self.__timer = next(self.__queue)
        self.__timer.on_complete = lambda: self.__on_complete()
        self.__render(self.__master, timer=self.__timer)
        self.__sound: bool = True

    def __turn_off_sound_effect(self) -> None:
        self.__sound = False

    def __on_complete(self):
        try:
            timer = next(self.__queue)
            timer.on_complete = lambda: self.__on_complete()
            self.__render(self.__master, timer=timer)
        except:
            self.__context.close_window_and_reset_speed(master=self.__window)
            if self.__sound:
                UtilityFunctions.sound_effect()

    def __render(self, master, timer: Timer) -> None:
        if self.__window:
            UtilityFunctions.close_window(master=self.__window)

        self.__window = CustomTopLevel(
            master=master,
            title=f"Uruchomiono: {self.__context.profiles_manager.get_active_profile_name()}",
            geometry="300x100",
            close_window_button_blocked=True
        )
        UtilityFunctions.center_window(master=self.__window)

        time_label = CTkLabel(master=self.__window, width=270)
        time_label.place(relx=0.025, rely=0)

        stop_button = CTkButton(
            master=self.__window,
            text="Zatrzymaj",
            command=lambda: (
                timer.stop(),
                self.__queue.stop(),
                self.__context.close_window_and_reset_speed(self.__window),
                self.__turn_off_sound_effect(),
            )
        )
        stop_button.place(relx=0.5, rely=0.5, anchor="center")

        timer.update_time = lambda time: time_label.configure(text=time)
        timer.start()
