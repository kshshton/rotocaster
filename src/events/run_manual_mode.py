from customtkinter import (CTk, CTkButton, CTkEntry, CTkLabel, CTkSlider,
                           IntVar, StringVar)

from src.custom_components.custom_frame import CustomFrame
from src.custom_components.custom_top_level import CustomTopLevel
from src.types.speed_operator import SpeedOperator
from src.utils.settings import Settings
from src.utils.timer import Timer
from src.utils.utility_functions import UtilityFunctions


class RunManualMode:
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master)

    def __manual_to_output_speed(self, *args: any) -> None:
        self.__settings._damper.actual_speed = self.__manual_speed.get()
    
    def __render(self, master) -> None:
        window = CustomTopLevel(
            master=master,
            title="Uruchomiono: tryb ręczny",
        )
        frame = CustomFrame(master=window)

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

        label = CTkLabel(master=frame)
        label.place(relx=0.025, rely=0)

        timer = Timer(callback=lambda time: label.configure(text=time))
        timer.start()

        slider = CTkSlider(master=frame, from_=0, to=100, variable=self.__manual_speed)
        slider.place(relx=0.5, rely=0.5, anchor="center")

        speed_box = CTkEntry(master=frame, textvariable=self.__manual_speed_text)
        speed_box.place(relx=0.5, rely=0.25, anchor="center")

        stop_button = CTkButton(
            master=frame,
            text="Zatrzymaj",
            command=lambda: (
                timer.stop(),
                self.__settings._close_window(
                    window=window,
                    callback=self.__settings._damper \
                        .speed_operation(SpeedOperator.DECREMENT)
                ),
            )
        )
        stop_button.place(relx=0.5, rely=0.8, anchor="center")

        self.__settings._damper.actual_speed = self.__manual_speed.get()        
