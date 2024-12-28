from customtkinter import CTk

from src.components.custom_combobox import CustomComboBox
from src.events.edit_profile import EditProfile
from src.utils.settings import Settings


class AddProfile:
    def __init__(self, master: CTk, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master, combobox)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        try:
            name = combobox.get()
            assert not name in self.__settings.manager.list_profiles()
            self.__settings.manager.active_profile = name
            self.__settings.manager.create_profile(name)
            combobox.configure(values=self.__settings.manager.list_profiles())
            EditProfile(master=master, settings=self.__settings)
        except AssertionError:
            pass
