#!/usr/bin/env python3
"""
detect_esp32.py

Lists all serial ports and calls out any that look like an ESP32 development board.
You need pyserial: pip install pyserial
"""

import serial.tools.list_ports

# Common USB<->Serial adapter VID/PID combos for ESP32 boards:
ESP32_VID_PID = {
    # Silicon Labs CP210x
    "10c4:ea60",
    # WCH CH340
    "1a86:7523",
    # FTDI FT232R
    "0403:6015",
    # sometimes seen on older Espressif dev boards
    "303a:1001",
}

# Keywords often in the description for ESP32 devkits
ESP32_DESC_KEYS = (
    "cp210",
    "ch340",
    "ftdi",
    "usb-serial",
    "esp32",
)


def find_ports():
    return list(serial.tools.list_ports.comports())


def looks_like_esp32(port):
    # build a vid:pid string if possible
    vid_pid = ""
    if port.vid is not None and port.pid is not None:
        vid_pid = f"{port.vid:04x}:{port.pid:04x}".lower()

    # check VID/PID first
    if vid_pid in ESP32_VID_PID:
        return True

    # fallback to description/hwid keywords
    low_desc = port.description.lower()
    low_hwid = port.hwid.lower()
    for key in ESP32_DESC_KEYS:
        if key in low_desc or key in low_hwid:
            return True

    return False


def main():
    ports = find_ports()
    print("All serial ports:\n")
    for p in ports:
        vid_pid = f"{p.vid:04x}:{p.pid:04x}" if p.vid and p.pid else "----"
        print(f"  {p.device:8}  {vid_pid:9}  {p.description}")

    suspects = [p for p in ports if looks_like_esp32(p)]
    if suspects:
        print("\nLikely ESP32 port(s):")
        for p in suspects:
            print(f"  → {p.device} ({p.description})\n\n")
    else:
        print("\nNo ESP32-like ports detected.\n\n")

if __name__ == "__main__":
    main()
