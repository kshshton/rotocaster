from customtkinter import CTk, CTkToplevel

from src.utils.utility_functions import UtilityFunctions


class CustomTopLevel(CTkToplevel):
    def __init__(
        self, 
        master: CTk,
        title: str,
        geometry: str = "300x200",
        **kwargs,
    ) -> None:  
        super().__init__(**kwargs)
        self.title(title)
        self.transient(master)
        self.geometry(geometry)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        UtilityFunctions.center_window(self)
