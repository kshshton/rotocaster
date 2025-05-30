from customtkinter import CTk, CTkEntry, CTkLabel

from src.components.custom_button import CustomButton
from src.components.custom_combobox import CustomComboBox
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.types.profile_struct import ProfileStruct
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition
from src.views.add_step import AddStep
from src.views.delete_step import DeleteStep
from src.views.edit_step import EditStep


class EditProfile:
    def __init__(self, master: CTk, combobox: CustomComboBox, context: Context) -> None:
        self.__context = context
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.15
        self.__render(master, combobox)

    def __update_profile_name(self, entry_box_value: str, combobox: CustomComboBox):
        if entry_box_value == "":
            return
        active_profile = self.__context.profiles_manager.get_active_profile_name()
        profiles = self.__context.profiles_manager.list_profiles()
        assert entry_box_value != active_profile, "Profile name is the same!"
        assert entry_box_value not in profiles, "Profile name already exist!"
        self.__context.profiles_manager.rename_profile(
            original_name=active_profile,
            new_name=entry_box_value,
        )
        self.__context.profiles_manager.set_active_profile_name(
            entry_box_value
        )
        combobox.configure(
            values=self.__context.profiles_manager.list_profiles()
        )
        combobox.set(entry_box_value)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        assert self.__context.profiles_manager.get_active_profile_name(
        ), "There are no profiles to edit!"
        active_profile = self.__context.profiles_manager.get_active_profile_name()
        active_profile_steps = self.__context.profiles_manager.get_active_profile_steps()
        self.__context.steps_manager.set_steps(active_profile_steps)
        last_step = self.__context.steps_manager.last_step()
        self.__context.steps_manager.set_active_step_number(last_step)
        vertical_position = VerticalPosition(
            self.__rely,
            self.__rely_padding
        )

        window = CustomTopLevel(
            master=master,
            title=f"Profil: {active_profile} - Kroki",
            geometry="380x340",
        )
        frame = CustomFrame(master=window)

        profile_position = next(vertical_position)

        profile_label = CTkLabel(master=frame, text="Nazwa profilu:")
        profile_label.place(relx=self.__relx / 3.25,
                            rely=profile_position, anchor="center")

        profile_entry_box = CTkEntry(
            master=frame, placeholder_text=active_profile)
        profile_entry_box.place(
            relx=self.__relx, rely=profile_position, anchor="center")

        steps_position = next(vertical_position)

        steps_label = CTkLabel(master=frame, text="Krok:")
        steps_label.place(relx=self.__relx / 2.25,
                          rely=steps_position, anchor="center")

        steps_combobox = CustomComboBox(
            master=frame,
            state="readonly",
            values=self.__context.steps_manager.list_steps(),
            callback=lambda step_number: self.__context.steps_manager.set_active_step_number(
                step_number),
            content=last_step,
        )
        steps_combobox.place(
            relx=self.__relx, rely=steps_position, anchor="center")

        add_button = CustomButton(
            master=frame,
            text="Dodaj",
            callback=lambda: AddStep(
                master=window, context=self.__context, combobox=steps_combobox
            ),
        )
        add_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        edit_button = CustomButton(
            master=frame,
            text="Edytuj",
            callback=lambda: EditStep(
                master=window, context=self.__context),
        )
        edit_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        delete_button = CustomButton(
            master=frame,
            text="Usuń",
            callback=lambda: DeleteStep(
                context=self.__context, combobox=steps_combobox),
        )
        delete_button.place(relx=self.__relx, rely=next(
            vertical_position), anchor="center")

        save_button = CustomButton(
            master=frame,
            text="Zapisz",
            callback=lambda: (
                self.__update_profile_name(
                    entry_box_value=profile_entry_box.get(), combobox=combobox),
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
