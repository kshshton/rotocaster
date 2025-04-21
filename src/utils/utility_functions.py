import logging
import socket
import winsound
from tkinter import IntVar, StringVar

from customtkinter import CTk, CTkToplevel


class UtilityFunctions:
    @staticmethod
    def center_window(master: CTk) -> None:
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = int((screen_width - master.winfo_reqwidth()) / 2)
        y = int((screen_height - master.winfo_reqheight()) / 2)

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

    @staticmethod
    def close_window(master: CTkToplevel) -> None:
        master.destroy()

    def sound_effect(duration=2000, freq=440) -> None:
        winsound.Beep(freq, duration)

    @staticmethod
    def send_message_to_board(message: str) -> None:
        pico_ip = '192.168.4.1'  # The IP address of the Access Point
        port = 12345
        try:
            # Create a UDP socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(message.encode('utf-8'), (pico_ip, port))
                logging.info(f"Sent {message} message to Pico W at {pico_ip}")
        except Exception as e:
            logging.error(f"Error: {e}")
