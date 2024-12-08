import customtkinter as ctk
from customtkinter import CTk


class GUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("300x200")
        self.title("RotoCaster")
        self.__center_window(self)
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
        return self.__profiles[self.__active_profile]

    def __save_profile(self, name: str) -> None:        
        self.__profiles[name] = 0

    def __select_profile(self, name: str) -> None:
        self.__active_profile = name        

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

    def __delete_profile(self, name: str) -> None:    
        del self.__profiles[name]
        self.combobox.configure(values=list(self.__profiles.keys()))    

    def __window(self) -> None:
        self.combobox = ctk.CTkComboBox(
            master=self,
            values=list(self.__profiles.keys()),
            command=self.__select_profile,
            
        )
        self.combobox.pack(pady=10, padx=10, anchor='center')
        self.combobox.set("Wybierz profil")

        self.add_button = ctk.CTkButton(
            master=self,
            text="Dodaj",
            command=self.__edit_profile,
        )
        self.add_button.pack(pady=10, padx=10, anchor='center')

        self.edit_button = ctk.CTkButton(
            master=self,
            text="Edytuj",
            command=self.__edit_profile,
        )
        self.edit_button.pack(pady=10, padx=10, anchor='center')

        self.execute_button = ctk.CTkButton(
            master=self,
            text="Uruchom",
            command=self.__get_profile_value,
        )
        self.execute_button.pack(pady=10, padx=10, anchor='center')

        self.mainloop()
