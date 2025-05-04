from customtkinter import CTk, CTkButton, CTkEntry, CTkLabel

from src.components.custom_combobox import CustomComboBox
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.types.profile_struct import ProfileStruct
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class AddProfile:
    def __init__(self, master: CTk, combobox: CustomComboBox, context: Context) -> None:
        self.__context = context
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.275
        self.__render(master, combobox)

    def __add_profile(self, profile_name: str, combobox: CustomComboBox) -> None:
        assert profile_name != "", "Profile can't be empty!"
        self.__context.profiles_manager.create_profile(profile_name)
        self.__context.profiles_manager.set_active_profile_name(profile_name)
        combobox.configure(
            values=self.__context.profiles_manager.list_profiles())
        combobox.set(profile_name)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        window = CustomTopLevel(
            master=master,
            title=f"Dodaj profil",
            geometry="200x200",
        )
        frame = CustomFrame(master=window)
        vertical_position = VerticalPosition(self.__rely, self.__rely_padding)

        speed_label = CTkLabel(master=frame, text="Nazwa profilu:")
        speed_label.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        entry_box = CTkEntry(master=frame)
        entry_box.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        save_button = CTkButton(
            master=frame,
            text="Zapisz",
            command=lambda: (
                self.__add_profile(
                    profile_name=entry_box.get(),
                    combobox=combobox,
                ),
                self.__context.save_profile_context(
                    ProfileStruct(
                        self.__context.steps_manager.get_steps()
                    ).to_dict()
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")
