# ticker32

**ticker32** is a beginner-friendly ESP32-S3 project that displays live and 1-hour price trends for Pi Network’s PI coin on a 1.8″ Waveshare AMOLED touchscreen.

## Current Release
**Version:** 1\.0\.0

### Features
- **Live PI price & trend**: current PI price, 1-hour average, percentage change, plus a simple 13-point graph  
- **Touch control**: tap the screen to adjust brightness  
- **Built-in clock & Wi-Fi status**: see local time and signal strength at a glance

---

## Setup
#### 1. Required Hardware
- **Waveshare 1.8″ AMOLED display**
- **microSD card** (≥4 GB) & SD adapter  
- **USB cable** (USB-C to USB-A, data & power)  
- **3D-printed base** (`base.stl`, 100% scale, no supports)

#### 2. microSD Card Configuration
1. **Format** the card as **FAT32**.  
2. **Create** a file named `config.json` in the root folder with your settings. Example:
   ```json
   {
     "SSID":               "YourNetwork",
     "PASSWORD":           "YourPassword",
     "TZ_INFO":            "NZST-12NZDT-13:00:00,M9.5.0/02:00:00,M4.1.0/03:00:00",
     "NTP1":               "pool.ntp.org",
     "NTP2":               "time.nist.gov",
     "THEME_ENABLED":      true,
     "THEME_BG":           "0x48C8",
     "THEME_HL":           "0xF441",
     "DEFAULT_BRIGHTNESS": 80,
     "BRIGHTNESS_STEP":    10,
     "COIN_ID":            "pi-network",
     "VS_CURRENCY":        "usd",
     "HISTORY_DAYS":       1,
     "DEBUG_DOT":          1
   }
   ```
3. **Insert** the microSD card into the ESP32’s SD slot.

#### 3. Flash the Firmware
1. Install Python 3 and dependencies:
   ```bash
   pip install esptool pyserial
   ```
2. Ensure `flash.py` and `firmware.bin` are in the project root.  
3. Run:
   ```bash
   python flash.py
   ```
   This auto-detects your ESP32-S3 port and flashes at 115200 baud (use `--help` for options).

#### 4. Assembly & Power
1. **Print** `base.stl` on your 3D printer (PLA/ABS, 0.2 mm layer height).  
2. **Insert** the formatted microSD card.
3. **Connect** the USB-C cable between a power source and the ESP32.
4. **Press-fit** the display into the base.  

#### 5. First Boot & Adjustment
- The splash screen shows Wi-Fi, time-sync, and API status.  
- In the main view, **tap** the screen to adjust brightness.
