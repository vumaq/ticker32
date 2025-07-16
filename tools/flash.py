#!/usr/bin/env python3
"""
flash.py

Detects an ESP32 serial port (if not given), then prompts and flashes firmware using esptool.
If no firmware path is given, defaults to the most recent v*.bin next to this script.
Filenames must be of the form:
    vMAJOR.MINOR.PATCH[-prerelease].YYYY.MM.DD.bin
If there are multiple matching files, uses the one with the highest semantic version
(and newest date if versions equal).
Usage:
    python flash.py [--port COM3] [--baud 115200] [--chip esp32s3]
                    [--address 0x0] [--verify] [--before default-reset]
                    [--after hard-reset] [firmware.bin]
"""
import sys
import os
import glob
import re

# Handle missing dependencies
try:
    import argparse
    import esptool
    import serial.tools.list_ports
except ImportError as e:
    missing = e.name if hasattr(e, 'name') else str(e).split()[-1]
    print(f"Error: Required library '{missing}' is not installed.")
    print("Please install it with: pip install esptool pyserial")
    sys.exit(1)

# Known ESP32 USB-serial VID:PID pairs and their driver info
ESP32_DRIVERS = {
    "10c4:ea60": (
        "Silicon Labs CP210x USB to UART Bridge VCP Drivers",
        "https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers"
    ),
    "1a86:7523": (
        "WCH CH340/CH341 Windows Drivers",
        "http://www.wch.cn/downloads/CH341SER_ZIP.html"
    ),
    "0403:6015": (
        "FTDI Virtual COM Port Drivers",
        "https://ftdichip.com/drivers/vcp-drivers/"
    ),
    "303a:1001": (
        "Espressif USB Driver",
        "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/windows-setup.html#install-usb-driver"
    ),
}
KNOWN_VIDS = set(ESP32_DRIVERS.keys())
ESP32_KEYWORDS = ("cp210", "ch340", "ftdi", "usb-serial", "esp32")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def suggest_drivers(ports):
    """Suggest drivers for any detected serial devices whose VID:PID is unknown."""
    unknown = set()
    for p in ports:
        if p.vid and p.pid:
            vidpid = f"{p.vid:04x}:{p.pid:04x}".lower()
            if vidpid not in KNOWN_VIDS:
                unknown.add(vidpid)
    if unknown:
        print("\nDetected USB serial devices with unrecognized VID:PID:")
        for up in unknown:
            print(f"  {up}")
            drv = ESP32_DRIVERS.get(up)
            if drv:
                print(f"    Suggested driver: {drv[0]} ({drv[1]})")
        print("If your ESP32 board isn’t recognized, install the appropriate driver above and reconnect the device.\n")


def detect_esp32_port():
    """Scan COM ports and return the first one likely to be an ESP32, or None."""
    ports = list(serial.tools.list_ports.comports())
    candidates = []
    for p in ports:
        vidpid = f"{p.vid:04x}:{p.pid:04x}".lower() if p.vid and p.pid else None
        desc = (p.description or "").lower()
        hwid = (p.hwid or "").lower()
        if vidpid in KNOWN_VIDS or any(key in desc or key in hwid for key in ESP32_KEYWORDS):
            candidates.append(p.device)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        print("Multiple ESP32-like ports found:")
        for idx, d in enumerate(candidates, 1):
            print(f"  {idx}: {d}")
        print("Using the first one by default.")
        return candidates[0]
    return None


