import json
import os
from typing import Optional

from customtkinter import (CTk, CTkButton, CTkComboBox, CTkEntry, CTkFrame,
                           CTkSlider, CTkToplevel, IntVar, StringVar)


class GUI(CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("300x300")
        self.title("RotoCaster")
        self.__button_padding = {"pady":10, "padx": 10}
        self.__center_window(self)
        self.__json_filename = "profiles.json"
        self.__create_profiles_file()
        self.__profiles = self.__load_profiles_file()
        self.__output_speed = 0
        self.__active_profile = None
        self.__active_operator = None
        self.__profile_speed = IntVar()
        self.__profile_speed_text = StringVar()
        self.__profile_speed.trace_add(
            "write",
            lambda *args: self.__text_to_speed(
                text=self.__profile_speed_text,
                speed=self.__profile_speed,
            )
        )
        self.__profile_speed_text.trace_add(
            "write",
            lambda *args: self.__slider_validation(
                input=self.__profile_speed_text,
                output=self.__profile_speed,
            )
        )
        self.__test_speed = IntVar()
        self.__test_speed_text = StringVar()
        self.__test_speed.trace_add(
            "write",
            lambda *args: self.__text_to_speed(
                text=self.__test_speed_text,
                speed=self.__test_speed,
            )
        )
        self.__test_speed_text.trace_add(
            "write",
            lambda *args: self.__slider_validation(
                input=self.__test_speed_text,
                output=self.__test_speed,
            )
        )
        self.__test_speed.trace_add("write", self.__test_to_output_speed)
        self.combobox = CTkComboBox(
            master=self,
            values=self.__list_profiles(),
            command=self.__select_profile
        )
        self.combobox.pack(**self.__button_padding, anchor="center")
        self.combobox.set("")
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
        if self.__active_operator == "decrement":
            if self.__output_speed == 0:
                return self.__output_speed
            self.__output_speed -= 1
            self.after(ms=50, func=self.__reset_speed_value)

    def __reach_current_profile_speed(self) -> None:
        if self.__active_operator == "increment":
            if self.__output_speed == self.__get_profile_value():
                return self.__output_speed + 1
            self.__output_speed += 1
            self.after(ms=50, func=self.__reach_current_profile_speed)

    def __slider_validation(self, input: StringVar, output: IntVar) -> None:
        try:
            value = int(input.get())
            if value > 100:
                output.set(100)
            else:
                output.set(value)
        except:
            output.set(0)

    def __test_to_output_speed(self, *args: any) -> None:
        self.__output_speed = self.__test_speed.get()

    def __text_to_speed(self, text: StringVar, speed: IntVar) -> None:
        try:
            text.set(str(speed.get()))
        except:
            speed.set(0)

    def __create_profiles_file(self) -> None:
        if not os.path.exists(self.__json_filename):
            with open(self.__json_filename, "w") as file:
                data = {}
                json.dump(data, file, indent=4)

    def __load_profiles_file(self) -> None:
        try:
            with open(self.__json_filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def __update_profiles_file(self) -> None:
        with open("profiles.json", "w") as file:
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
            window: CTkToplevel,
            callback: Optional[callable] = None
        ) -> None:
        self.__active_operator = "decrement"
        try:
            callback()
        except TypeError:
            pass
        finally:
            window.destroy()

    def __save_profile_value(self, window: CTkToplevel) -> None:
        self.__profiles[self.__active_profile] = self.__profile_speed.get()
        self.__close_window(window)
        self.__update_profiles_file()

    def __run_profile(self) -> None:
        try:
            assert self.__active_profile
            run_window = CTkToplevel()
            run_window.geometry("300x100")
            run_window.title(f"Uruchomiono: {self.__active_profile}")
            run_window.transient(self)
            self.__center_window(window=run_window)
            self.__active_operator = "increment"
            self.__reach_current_profile_speed()
            run_stop_button = CTkButton(
                master=run_window,
                text="Zatrzymaj",
                command=lambda:
                    self.__close_window(
                        window=run_window,
                        callback=self.__reset_speed_value
                    ),
            )
            run_stop_button.place(relx=0.5, rely=0.5, anchor="center")
        except AssertionError:
            pass

    def __run_test_mode(self) -> None:
        test_window = CTkToplevel()
        test_window.geometry("300x200")
        test_window.title("Uruchomiono: tryb testowy")
        test_window.transient(self)
        self.__center_window(test_window)

        test_frame = CTkFrame(master=test_window)
        test_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.__test_speed.set(0)

        test_slider = CTkSlider(master=test_frame, from_=0, to=100, variable=self.__test_speed)
        test_slider.place(relx=0.5, rely=0.5, anchor="center")

        test_speed_box = CTkEntry(master=test_frame, textvariable=self.__test_speed_text)
        test_speed_box.place(relx=0.5, rely=0.25, anchor="center")

        test_stop_button = CTkButton(
            master=test_frame,
            text="Zatrzymaj",
            command=lambda:
                self.__close_window(
                    window=test_window,
                    callback=self.__reset_speed_value
                ),
        )
        test_stop_button.place(relx=0.5, rely=0.8, anchor="center")

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
        try:
            assert self.__active_profile
            value = self.combobox.get()
            del self.__profiles[value]
            self.combobox.configure(values=self.__list_profiles())
            self.combobox.set("")
            self.__update_profiles_file()
        except AssertionError:
            pass

    def __edit_profile(self) -> None:
        try:
            assert self.__active_profile
            edit_window = CTkToplevel()
            edit_window.geometry("300x200")
            edit_window.title(self.__active_profile)
            edit_window.transient(self)
            self.__center_window(edit_window)

            profile_frame = CTkFrame(master=edit_window)
            profile_frame.pack(pady=20, padx=20, fill="both", expand=True)

            profile_value = self.__profiles[self.__active_profile]

            profile_slider = CTkSlider(master=profile_frame, from_=0, to=100, variable=self.__profile_speed)
            profile_slider.place(relx=0.5, rely=0.5, anchor="center")
            profile_slider.set(profile_value)

            profile_speed_box = CTkEntry(master=profile_frame, textvariable=self.__profile_speed_text)
            profile_speed_box.place(relx=0.5, rely=0.25, anchor="center")

            profile_save_button = CTkButton(
                master=profile_frame,
                text="Zapisz",
                command=lambda: self.__save_profile_value(window=edit_window),
            )
            profile_save_button.place(relx=0.5, rely=0.8, anchor="center")
        except AssertionError:
            pass

    def __add_button(self, text: str, callback: callable) -> None:
        button = CTkButton(
            master=self,
            text=text,
            command=callback,
        )
        button.pack(**self.__button_padding, anchor="center")


if __name__ == "__main__":
    GUI()
