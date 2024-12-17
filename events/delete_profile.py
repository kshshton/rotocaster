from custom_components.custom_combobox import CustomComboBox
from settings import Settings


class DeleteProfile:
    def __init__(self, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        try:
            assert self.__settings._manager.is_profile_active()
            self.__settings._manager.active_profile = combobox.get()
            del self.__settings._manager.active_profile
            combobox.configure(values=self.__settings._manager.list_profiles())
            combobox.set(self.__settings._manager.first_profile())
            self.__settings._file.update(self.__settings._manager.profiles)
        except AssertionError:
            pass
