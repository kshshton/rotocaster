from customtkinter import CTk, CTkButton, CTkComboBox, CTkLabel

from src.components.custom_combobox import CustomComboBox
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.types.axis_direction import AxisDirection
from src.utils.settings import Settings
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition
from src.views.run_manual_mode import RunManualMode


class SelectDirection:
    def __init__(self, master: CTk, settings: Settings) -> None:
        self.__settings = settings
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.275
        self.__render(master)

    def __update_direction(self, direction: str) -> None:
        self.__settings.engine.direction = direction

    def __render(self, master: CTk) -> None:
        window = CustomTopLevel(
            master=master,
            title=f"Wybierz kierunek",
            geometry="200x200",
        )
        frame = CustomFrame(master=window)
        vertical_position = VerticalPosition(self.__rely, self.__rely_padding)

        direction_label = CTkLabel(master=frame, text="Kierunek:")
        direction_label.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        direction_combobox = CustomComboBox(
            master=frame, 
            values=[AxisDirection.LEFT.value, AxisDirection.RIGHT.value],
            content=self.__settings.engine.direction,
        )
        direction_combobox.place(relx=self.__relx, rely=next(vertical_position), anchor="center")

        save_button = CTkButton(
            master=frame,
            text="Zapisz",
            command=lambda: (
                self.__update_direction(direction_combobox.get()),
                UtilityFunctions.close_window(master=window),
                RunManualMode(master=master, settings=self.__settings),
            )
        )
        save_button.place(relx=self.__relx, rely=next(vertical_position), anchor="center")
