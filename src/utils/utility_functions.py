from tkinter import IntVar, StringVar

from customtkinter import CTk, CTkToplevel


class UtilityFunctions:
    @staticmethod
    def center_window(master: CTk) -> None:
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = int((screen_width - master.winfo_reqwidth()) / 2)
        y = int((screen_height - master.winfo_reqheight()) / 2)

        master.geometry(f"+{x}+{y}")

    @staticmethod
    def slider_validation(input: StringVar, output: IntVar) -> None:
        try:
            value = int(input.get())
            if value > 100:
                output.set(100)
            else:
                output.set(value)
        except ValueError:
            output.set(0)

    @staticmethod
    def text_to_speed(text: StringVar, speed: IntVar) -> None:
        try:
            text.set(str(speed.get()))
        except ValueError:
            speed.set(0)

    @staticmethod
    def close_window(master: CTkToplevel) -> None:        
        master.destroy()
