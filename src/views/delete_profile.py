from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteProfile:
    def __init__(self, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        try:
            assert self.__settings.profiles_manager.is_profile_active()
            self.__settings.profiles_manager.set_active_profile(combobox.get())
            self.__settings.profiles_manager.delete_active_profile()
            combobox.configure(
                values=self.__settings.profiles_manager.list_profiles())
            combobox.set(self.__settings.profiles_manager.first_profile())
            self.__settings.profiles_file.update(
                self.__settings.profiles_manager.profiles)
        except AssertionError:
            pass
