from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkLabel,
                           CTkSlider, IntVar, StringVar)

from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.components.time_input import TimeInput
from src.types.axis_direction import AxisDirection
from src.types.profile_struct import ProfileStruct
from src.types.step_struct import StepStruct
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class EditStep:
    def __init__(self, master: CTk, context: Context) -> None:
        self.__context = context
        self.__relx: float = 0.5
        self.__rely: float = 0.1
        self.__rely_padding: float = 0.2
        self.__render(master)

    def __render(self, master: CTk) -> None:
        assert self.__context.steps_manager.is_step_active(), "There are no steps to edit!"
        active_profile = self.__context.profiles_manager.get_active_profile_name()
        active_step = self.__context.steps_manager.get_active_step_number()
        step_content = self.__context.steps_manager.get_active_step_content()
        self.__context.engine.current_profile_speed = step_content.get(
            "speed", 0)
        vertical_position = VerticalPosition(
            self.__rely, self.__rely_padding)

        window = CustomTopLevel(
            master=master,
            title=f"Profil: {active_profile} - Krok: {active_step}",
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
        speed_box.place(relx=self.__relx,
                        rely=self.__rely, anchor="center")

        slider = CTkSlider(master=frame, from_=0,
                           to=100, variable=self.__speed)
        slider.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")
        slider.set(step_content.get("speed", 0))

        time_input = TimeInput(frame)
        time_input.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")
        time_input.update(step_content.get("time"))

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
        direction_combobox.set(step_content.get("direction"))

        save_button = CTkButton(
            master=frame,
            text="Zapisz",
            command=lambda: (
                self.__context.steps_manager.set_active_step_content(
                    step=StepStruct(
                        speed=self.__speed.get(),
                        time=str(time_input),
                        direction=direction_combobox.get(),
                    ).to_dict()
                ),
                self.__context.save_profile_to_file(
                    ProfileStruct(
                        self.__context.steps_manager.get_steps()
                    ).to_dict()
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")
