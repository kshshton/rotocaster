import asyncio

from customtkinter import CTk, CTkLabel

from src.components.custom_button import CustomButton
from src.components.custom_combobox import CustomComboBox
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions
from src.views.add_profile import AddProfile
from src.views.delete_profile import DeleteProfile
from src.views.edit_profile import EditProfile
from src.views.exit_app import ExitApp
from src.views.run_profile import RunProfile
from src.views.select_direction import SelectDirection
from src.views.settings import Settings


class App(CTk):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.__window_geometry: str = "300x350"
        self.geometry(self.__window_geometry)
        self.resizable(False, False)
        self.title(title)
        UtilityFunctions.center_window(
            self, window_geometry=self.__window_geometry)
        self.__context = Context()
        self.__label = CTkLabel(self, text="Profil: ")
        self.__label.place(relx=0.16, rely=0.065, anchor="center")
        self.protocol("WM_DELETE_WINDOW", self.exit_window)

        self.__active_exit_window: bool = False
        first_profile = self.__context.profiles_manager.first_profile() or ""
        self.__context.profiles_manager.set_active_profile_name(
            first_profile)

        self.__combobox = CustomComboBox(
            master=self,
            state="readonly",
            values=self.__context.profiles_manager.list_profiles(),
            content=first_profile,
            callback=lambda name: self.__context.profiles_manager.set_active_profile_name(
                name
            ),
        )

        CustomButton(master=self, text="Dodaj profil", callback=lambda: AddProfile(
            master=self, combobox=self.__combobox, context=self.__context))
        CustomButton(master=self, text="Edytuj profil", callback=lambda: EditProfile(
            master=self, combobox=self.__combobox, context=self.__context))
        CustomButton(master=self, text="Usuń profil", callback=lambda: DeleteProfile(
            combobox=self.__combobox, context=self.__context))
        CustomButton(master=self, text="Uruchom profil", callback=lambda: RunProfile(
            master=self, context=self.__context))
        CustomButton(master=self, text="Uruchom tryb ręczny", callback=lambda: SelectDirection(
            master=self, context=self.__context))
        CustomButton(master=self, text="Ustawienia",
                     callback=lambda: Settings(master=self))

    def run(self):
        self.__context.engine.stream_output_to_board()
        self.mainloop()

    def exit_window(self):
        if not self.__active_exit_window:
            self.__active_exit_window = True
            ExitApp(master=self, context=self.__context)

    def unactivate_exit_window(self):
        self.__active_exit_window = False
