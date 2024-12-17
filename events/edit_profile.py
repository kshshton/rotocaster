from customtkinter import (CTk, CTkButton, CTkEntry, CTkSlider, IntVar,
                           StringVar)

from custom_components.custom_frame import CustomFrame
from custom_components.custom_top_level import CustomTopLevel
from settings import Settings
from utils import Utils


class EditProfile():
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master)

    def __render(self, master: CTk) -> None:
        try:
            assert self.__settings._manager.is_profile_active()
            window = CustomTopLevel(
                master=master,
                title=self.__settings._manager.active_profile
            )
            frame = CustomFrame(master=window)

            self.__speed = IntVar()
            self.__speed_text = StringVar()
            self.__speed.trace_add(
                "write",
                lambda *args: Utils.text_to_speed(
                    text=self.__speed_text,
                    speed=self.__speed,
                )
            )
            self.__speed_text.trace_add(
                "write",
                lambda *args: Utils.slider_validation(
                    input=self.__speed_text,
                    output=self.__speed,
                )
            )
            profile_value = self.__settings._manager.active_profile_value
            self.__settings._damper.current_profile_speed = profile_value

            slider = CTkSlider(master=frame, from_=0, to=100, variable=self.__speed)
            slider.place(relx=0.5, rely=0.5, anchor="center")
            slider.set(profile_value)

            speed_box = CTkEntry(master=frame, textvariable=self.__speed_text)
            speed_box.place(relx=0.5, rely=0.25, anchor="center")

            save_button = CTkButton(
                master=frame,
                text="Zapisz",
                command=lambda: self.__settings._save_button_event(
                    master=window,
                    value=self.__speed.get()
                ),
            )
            save_button.place(relx=0.5, rely=0.8, anchor="center")
        except AssertionError:
            pass
