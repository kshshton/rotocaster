import socket

import network
from machine import PWM, Pin

ssid = "Pico_W_AP"
password = "__ur_password__"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)
print(f"Access Point running as: {ssid}")

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("0.0.0.0", 12345))

STBY = Pin(10, Pin.OUT)
AIN1 = Pin(12, Pin.OUT)
AIN2 = Pin(13, Pin.OUT)
PWMA = PWM(Pin(11))

# Set PWM on 1000Hz
PWMA.freq(1000)

# Activate driver
STBY.value(1)


def forward(speed) -> None:
    speed = max(0, min(int(speed), 100))  # speed range 0-100
    AIN1.value(1)
    AIN2.value(0)
    PWMA.duty_u16(int((speed / 100) * 65535))


def backward(speed) -> None:
    speed = max(0, min(int(speed), 100))
    AIN1.value(0)
    AIN2.value(1)
    PWMA.duty_u16(int((speed / 100) * 65535))


while True:
    bytes, _ = udp_socket.recvfrom(1024)
    message = bytes.decode("utf-8").strip()
    command, value = message.split(":")

    if command == "settings":
        print(value)
        pairs = [declaration.split('=') for declaration in value.split(';')]
        for pair in pairs:
            name, value = pair
            if name == "STBY":
                STBY = Pin(int(value), Pin.OUT)
                STBY.value(1)
            elif name == "AIN1":
                AIN1 = Pin(int(value), Pin.OUT)
            elif name == "AIN2":
                AIN2 = Pin(int(value), Pin.OUT)
            elif name == "PWMA":
                PWMA = PWM(Pin(int(value)))
                PWMA.freq(1000)

    if command == "engine":
        direction, speed = value.split(";")
        print(speed)
        if direction == "LEWO":
            forward(speed)
        elif direction == "PRAWO":
            backward(speed)
