from customtkinter import CTk, CTkButton, CTkLabel

from src.components.custom_top_level import CustomTopLevel
from src.utils.context import Context
from src.utils.utility_functions import UtilityFunctions


class ExitApp:
    def __init__(self, master: CTk, context: Context) -> None:
        self.__context = context
        self.__relx: float = 0.5
        self.__render(master)

    def __render(self, master: CTk) -> None:
        window = CustomTopLevel(
            master=master,
            geometry="275x100",
            title="Zamknij aplikacje",
            close_window_button_blocked=True
        )

        message_label = CTkLabel(
            master=window, text="Czy na pewno chcesz zamknąć aplikację?")
        message_label.place(
            relx=self.__relx, rely=0.2, anchor="center")

        yes_button = CTkButton(
            master=window,
            text="Tak",
            width=70,
            command=lambda: (
                self.__context.engine.turn_off(),
                UtilityFunctions.close_window(master=master)
            )
        )
        yes_button.place(relx=self.__relx - 0.15, rely=0.6, anchor="center")

        no_button = CTkButton(
            master=window,
            text="Nie",
            width=70,
            command=lambda: (
                master.unactivate_exit_window(),
                UtilityFunctions.close_window(master=window),
            )
        )
        no_button.place(relx=self.__relx + 0.15, rely=0.6, anchor="center")
