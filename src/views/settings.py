import json
from tkinter import StringVar

from customtkinter import CTk, CTkEntry, CTkLabel

from src.components.custom_button import CustomButton
from src.components.custom_frame import CustomFrame
from src.components.custom_top_level import CustomTopLevel
from src.utils.utility_functions import UtilityFunctions
from src.utils.vertical_position import VerticalPosition


class Settings:
    def __init__(self, master: CTk) -> None:
        self.__settings_filename: str = "settings.json"
        self.__relx: float = 0.5
        self.__rely: float = 0
        self.__rely_padding: float = 0.13
        self.__render(master)

    def load_settings(self) -> dict:
        with open(self.__settings_filename, "r") as file:
            config = json.load(file)
            return config

    def update_connetion_context(
        self,
        address: str,
        port: int,
        STBY: int,
        AIN1: int,
        AIN2: int,
        PWMA: int
    ) -> None:
        with open(self.__settings_filename, "r") as file:
            config = json.load(file)

        config["accessPoint"]["address"] = address
        config["accessPoint"]["port"] = port
        config["pins"]["STBY"] = STBY
        config["pins"]["AIN1"] = AIN1
        config["pins"]["AIN2"] = AIN2
        config["pins"]["PWMA"] = PWMA

        with open(self.__settings_filename, "w") as file:
            json.dump(config, file)

        message = f"settings:STBY={STBY};AIN1={AIN1};AIN2={AIN2};PWMA={PWMA}"
        UtilityFunctions.send_message_to_board(message)

    def __render(self, master: CTk) -> None:
        vertical_position = VerticalPosition(
            self.__rely,
            self.__rely_padding
        )

        window = CustomTopLevel(
            master=master,
            title=f"Ustawienia",
            geometry="380x380",
        )
        frame = CustomFrame(master=window)

        settings = self.load_settings()

        position = next(vertical_position)

        address_label = CTkLabel(master=frame, text="Address:")
        address_label.place(relx=self.__relx / 3,
                            rely=position, anchor="center")

        address_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["accessPoint"]["address"]))
        address_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        port_label = CTkLabel(master=frame, text="Port:")
        port_label.place(relx=self.__relx / 2.5,
                         rely=position, anchor="center")

        port_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["accessPoint"]["port"]))
        port_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        stby_label = CTkLabel(master=frame, text="STBY:")
        stby_label.place(relx=self.__relx / 2.5,
                         rely=position, anchor="center")

        stby_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["pins"]["STBY"]))
        stby_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        pwma_label = CTkLabel(master=frame, text="PWMA:")
        pwma_label.place(relx=self.__relx / 2.5,
                         rely=position, anchor="center")

        pwma_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["pins"]["PWMA"]))
        pwma_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        ain1_label = CTkLabel(master=frame, text="AIN1:")
        ain1_label.place(relx=self.__relx / 2.5,
                         rely=position, anchor="center")

        ain1_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["pins"]["AIN1"]))
        ain1_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        ain2_label = CTkLabel(master=frame, text="AIN2:")
        ain2_label.place(relx=self.__relx / 2.5,
                         rely=position, anchor="center")

        ain2_entry_box = CTkEntry(
            master=frame, textvariable=StringVar(value=settings["pins"]["AIN2"]))
        ain2_entry_box.place(
            relx=self.__relx, rely=position, anchor="center")

        position = next(vertical_position)

        save_button = CustomButton(
            master=frame,
            text="Zapisz",
            callback=lambda: (
                self.update_connetion_context(
                    address=address_entry_box.get(),
                    port=int(port_entry_box.get()),
                    STBY=int(stby_entry_box.get()),
                    AIN1=int(ain1_entry_box.get()),
                    AIN2=int(ain2_entry_box.get()),
                    PWMA=int(pwma_entry_box.get()),
                ),
                UtilityFunctions.close_window(master=window),
            )
        )
        save_button.place(relx=self.__relx,
                          rely=position, anchor="center")
