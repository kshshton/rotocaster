from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteStep:
    def __init__(self, settings: Settings, combobox: CustomComboBox) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        assert self.__settings.steps_manager.is_step_active(), "There are no steps to delete!"
        self.__settings.steps_manager.delete_active_step()
        self.__settings.steps_manager.reset_numbers()
        current_steps = self.__settings.steps_manager.get_steps()
        self.__settings.profiles_manager.set_active_profile_steps(
            current_steps)
        self.__settings.profiles_file.update(
            self.__settings.profiles_manager.get_profiles())
        combobox.configure(
            values=self.__settings.steps_manager.list_steps()
        )
        previous_step = self.__settings.steps_manager.last_step() or ""
        combobox.set(previous_step)
        self.__settings.steps_manager.set_active_step_number(previous_step)
