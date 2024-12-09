import json
import os
import time
from typing import Optional

import customtkinter as ctk
from customtkinter import CTk


class GUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("300x300")
        self.title("RotoCaster")
        self.__button_padding = {"pady":10, "padx": 10}
        self.__center_window(self)
        self.__default_text = "Wybierz profil"
        self.__json_filename = "profiles.json"
        self.__create_profiles_file()
        self.__profiles = self.__load_profiles_file()
        self.__output_speed = 0
        self.__active_profile = None
        self.__speed = ctk.IntVar()
        self.__test_speed = ctk.IntVar()
        self.__test_speed.trace_add('write', self.__overwrite_output_speed)
        self.combobox = ctk.CTkComboBox(
            master=self,
            values=self.__list_profiles(),
            command=self.__select_profile
        )
        self.combobox.pack(**self.__button_padding, anchor='center')
        self.combobox.set(self.__default_text)
        self.__add_button("Dodaj", self.__add_profile)
        self.__add_button("Usuń", self.__delete_profile)
        self.__add_button("Edytuj", self.__edit_profile)
        self.__add_button("Uruchom profil", self.__run_profile)
        self.__add_button("Uruchom tryb testowy", self.__run_test_mode)
        self.__listen_output_speed()
        self.mainloop()

    def __listen_output_speed(self) -> None:
        print(self.__output_speed)
        self.after(ms=100, func=self.__listen_output_speed)

    def __reset_speed_value(self) -> None:
        if self.__output_speed == 0:
            return self.__output_speed
        self.__output_speed -= 1
        self.after(ms=50, func=self.__reset_speed_value)

    def __overwrite_output_speed(self, *args) -> None:
        self.__output_speed = self.__test_speed.get()

    def __create_profiles_file(self) -> None:
        if not os.path.exists(self.__json_filename):
            with open(self.__json_filename, 'w') as file:
                data = {}
                json.dump(data, file, indent=4)

    def __load_profiles_file(self) -> None:
        try:
            with open(self.__json_filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def __update_profiles_file(self) -> None:
        with open("profiles.json", 'w') as file:
            file.write(json.dumps(self.__profiles, indent=4))

    def __center_window(self, window) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - window.winfo_reqwidth()) // 2 - 100
        y = (screen_height - window.winfo_reqheight()) // 2.25

        window.geometry(f"+{x}+{y}")

    def __get_profile_value(self) -> int:
        return self.__profiles[self.__active_profile]

    def __close_window(
            self,
            window: ctk.CTkToplevel,
            callback: Optional[callable] = None
        ) -> None:
        try:
            callback()
        except TypeError:
            pass
        finally:
            window.destroy()

    def __save_profile_value(self, window) -> None:
        self.__profiles[self.__active_profile] = self.__speed.get()
        self.__close_window(window)
        self.__update_profiles_file()

    def __run_profile(self) -> None:
        try:
            assert self.__active_profile
            run_window = ctk.CTkToplevel()
            run_window.geometry("200x100")
            run_window.title(f"Uruchomiono: {self.__active_profile}")
            run_window.transient(self)
            self.__center_window(window=run_window)

            self.__output_speed = self.__get_profile_value()

            self.stop_button = ctk.CTkButton(
                master=run_window,
                text="Zatrzymaj",
                command=lambda:
                    self.__close_window(
                        window=run_window,
                        callback=self.__reset_speed_value
                    ),
            )
            self.stop_button.place(relx=0.5, rely=0.5, anchor='center')
        except:
            pass

    def __run_test_mode(self) -> None:
        test_window = ctk.CTkToplevel()
        test_window.geometry("300x200")
        test_window.title("Uruchomiono: tryb testowy")
        test_window.transient(self)
        self.__center_window(test_window)

        frame = ctk.CTkFrame(master=test_window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.__test_speed.set(0)

        slider = ctk.CTkSlider(master=frame, from_=0, to=100, variable=self.__test_speed)
        slider.place(relx=0.5, rely=0.5, anchor='center')

        speed_box = ctk.CTkEntry(master=frame, textvariable=self.__test_speed)
        speed_box.place(relx=0.5, rely=0.25, anchor='center')

        self.stop_button = ctk.CTkButton(
            master=frame,
            text="Zatrzymaj",
            command=lambda:
                self.__close_window(
                    window=test_window,
                    callback=self.__reset_speed_value
                ),
        )
        self.stop_button.place(relx=0.5, rely=0.8, anchor='center')

        self.__output_speed = self.__test_speed.get()

    def __save_profile(self, name: str) -> None:
        self.__profiles[name] = 0

    def __select_profile(self, name: str) -> None:
        self.__active_profile = name

    def __list_profiles(self) -> list:
        return sorted(list(self.__profiles.keys()))

    def __add_profile(self) -> None:
        value = self.combobox.get()
        self.__active_profile = value
        self.__save_profile(self.__active_profile)
        self.combobox.configure(values=self.__list_profiles())
        self.__edit_profile()
        self.__update_profiles_file()

    def __delete_profile(self) -> None:
        value = self.combobox.get()
        del self.__profiles[value]
        self.combobox.configure(values=self.__list_profiles())
        self.combobox.set(self.__default_text)
        self.__update_profiles_file()

    def __edit_profile(self) -> None:
        edit_window = ctk.CTkToplevel()
        edit_window.geometry("300x200")
        edit_window.title(self.__active_profile)
        edit_window.transient(self)
        self.__center_window(edit_window)

        frame = ctk.CTkFrame(master=edit_window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        profile_value = self.__profiles[self.__active_profile]

        slider = ctk.CTkSlider(master=frame, from_=0, to=100, variable=self.__speed)
        slider.place(relx=0.5, rely=0.5, anchor='center')
        slider.set(profile_value)

        speed_box = ctk.CTkEntry(master=frame, textvariable=self.__speed)
        speed_box.place(relx=0.5, rely=0.25, anchor='center')

        self.save_button = ctk.CTkButton(
            master=frame,
            text="Zapisz",
            command=lambda: self.__save_profile_value(window=edit_window),
        )
        self.save_button.place(relx=0.5, rely=0.8, anchor='center')

    def __add_button(self, text: str, callback: callable) -> None:
        button = ctk.CTkButton(
            master=self,
            text=text,
            command=callback,
        )
        button.pack(**self.__button_padding, anchor='center')


if __name__ == "__main__":
    GUI()
