from customtkinter import CTk, CTkToplevel

from utils import Utils


class CustomTopLevel(CTkToplevel):
    def __init__(
        self, 
        title: str,
        master: CTk,
        geometry: str = "300x200",
    ) -> None:  
        super().__init__()
        self.title(title)
        self.transient(master)
        self.geometry(geometry)
        Utils.center_window(self)
