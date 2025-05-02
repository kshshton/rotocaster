from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteStep:
    def __init__(self, settings: Settings, combobox: CustomComboBox) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        try:
            assert self.__settings.steps_manager.is_step_active()
            active_step = self.__settings.steps_manager.get_active_step()
            active_profile_name = self.__settings.profiles_manager.get_active_profile()
            self.__settings.steps_manager.delete_step(
                profile_name=active_profile_name, step=active_step)
            self.__settings.steps_manager.reset_numbers(
                profile_name=active_profile_name)
            combobox.configure(values=self.__settings.steps_manager.sequence(
                profile_name=active_profile_name))
            combobox.set(self.__settings.steps_manager.last_step_number(
                profile_name=active_profile_name))
        except AssertionError:
            pass
