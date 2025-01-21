from customtkinter import CTk, CTkEntry, CTkLabel

from src.components.custom_button import CustomButton
from src.components.custom_combobox import CustomComboBox
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.types.profile_struct import ProfileStruct
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition
from src.views.add_step import AddStep
from src.views.delete_step import DeleteStep
from src.views.edit_step import EditStep


class ManageSteps:
    def __init__(self, master: CTk, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.15
        self.__render(master, combobox)

    def __update_profile_name(self, entry_box_value: str, combobox: CustomComboBox):
        active_profile = self.__settings.profiles_manager.active_profile
        if entry_box_value != active_profile and entry_box_value != "":
            self.__settings.profiles_manager.rename_profile(
                original_name=active_profile,
                new_name=entry_box_value,
            )
            self.__settings.profiles_manager.active_profile = entry_box_value
            combobox.configure(values=self.__settings.profiles_manager.list_profiles())
            combobox.set(entry_box_value)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        active_profile = self.__settings.profiles_manager.active_profile
        active_profile_content = self.__settings.profiles_manager.active_profile_content
        self.__settings.steps_manager.update_steps(
            profile_name=active_profile,
            steps=active_profile_content.get("steps", {})
        )
        vertical_position = VerticalPosition(self.__rely, self.__rely_padding)

        window = CustomTopLevel(
            master=master,
            title=f"Profil: {active_profile} - Kroki",
            geometry="360x340",
        )
        frame = CustomFrame(master=window)

        profile_position = next(vertical_position)

        profile_label = CTkLabel(master=frame, text="Nazwa profilu:")
        profile_label.place(relx=self.__relx / 4, rely=profile_position, anchor="center")

        profile_entry_box = CTkEntry(master=frame, placeholder_text=active_profile)
        profile_entry_box.place(relx=self.__relx, rely=profile_position, anchor="center")

        steps_position = next(vertical_position)

        steps_label = CTkLabel(master=frame, text="Krok:")
        steps_label.place(relx=self.__relx / 4, rely=steps_position, anchor="center")

        steps_combobox = CustomComboBox(
            master=frame,
            state="readonly",
            values=self.__settings.steps_manager.sequence(profile_name=active_profile),
            content=self.__settings.steps_manager.first_step(profile_name=active_profile),
            callback=self.__settings.steps_manager.select_step,
        )
        steps_combobox.place(relx=self.__relx, rely=steps_position, anchor="center")

        edit_button = CustomButton(
            master=frame,
            text="Edytuj",
            callback=lambda: EditStep(master=window, settings=self.__settings),
        )
        edit_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        add_button = CustomButton(
            master=frame,
            text="Dodaj",
            callback=lambda: AddStep(master=window, settings=self.__settings, combobox=steps_combobox),
        )
        add_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        delete_button = CustomButton(
            master=frame,
            text="Usuń",
            callback=lambda: DeleteStep(settings=self.__settings, combobox=steps_combobox),
        )
        delete_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        save_button = CustomButton(
            master=frame,
            text="Zapisz",
            callback=lambda: (
                self.__update_profile_name(entry_box_value=profile_entry_box.get(), combobox=combobox),
                self.__settings.save_profile_settings(
                    ProfileStruct(
                        steps=self.__settings.steps_manager.get_steps(profile_name=active_profile),
                    )
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")
