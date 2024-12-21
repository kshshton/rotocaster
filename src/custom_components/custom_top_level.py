from customtkinter import CTk, CTkToplevel

from src.utils.utility_functions import UtilityFunctions


class CustomTopLevel(CTkToplevel):
    def __init__(
        self, 
        master: CTk,
        title: str,
        geometry: str = "300x200",
    ) -> None:  
        super().__init__()
        self.title(title)
        self.transient(master)
        self.geometry(geometry)
        UtilityFunctions.center_window(self)
