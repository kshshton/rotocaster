from customtkinter import CTk

from src.custom_components.custom_button import CustomButton
from src.custom_components.custom_combobox import CustomComboBox
from src.events.add_profile import AddProfile
from src.events.delete_profile import DeleteProfile
from src.events.edit_profile import EditProfile
from src.events.run_manual_mode import RunManualMode
from src.events.run_profile import RunProfile
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions


class App(CTk):
    def __init__(self, title: str) -> None:
        super().__init__()        
        self.geometry("300x300")
        self.title(title)
        UtilityFunctions.center_window(self)

        self.__settings = Settings()

        self.__combobox = CustomComboBox(
            master=self,
            values=self.__settings._manager.list_profiles(),
            content=self.__settings._manager.first_profile(),
            callback=self.__settings._manager.select_profile 
        )
        CustomButton(master=self, text="Edytuj", callback=lambda: EditProfile(master=self, settings=self.__settings))
        CustomButton(master=self, text="Dodaj", callback=lambda: AddProfile(master=self, combobox=self.__combobox, settings=self.__settings))
        CustomButton(master=self, text="Usuń", callback=lambda: DeleteProfile(combobox=self.__combobox, settings=self.__settings))
        CustomButton(master=self, text="Uruchom profil", callback=lambda: RunProfile(master=self, settings=self.__settings))
        CustomButton(master=self, text="Uruchom tryb ręczny", callback=lambda: RunManualMode(master=self, settings=self.__settings))

        self.__settings._damper._listen_speed_value()
        self.mainloop()
