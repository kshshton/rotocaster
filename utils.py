

class Utils:
    @staticmethod
    def center_window(window) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - window.winfo_reqwidth()) // 2 - 100
        y = (screen_height - window.winfo_reqheight()) // 2.25

        window.geometry(f"+{x}+{y}")
