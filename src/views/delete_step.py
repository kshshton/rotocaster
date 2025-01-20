from src.components.custom_combobox import CustomComboBox
from src.utils.settings import Settings


class DeleteStep:
    def __init__(self, combobox: CustomComboBox, settings: Settings) -> None:
        self.__settings = settings
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        try:
            assert self.__settings.steps_manager.is_step_active()
            self.__settings.steps_manager.active_profile = combobox.get()
            del self.__settings.profiles_manager.active_profile_content[
                self.__settings.steps_manager.active_step
            ]
            combobox.configure(values=self.__settings.steps_manager.sequence())
            combobox.set(self.__settings.steps_manager.first_step())
            self.__settings.file.update(self.__settings.profiles_manager.profiles)
        except AssertionError:
            pass
