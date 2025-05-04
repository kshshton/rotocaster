from src.components.custom_combobox import CustomComboBox
from src.utils.context import Context


class DeleteProfile:
    def __init__(self, combobox: CustomComboBox, context: Context) -> None:
        self.__context = context
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        assert self.__context.profiles_manager.is_profile_active(
        ), "There are no profiles to delete!"
        self.__context.profiles_manager.delete_active_profile()
        combobox.configure(
            values=self.__context.profiles_manager.list_profiles())
        first_profile = self.__context.profiles_manager.first_profile() or ""
        combobox.set(first_profile)
        self.__context.profiles_manager.set_active_profile_name(
            first_profile)
        self.__context.profiles_file.update(
            self.__context.profiles_manager.get_profiles())
