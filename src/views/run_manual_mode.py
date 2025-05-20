from customtkinter import (CTk, CTkButton, CTkEntry, CTkLabel, CTkSlider,
                           IntVar, StringVar)

from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.controllers.stopwatch import Stopwatch
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class RunManualMode:
    def __init__(self, master: CTk, context: Context) -> None:
        self.__context = context
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.21
        self.__render(master)

    def __manual_to_output_speed(self, *args: any) -> None:
        self.__context.engine.speed = self.__manual_speed.get()

    def __render(self, master) -> None:
        window = CustomTopLevel(
            master=master,
            title="Uruchomiono: tryb ręczny",
            geometry="320x240",
            close_window_button_blocked=True
        )
        frame = CustomFrame(master=window)
        vertical_position = VerticalPosition(self.__rely, self.__rely_padding)

        self.__manual_speed = IntVar()
        self.__manual_speed_text = StringVar()
        self.__manual_speed.trace_add(
            "write",
            lambda *args: UtilityFunctions.text_to_speed(
                text=self.__manual_speed_text,
                speed=self.__manual_speed,
            )
        )
        self.__manual_speed_text.trace_add(
            "write",
            lambda *args: UtilityFunctions.slider_validation(
                input=self.__manual_speed_text,
                output=self.__manual_speed,
            )
        )
        self.__manual_speed.trace_add("write", self.__manual_to_output_speed)
        self.__manual_speed.set(0)

        time_label = CTkLabel(master=frame)
        time_label.place(relx=0.025, rely=0)

        timer = Stopwatch(
            callback=lambda time: time_label.configure(text=time))
        timer.start()

        speed_position = next(vertical_position)

        speed_label = CTkLabel(master=frame, text="Prędkość:")
        speed_label.place(relx=self.__relx / 4,
                          rely=speed_position, anchor="center")

        speed_box = CTkEntry(
            master=frame, textvariable=self.__manual_speed_text)
        speed_box.place(relx=self.__relx, rely=speed_position, anchor="center")

        slider = CTkSlider(master=frame, from_=0, to=100,
                           variable=self.__manual_speed)
        slider.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        stop_button = CTkButton(
            master=frame,
            text="Zatrzymaj",
            command=lambda: (
                timer.stop(),
                self.__context.engine.reset(wait_until_end=True),
                UtilityFunctions.close_window(window),
            )
        )
        stop_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        self.__context.engine.speed = self.__manual_speed.get()
