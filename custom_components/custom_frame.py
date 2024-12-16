from customtkinter import CTk, CTkFrame


class CustomFrame(CTkFrame):
    def __init__(self, master: CTk) -> None:  
        super().__init__(master=master)
        self.pack(pady=20, padx=20, fill="both", expand=True)
