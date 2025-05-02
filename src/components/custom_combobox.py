from typing import Optional

from customtkinter import CTk, CTkComboBox


class CustomComboBox(CTkComboBox):
    def __init__(
        self,
        master: CTk,
        values: list,
        content: any,
        callback: Optional[callable] = None,
        padding={"padx": 10, "pady": 10},
        anchor="center",
        **kwargs,
    ):
        super().__init__(
            master=master,
            values=values,
            command=callback,
            **kwargs,
        )
        self.pack(**padding, anchor=anchor)
        self.set(content or "")
