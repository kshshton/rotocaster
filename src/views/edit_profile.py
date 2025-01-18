from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkSlider,
                           IntVar, StringVar)

from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.components.time_input import TimeInput
from src.types.axis_direction import AxisDirection
from src.types.profile_struct import ProfileStruct
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class EditProfile():
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__relx: float = 0.5
        self.__rely: float = 0.1
        self.__rely_diff: float = 0.15
        self.__render(master)

    def __render(self, master: CTk) -> None:
        try:
            assert self.__settings.manager.is_profile_active()
            profile_content = self.__settings.manager.active_profile_content
            self.__settings.suspension.__current_profile_speed = profile_content.get("speed", 0)

            window = CustomTopLevel(
                master=master,
                title=f"Profil: {self.__settings.manager.active_profile}",
                geometry="300x300",
            )
            frame = CustomFrame(master=window)

            self.__speed = IntVar()
            self.__speed_text = StringVar()
            self.__speed.trace_add(
                "write",
                lambda *args: UtilityFunctions.text_to_speed(
                    text=self.__speed_text,
                    speed=self.__speed,
                )
            )
            self.__speed_text.trace_add(
                "write",
                lambda *args: UtilityFunctions.slider_validation(
                    input=self.__speed_text,
                    output=self.__speed,
                )
            )

            speed_box = CTkEntry(master=frame, textvariable=self.__speed_text)
            speed_box.place(relx=self.__relx, rely=self.__rely, anchor="center")

            slider = CTkSlider(master=frame, from_=0, to=100, variable=self.__speed)
            slider.place(relx=self.__relx, rely=self.__rely + self.__rely_diff / 1.5, anchor="center")
            slider.set(profile_content.get("speed", 0))

            vertical_position = VerticalPosition(self.__rely, self.__rely_diff)

            time_input = TimeInput(frame)
            time_input.place(
                relx=self.__relx, 
                rely=next(vertical_position),
                anchor="center"
            )
            time_input.update(profile_content.get("time"))

            direction_combobox = CTkComboBox(
                master=frame, 
                values=[AxisDirection.LEFT.value, AxisDirection.RIGHT.value]
            )
            direction_combobox.place(
                relx=self.__relx, 
                rely=next(vertical_position),
                anchor="center"
            )
            direction_combobox.set(profile_content.get("direction"))


            save_button = CTkButton(
                master=frame,
                text="Zapisz",
                command=lambda: self.__settings.save_window_settings(
                    master=window,
                    value=ProfileStruct(
                        speed=self.__speed.get(), 
                        time=str(time_input), 
                        direction=direction_combobox.get(),
                    )
                ),
            )
            save_button.place(
                relx=self.__relx, 
                rely=next(vertical_position),
                anchor="center"
            )
        except AssertionError:
            pass
