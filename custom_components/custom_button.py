from customtkinter import CTk, CTkButton


class CustomButton(CTkButton):
    def __init__(
        self,
        master: CTk, 
        text: str, 
        callback: callable,
        anchor: str = "center",
        padding: dict = {"pady": 10, "padx": 10},
    ) -> None:
        super().__init__(
            master=master,
            text=text,
            command=callback,
        )
        self.pack(**padding, anchor=anchor)
