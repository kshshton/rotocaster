from customtkinter import CTk

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
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__relx: float = 0.5
        self.__rely: float = 0.1
        self.__rely_padding: float = 0.2
        self.__render(master)

    def __render(self, master: CTk) -> None:
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
            geometry="320x300",
        )
        frame = CustomFrame(master=window)

        combobox = CustomComboBox(
            master=frame,
            state="readonly",
            values=self.__settings.steps_manager.sequence(profile_name=active_profile),
            content=self.__settings.steps_manager.first_step(profile_name=active_profile),
            callback=self.__settings.steps_manager.select_step,
        )
        combobox.place(relx=self.__relx, rely=self.__rely, anchor="center")

        edit_button = CustomButton(
            master=frame,
            text="Edytuj",
            callback=lambda: EditStep(master=window, settings=self.__settings),
        )
        edit_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        add_button = CustomButton(
            master=frame,
            text="Dodaj",
            callback=lambda: AddStep(master=window, settings=self.__settings, combobox=combobox),
        )
        add_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        delete_button = CustomButton(
            master=frame,
            text="Usuń",
            callback=lambda: DeleteStep(settings=self.__settings, combobox=combobox),
        )
        delete_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        save_button = CustomButton(
            master=frame,
            text="Zapisz",
            callback=lambda: (
                self.__settings.save_profile_settings(
                    ProfileStruct(
                        speed=active_profile_content["speed"],
                        time=active_profile_content["time"],
                        direction=active_profile_content["direction"],
                        steps=self.__settings.steps_manager.get_steps(profile_name=active_profile),
                    )
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")
