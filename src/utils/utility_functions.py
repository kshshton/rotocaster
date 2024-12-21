from tkinter import IntVar, StringVar


class UtilityFunctions:
    @staticmethod
    def center_window(master) -> None:
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width - master.winfo_reqwidth()) // 2 - 100
        y = (screen_height - master.winfo_reqheight()) // 2.25

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
