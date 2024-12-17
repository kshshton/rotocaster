from typing import Optional

from customtkinter import (CTk, CTkButton, CTkEntry, CTkSlider, CTkToplevel,
                           IntVar, StringVar)

from custom_components.custom_button import CustomButton
from custom_components.custom_combobox import CustomComboBox
from custom_components.custom_frame import CustomFrame
from custom_components.custom_top_level import CustomTopLevel
from profiles.profiles_file import ProfilesFile
from profiles.profiles_manager import ProfilesManager
from speed.speed_damper import SpeedDamper
from speed.speed_operator import SpeedOperator
from utils import Utils


class Master(CTk):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.geometry("300x300")
        self.title(title)
        Utils.center_window(self)
        self.__file = ProfilesFile(filename="profiles")
        self.__manager = ProfilesManager()
        self.__manager.profiles = self.__file.load()
        self.__damper = SpeedDamper()        

        self.combobox = CustomComboBox(
            master=self,
            values=self.__manager.list_profiles(),
            content=self.__manager.first_profile(),
            callback=self.__manager.select_profile        
        )

        CustomButton(master=self, text="Edytuj", callback=self.__edit_profile)
        CustomButton(master=self, text="Dodaj", callback=self.__add_profile)
        CustomButton(master=self, text="Usuń", callback=self.__delete_profile)
        CustomButton(master=self, text="Uruchom profil", callback=self.__run_profile)
        CustomButton(master=self, text="Uruchom tryb ręczny", callback=self.__run_manual_mode)

        self.__listen_output_speed()
        self.mainloop()

    def __listen_output_speed(self) -> None:
        print(self.__damper.actual_speed)
        self.after(ms=100, func=self.__listen_output_speed)

    def __slider_validation(self, input: StringVar, output: IntVar) -> None:
        try:
            value = int(input.get())
            if value > 100:
                output.set(100)
            else:
                output.set(value)
        except ValueError:
            output.set(0)

    def __text_to_speed(self, text: StringVar, speed: IntVar) -> None:
        try:
            text.set(str(speed.get()))
        except ValueError:
            speed.set(0)

    def __manual_to_output_speed(self, *args: any) -> None:
        self.__damper.actual_speed = self.__manual_speed.get()

    def __close_window(
            self,
            window: CTkToplevel,
            callback: Optional[callable] = None
        ) -> None:
        self.__damper.speed_control(SpeedOperator.DECREMENT)
        try:
            callback()
        except TypeError:
            pass
        finally:
            window.destroy()

    def __save_button_event(self, master: CTkToplevel, value: int) -> None:
        self.__manager.active_profile_value = value
        self.__file.update(self.__manager.profiles)
        self.__close_window(master)

    def __run_profile(self) -> None:
        try:
            assert self.__manager.is_profile_active()
            run_window = CustomTopLevel(
                master=self,
                title=f"Uruchomiono: {self.__active_profile}",
                geometry="300x100"
            )
            Utils.center_window(master=run_window)
            self.__damper.speed_control(SpeedOperator.INCREMENT)
            run_stop_button = CTkButton(
                master=run_window,
                text="Zatrzymaj",
                command=lambda:
                    self.__close_window(
                        window=run_window,
                        callback=self.__damper.speed_control(SpeedOperator.DECREMENT)
                    ),
            )
            run_stop_button.place(relx=0.5, rely=0.5, anchor="center")
        except AssertionError:
            pass

    def __run_manual_mode(self) -> None:
        manual_window = CustomTopLevel(
            master=self,
            title="Uruchomiono: tryb ręczny",
        )
        manual_frame = CustomFrame(master=manual_window)

        self.__manual_speed = IntVar()
        self.__manual_speed_text = StringVar()
        self.__manual_speed.trace_add(
            "write",
            lambda *args: self.__text_to_speed(
                text=self.__manual_speed_text,
                speed=self.__manual_speed,
            )
        )
        self.__manual_speed_text.trace_add(
            "write",
            lambda *args: self.__slider_validation(
                input=self.__manual_speed_text,
                output=self.__manual_speed,
            )
        )
        self.__manual_speed.trace_add("write", self.__manual_to_output_speed)
        self.__manual_speed.set(0)

        manual_slider = CTkSlider(master=manual_frame, from_=0, to=100, variable=self.__manual_speed)
        manual_slider.place(relx=0.5, rely=0.5, anchor="center")

        manual_speed_box = CTkEntry(master=manual_frame, textvariable=self.__manual_speed_text)
        manual_speed_box.place(relx=0.5, rely=0.25, anchor="center")

        manual_stop_button = CTkButton(
            master=manual_frame,
            text="Zatrzymaj",
            command=lambda:
                self.__close_window(
                    window=manual_window,
                    callback=self.__damper.speed_control(SpeedOperator.DECREMENT)
                ),
        )
        manual_stop_button.place(relx=0.5, rely=0.8, anchor="center")

        self.__damper.actual_speed = self.__manual_speed.get()

    def __add_profile(self) -> None:
        try:
            name = self.combobox.get()
            assert not name in self.__manager.list_profiles()
            self.__manager.active_profile = name
            self.__manager.create_profile(name)
            self.combobox.configure(values=self.__manager.list_profiles())
            self.__edit_profile()
            self.__file.update(self.__manager.profiles)
        except AssertionError:
            pass

    def __delete_profile(self) -> None:
        try:
            assert self.__manager.is_profile_active()
            self.__manager.active_profile = self.combobox.get()
            del self.__manager.active_profile
            self.combobox.configure(values=self.__manager.list_profiles())
            self.combobox.set(self.__manager.first_profile())
            self.__file.update(self.__manager.profiles)
        except AssertionError:
            pass

    def __edit_profile(self) -> None:
        try:
            assert self.__manager.is_profile_active()
            window = CustomTopLevel(
                master=self, 
                title=self.__manager.active_profile
            )
            frame = CustomFrame(master=window)

            self.__speed = IntVar()
            self.__speed_text = StringVar()
            self.__speed.trace_add(
                "write",
                lambda *args: self.__text_to_speed(
                    text=self.__speed_text,
                    speed=self.__speed,
                )
            )
            self.__speed_text.trace_add(
                "write",
                lambda *args: self.__slider_validation(
                    input=self.__speed_text,
                    output=self.__speed,
                )
            )
            profile_value = self.__manager.active_profile_value
            self.__damper.current_profile_speed = profile_value

            slider = CTkSlider(master=frame, from_=0, to=100, variable=self.__speed)
            slider.place(relx=0.5, rely=0.5, anchor="center")
            slider.set(profile_value)

            speed_box = CTkEntry(master=frame, textvariable=self.__speed_text)
            speed_box.place(relx=0.5, rely=0.25, anchor="center")

            save_button = CTkButton(
                master=frame,
                text="Zapisz",
                command=lambda: self.__save_button_event(
                    master=window,
                    value=self.__speed.get()
                ),
            )
            save_button.place(relx=0.5, rely=0.8, anchor="center")
        except AssertionError:
            pass
