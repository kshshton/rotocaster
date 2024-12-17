from customtkinter import CTk

from custom_components.custom_combobox import CustomComboBox
from events.edit_profile import EditProfile
from settings import Settings


class AddProfile:
    def __init__(self, master: CTk, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(master, combobox)

    def __render(self, master: CTk, combobox: CustomComboBox) -> None:
        try:
            name = combobox.get()
            assert not name in self.__settings._manager.list_profiles()
            self.__settings._manager.active_profile = name
            self.__settings._manager.create_profile(name)
            combobox.configure(values=self.__settings._manager.list_profiles())
            EditProfile(master=master, settings=self.__settings)
            self.__settings._file.update(self.__settings._manager.profiles)
        except AssertionError:
            pass
