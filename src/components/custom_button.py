from customtkinter import CTk, CTkButton


class CustomButton(CTkButton):
    def __init__(
        self,
        master: CTk, 
        text: str, 
        callback: callable,
        anchor: str = "center",
        padding: dict[str, int] = {"pady": 10, "padx": 10},
        **kwargs,
    ) -> None:
        super().__init__(
            master=master,
            text=text,
            command=callback,
            **kwargs,
        )
        self.pack(**padding, anchor=anchor)
