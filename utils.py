

class Utils:
    @staticmethod
    def center_window(master) -> None:
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width - master.winfo_reqwidth()) // 2 - 100
        y = (screen_height - master.winfo_reqheight()) // 2.25

        master.geometry(f"+{x}+{y}")
