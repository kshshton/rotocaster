from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteProfile:
    def __init__(self, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        assert self.__settings.profiles_manager.is_profile_active(
        ), "There are no profiles to delete!"
        self.__settings.profiles_manager.delete_active_profile()
        combobox.configure(
            values=self.__settings.profiles_manager.list_profiles())
        first_profile = self.__settings.profiles_manager.first_profile() or ""
        combobox.set(first_profile)
        self.__settings.profiles_manager.set_active_profile_name(
            first_profile)
        self.__settings.profiles_file.update(
            self.__settings.profiles_manager.get_profiles())
