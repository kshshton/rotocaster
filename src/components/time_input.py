from customtkinter import CTkEntry, CTkFrame, CTkLabel, StringVar


class TimeInput(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.hours = StringVar()
        self.minutes = StringVar()
        self.seconds = StringVar()
        
        self.colon1 = CTkLabel(self, text="godz:")
        self.colon1.grid(row=0, column=0, padx=2)

        self.hour_entry = CTkEntry(
            self, 
            width=40, 
            textvariable=self.hours, 
            justify="center", 
            placeholder_text="HH"
        )
        self.hour_entry.grid(row=0, column=1, padx=5)        
        
        self.colon2 = CTkLabel(self, text="min: ")
        self.colon2.grid(row=0, column=2, padx=2)

        self.minute_entry = CTkEntry(
            self, 
            width=40, 
            textvariable=self.minutes, 
            justify="center", 
            placeholder_text="MM"
        )
        self.minute_entry.grid(row=0, column=3, padx=5)

        self.colon3 = CTkLabel(self, text="sek: ")
        self.colon3.grid(row=0, column=4, padx=2)
                
        self.second_entry = CTkEntry(
            self, 
            width=40, 
            textvariable=self.seconds, 
            justify="center", 
            placeholder_text="SS"
        )
        self.second_entry.grid(row=0, column=5, padx=5)
        
        self.hours.trace_add("write", self.validate_time)
        self.minutes.trace_add("write", self.validate_time)
        self.seconds.trace_add("write", self.validate_time)

    def validate_time(self, *args) -> bool:
        def is_valid_time(value, max):
            if not value.isdigit() or int(value) < 0 or int(value) > max:
                return False
            return True
        
        if not is_valid_time(self.hours.get(), 23):
            self.hours.set("")
        
        if not is_valid_time(self.minutes.get(), 59):
            self.minutes.set("")
        
        if not is_valid_time(self.seconds.get(), 59):
            self.seconds.set("")

    def update(self, time: str) -> None:
        hours, minutes, seconds = time.split(":")
        self.hours.set(hours)
        self.minutes.set(minutes)
        self.seconds.set(seconds)
        
    def __str__(self) -> str:
        hour = self.hours.get() or "0"
        minute = self.minutes.get() or "0"
        second = self.seconds.get() or "0"
        return f"{hour}:{minute}:{second}"
