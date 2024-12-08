import customtkinter as ctk
from customtkinter import CTk


class GUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("300x250")
        self.title("RotoCaster")
        self.__button_padding = {"pady":10, "padx": 10}
        self.__center_window(self)
        self.__default_text = "Wybierz profil"
        self.__profiles = {}
        self.__active_profile = None
        self.__speed = ctk.IntVar()

        # mockup
        self.__save_profile("rzezba1")
        self.__save_profile("rzezba2")
        self.__save_profile("rzezba3")
        self.__save_profile("rzezba4")

        self.__window()

    def __center_window(self, window) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - window.winfo_reqwidth()) // 2 - 150
        y = (screen_height - window.winfo_reqheight()) // 2.25

        window.geometry(f"+{x}+{y}")

    def __save_profile_value(self, window) -> None:        
        self.__profiles[self.__active_profile] = self.__speed.get()
        self.__close_window(window)
        print(self.__profiles)

    def __get_profile_value(self) -> int:
        print(self.__profiles[self.__active_profile])
        return self.__profiles[self.__active_profile]

    def __save_profile(self, name: str) -> None:        
        self.__profiles[name] = 0

    def __select_profile(self, name: str) -> None:
        self.__active_profile = name

    def __add_profile(self) -> None:
        value = self.combobox.get()
        self.__active_profile = value
        self.__save_profile(self.__active_profile)
        self.combobox.configure(values=list(self.__profiles.keys()))
        self.__edit_profile()

    def __delete_profile(self) -> None:    
        value = self.combobox.get()
        del self.__profiles[value]
        self.combobox.configure(values=list(self.__profiles.keys()))
        self.combobox.set(self.__default_text)

    def __edit_profile(self) -> None:
        edit_window = ctk.CTkToplevel()
        edit_window.geometry("300x200")
        edit_window.title(self.__active_profile)
        edit_window.transient(self)

        self.__center_window(edit_window)

        self.frame = ctk.CTkFrame(master=edit_window)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        profile_value = self.__profiles[self.__active_profile]

        self.slider = ctk.CTkSlider(master=self.frame, from_=0, to=100, variable=self.__speed)
        self.slider.place(relx=0.5, rely=0.5, anchor='center')
        self.slider.set(profile_value)

        self.speed_box = ctk.CTkEntry(master=self.frame, textvariable=self.__speed)
        self.speed_box.place(relx=0.5, rely=0.25, anchor='center')

        self.save_button = ctk.CTkButton(
            master=self.frame,
            text="Zapisz",
            command=lambda: self.__save_profile_value(edit_window),
        )
        self.save_button.place(relx=0.5, rely=0.8, anchor='center')

    def __close_window(self, window: ctk.CTkToplevel) -> None:
        window.destroy()

    def __add_button(self, text: str, func: callable):
        button = ctk.CTkButton(
            master=self,
            text=text,
            command=func,
        )
        button.pack(**self.__button_padding, anchor='center')

    def __window(self) -> None:
        self.combobox = ctk.CTkComboBox(
            master=self,
            values=list(self.__profiles.keys()),
            command=self.__select_profile            
        )
        self.combobox.pack(**self.__button_padding, anchor='center')
        self.combobox.set(self.__default_text)
        self.__add_button("Dodaj", self.__add_profile)
        self.__add_button("Usuń", self.__delete_profile)
        self.__add_button("Edytuj", self.__edit_profile)
        self.__add_button("Uruchom", self.__get_profile_value)

        self.mainloop()