def version_key(path):
    """
    Parse filenames like:
      vMAJOR.MINOR.PATCH[-prerelease].YYYY.MM.DD.bin
    and return a tuple:
      (major, minor, patch, stable_flag, YYYY, MM, DD)
    where stable_flag is 1 for no prerelease, 0 otherwise.
    """
    base = os.path.splitext(os.path.basename(path))[0]
    m = re.match(
        r'^v(\d+)\.(\d+)\.(\d+)(?:-([^\.]+))?\.(\d{4})\.(\d{2})\.(\d{2})$',
        base
    )
    if not m:
        return ()
    major, minor, patch, prerelease, year, month, day = m.groups()
    stable_flag = 1 if prerelease is None else 0
    return (
        int(major),
        int(minor),
        int(patch),
        stable_flag,
        int(year),
        int(month),
        int(day),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Flash firmware to ESP32 via esptool (auto-detect COM port)"
    )
    parser.add_argument('-p', '--port', help='Serial port (e.g. COM3 or /dev/ttyUSB0)')
    parser.add_argument('-b', '--baud', type=int, default=115200, help='Baud rate')
    parser.add_argument('-c', '--chip', default='esp32s3',
                        choices=['esp32', 'esp32s2', 'esp32s3'], help='Target chip')
    parser.add_argument('-a', '--address', default='0x0', help='Flash start address')
    parser.add_argument('--verify', action='store_true', help='Verify flash after writing')
    parser.add_argument('--before', default='default-reset', help='Reset method before flashing')
    parser.add_argument('--after', choices=['no-reset', 'soft-reset', 'hard-reset'],
                        default='hard-reset', help='Reset method after flashing')
    parser.add_argument('firmware', nargs='?', help='Path to firmware binary')
    args = parser.parse_args()

    # ─── Determine firmware path ──────────────────────────────────────────────────────
    if args.firmware:
        firmware = args.firmware
    else:
        pattern = os.path.join(SCRIPT_DIR, 'v*.bin')
        candidates = glob.glob(pattern)
        if not candidates:
            print("Error: No firmware files found matching 'v*.bin' in", SCRIPT_DIR)
            sys.exit(1)
        firmware = max(candidates, key=version_key)

    if not os.path.isfile(firmware):
        print(f"Error: firmware file '{firmware}' not found.")
        sys.exit(1)
    # ────────────────────────────────────────────────────────────────────────────────

    # Suggest drivers & detect port
    all_ports = list(serial.tools.list_ports.comports())
    suggest_drivers(all_ports)
    port = args.port or detect_esp32_port()
    if not port:
        print("Error: Could not auto-detect an ESP32 port. Please specify --port.")
        sys.exit(1)

    # Suggest driver for chosen port
    for p in all_ports:
        if p.device == port and p.vid and p.pid:
            vidpid = f"{p.vid:04x}:{p.pid:04x}".lower()
            drv = ESP32_DRIVERS.get(vidpid)
            if drv:
                print(f"Detected ESP32 port {port} uses VID:PID {vidpid}.\n"
                      f"Suggested driver: {drv[0]} ({drv[1]})\n")
            break

    # Build esptool command
    cmd = [
        '--chip', args.chip,
        '--port', port,
        '--baud', str(args.baud),
        '--before', args.before,
        '--after', args.after,
        'write-flash'
    ]
    if args.verify:
        cmd.append('--verify')
    cmd += [args.address, firmware]

    # Confirm & flash
    print(f"About to flash '{firmware}' to {port} ({args.chip} @ {args.baud}bps, address {args.address}).")
    print(f"Reset before: {args.before}, reset after: {args.after}.")
    if args.verify:
        print("Flash will be verified after writing.")
    resp = input("Proceed? [Y/n]: ").strip().lower()
    if resp not in ('', 'y', 'yes'):
        print("Flashing aborted.")
        sys.exit(0)

    print('Running esptool with:', ' '.join(cmd))
    try:
        ret = esptool.main(cmd)
    except SystemExit as e:
        ret = e.code if isinstance(e.code, int) else 0
    except Exception as e:
        print(f"Error during flashing: {e}")
        sys.exit(1)

    if ret in (None, 0):
        print("Flashing completed successfully.")
        sys.exit(0)
    else:
        print(f"Flashing failed with exit code {ret}.")
        sys.exit(ret)


if __name__ == '__main__':
    main()
