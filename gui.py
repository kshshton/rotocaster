import customtkinter as ctk
from customtkinter import CTk


class GUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("500x300")
        self.__center_window()
        self.profiles = {}
        self.active_profile = None
        self.__speed = ctk.IntVar()

        # mockup
        self.__save_profile("rzezba1")
        self.__save_profile("rzezba2")
        self.__save_profile("rzezba3")
        self.__save_profile("rzezba4")

        self.__window()

    def __center_window(self) -> None:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.winfo_reqwidth()) // 2 - 150
        y = (screen_height - self.winfo_reqheight()) // 2.25

        self.geometry(f"+{x}+{y}")

    def __save_profile_value(self) -> None:        
        self.profiles[self.active_profile] = self.__speed.get()

    def __get_profile_value(self) -> int:
        return self.profiles[self.active_profile]

    def __save_profile(self, name: str) -> None:        
        self.profiles[name] = 0

    def __select_profile(self, name: str) -> None:
        self.label.configure(text=name)
        # self.frame.pack(pady=20, padx=120, fill="both", expand=True)
        
        self.active_profile = name
        profile_value = self.profiles[self.active_profile]
        self.slider.set(profile_value)

    def __edit_profile(self) -> None:
        edit_window = ctk.CTkToplevel()
        edit_window.geometry("300x200")
        edit_window.title(self.active_profile)
        edit_window.transient(self)

        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()

        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2

        edit_window.geometry(f"+{x}+{y}")

    def __delete_profile(self, name: str) -> None:    
        del self.profiles[name]
        self.combobox.configure(values=list(self.profiles.keys()))    

    def __window(self) -> None:
        self.combobox = ctk.CTkComboBox(
            master=self,
            values=list(self.profiles.keys()),
            command=self.__select_profile,
            
        )
        self.combobox.pack(pady=10, padx=10, anchor='nw')
        self.combobox.set("Wybierz profil")

        self.frame = ctk.CTkFrame(master=self)
        self.label = ctk.CTkLabel(master=self.frame)
        self.label.place(relx=0.5, rely=0.1, anchor='center')

        self.slider = ctk.CTkSlider(master=self.frame, from_=0, to=100, variable=self.__speed)
        self.slider.place(relx=0.5, rely=0.55, anchor='center')

        self.speed_box = ctk.CTkEntry(master=self.frame, textvariable=self.__speed)
        self.speed_box.place(relx=0.5, rely=0.35, anchor='center')

        self.save_button = ctk.CTkButton(
            master=self.frame,
            text="Zapisz",
            command=self.__save_profile_value,
        )
        self.save_button.place(relx=0.5, rely=0.8, anchor='center')

        self.edit_button = ctk.CTkButton(
            master=self,
            text="Edytuj",
            command=self.__edit_profile,
        )
        self.edit_button.pack(pady=0, padx=10, anchor='nw')

        self.execute_button = ctk.CTkButton(
            master=self,
            text="Uruchom",
            command=self.__get_profile_value,
        )
        self.execute_button.pack(pady=10, padx=10, anchor='nw')

        self.mainloop()
