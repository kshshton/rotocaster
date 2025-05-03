from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkLabel,
                           CTkSlider, IntVar, StringVar)

from src.components.custom_combobox import CustomComboBox
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.components.time_input import TimeInput
from src.types.axis_direction import AxisDirection
from src.types.profile_struct import ProfileStruct
from src.types.step_struct import StepStruct
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class AddStep:
    def __init__(self, master: CTk, settings: Settings, combobox: CustomComboBox) -> None:
        self.__settings = settings
        self.__relx: float = 0.5
        self.__rely: float = 0.1
        self.__rely_padding: float = 0.18
        self.__render(master, combobox)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        active_profile = self.__settings.profiles_manager.get_active_profile_name()
        new_step_number = str(
            int(self.__settings.steps_manager.last_step() or 0) + 1
        )
        combobox.configure(
            values=self.__settings.steps_manager.list_steps())
        combobox.set(new_step_number)
        vertical_position = VerticalPosition(self.__rely, self.__rely_padding)

        window = CustomTopLevel(
            master=master,
            title=f"Profil: {active_profile} - Krok: {new_step_number}",
            geometry="320x300",
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

        speed_label = CTkLabel(master=frame, text="Prędkość: ")
        speed_label.place(relx=self.__relx / 4,
                          rely=self.__rely, anchor="center")

        speed_box = CTkEntry(master=frame, textvariable=self.__speed_text)
        speed_box.place(relx=self.__relx, rely=self.__rely, anchor="center")

        slider = CTkSlider(master=frame, from_=0,
                           to=100, variable=self.__speed)
        slider.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        time_input = TimeInput(frame)
        time_input.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        direction_position = next(vertical_position)

        direction_label = CTkLabel(master=frame, text="Kierunek:")
        direction_label.place(relx=self.__relx / 4,
                              rely=direction_position, anchor="center")

        direction_combobox = CTkComboBox(
            master=frame,
            values=[AxisDirection.LEFT.value, AxisDirection.RIGHT.value]
        )
        direction_combobox.place(
            relx=self.__relx, rely=direction_position, anchor="center")

        save_button = CTkButton(
            master=frame,
            text="Zapisz",
            command=lambda: (
                self.__settings.steps_manager.create_step(new_step_number),
                self.__settings.steps_manager.set_step_content(
                    step_number=new_step_number,
                    step=StepStruct(
                        speed=self.__speed.get(),
                        time=str(time_input),
                        direction=direction_combobox.get(),
                    ).to_dict()
                ),
                self.__settings.steps_manager.set_active_step_number(
                    new_step_number),
                self.__settings.save_profile_settings(
                    ProfileStruct(
                        self.__settings.steps_manager.get_steps()
                    ).to_dict()
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")
