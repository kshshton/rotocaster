import asyncio
import json
import logging
import os
import socket
import winsound
from tkinter import IntVar, StringVar

from customtkinter import CTk, CTkToplevel
from playwright.async_api import async_playwright


class UtilityFunctions:
    __SESSION_FILE = "whatsapp.session"

    @staticmethod
    def center_window(master: CTk, window_geometry: str) -> None:
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x, y = (int(num) for num in window_geometry.split("x"))
        x = int((screen_width - master.winfo_reqwidth()) / 2 - x / 4)
        y = int((screen_height - master.winfo_reqheight()) / 2 - y / 5)

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

    @staticmethod
    async def save_whatsapp_session():
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=UtilityFunctions.__SESSION_FILE,
                headless=False
            )
            page = await context.new_page()
            await page.goto('https://web.whatsapp.com')
            await page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=60000)
            await context.close()

    @staticmethod
    async def send_whatsapp_message():
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=UtilityFunctions.__SESSION_FILE,
                args=["--window-position=-32000,-32000"],
                headless=False,
            )
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto('https://web.whatsapp.com')
            await page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=60000)
            await page.fill('div[contenteditable="true"][data-tab="3"]', "(Ty)")
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            await page.fill('div[contenteditable="true"][data-tab="10"]', "Maszyna skończyła pracę!")
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            await context.close()

    @staticmethod
    def send_message_to_board(message: str) -> None:
        """
        message: string sent on microcontroller
        pico_ip: IP Address of Access Point
        port: Port of Access Point
        """
        with open("settings.json", "r") as file:
            config = json.load(file)
            access_point = config["accessPoint"]
        try:
            # Create a UDP socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(message.encode('utf-8'),
                         (access_point["address"], access_point["port"]))
                logging.info(
                    f"Sent {message} message to Pico W at {access_point["address"]}")
        except Exception as e:
            logging.error(f"Error: {e}")
