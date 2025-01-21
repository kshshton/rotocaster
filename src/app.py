from customtkinter import CTk, CTkLabel

from src.components.custom_button import CustomButton
from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions
from src.views.add_profile import AddProfile
from src.views.delete_profile import DeleteProfile
from src.views.manage_steps import ManageSteps
from src.views.run_manual_mode import RunManualMode
from src.views.run_profile import RunProfile


class App(CTk):
    def __init__(self, title: str) -> None:
        super().__init__()        
        self.geometry("300x300")
        self.title(title)
        UtilityFunctions.center_window(self)
        self.__settings = Settings()
        self.__label = CTkLabel(self, text="Profil: ")
        self.__label.place(relx=0.16, rely=0.08, anchor="center")

        self.__combobox = CustomComboBox(
            master=self,
            state="readonly",
            values=self.__settings.profiles_manager.list_profiles(),
            content=self.__settings.profiles_manager.first_profile(),
            callback=self.__settings.profiles_manager.select_profile,
        )

        CustomButton(master=self, text="Zarządzaj krokami", callback=lambda: ManageSteps(master=self, combobox=self.__combobox, settings=self.__settings))
        CustomButton(master=self, text="Dodaj profil", callback=lambda: AddProfile(master=self, combobox=self.__combobox, settings=self.__settings))
        CustomButton(master=self, text="Usuń profil", callback=lambda: DeleteProfile(combobox=self.__combobox, settings=self.__settings))
        CustomButton(master=self, text="Uruchom profil", callback=lambda: RunProfile(master=self, settings=self.__settings))
        CustomButton(master=self, text="Uruchom tryb ręczny", callback=lambda: RunManualMode(master=self, settings=self.__settings))

        self.__settings.engine.listen_value()
        self.mainloop()
