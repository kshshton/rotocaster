from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteProfile:
    def __init__(self, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        try:
            assert self.__settings.manager.is_profile_active()
            self.__settings.manager.active_profile = combobox.get()
            del self.__settings.manager.active_profile
            combobox.configure(values=self.__settings.manager.list_profiles())
            combobox.set(self.__settings.manager.first_profile())
            self.__settings.file.update(self.__settings.manager.profiles)
        except AssertionError:
            pass
