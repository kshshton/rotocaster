from src.components.custom_combobox import CustomComboBox
from src.utils.context import Context


class DeleteStep:
    def __init__(self, context: Context, combobox: CustomComboBox) -> None:
        self.__context = context
        self.__render(combobox)

    def __render(self, combobox: CustomComboBox) -> None:
        assert self.__context.steps_manager.is_step_active(), "There are no steps to delete!"
        self.__context.steps_manager.delete_active_step()
        self.__context.steps_manager.reset_numbers()
        current_steps = self.__context.steps_manager.get_steps()
        self.__context.profiles_manager.set_active_profile_steps(
            current_steps)
        self.__context.profiles_file.update(
            self.__context.profiles_manager.get_profiles())
        combobox.configure(
            values=self.__context.steps_manager.list_steps()
        )
        previous_step = self.__context.steps_manager.last_step() or ""
        combobox.set(previous_step)
        self.__context.steps_manager.set_active_step_number(previous_step)
