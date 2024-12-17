from customtkinter import CTk, CTkComboBox


class CustomComboBox(CTkComboBox):
    def __init__(
        self,
        master: CTk,
        values: list,
        content: any,
        callback: callable,
        padding={"padx": 10, "pady": 10},
        anchor="center",
    ):
        super().__init__(
            master=master,
            values=values,
            command=callback,
        )
        self.pack(**padding, anchor=anchor)
        self.set(content)
