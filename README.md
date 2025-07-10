# ticker32

**ticker32** is a beginner-friendly ESP32-S3 project that displays live and 1-hour price trends for any cryptocurrency (available on CoinGheko) on a 1.8″ Waveshare AMOLED touchscreen.

### Current Release  
**Version:** 1.0.0

#### Features
- **Live price & trend**: current price, 1-hour average, percentage change, and a 13-point mini-graph  
- **Touch control**: tap the screen to adjust brightness  
- **Built-in clock & Wi-Fi status**: see local time and signal strength at a glance  

---

### Setup

#### 1. Required Hardware
- **Waveshare 1.8″ AMOLED display**  
  [Product page](https://www.waveshare.com/esp32-s3-touch-amoled-1.8.htm)  
- **microSD card**
- **USB cable** (USB-C to USB-A power)  
- **3D-printed base** (`base.stl`, 100% scale, no supports)

#### 2. microSD Card Configuration
1. **Format** the card as **FAT32**  
2. **Create** a `config.json` file in the root directory:
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
     "DEBUG_DOT":          1
   }
   ```
   - Use any valid CoinGecko `coin_id` (e.g., `"ethereum"`, `"dogecoin"`, `"pi-network"`).  
   - Supported `vs_currency` values include `"usd"`, `"eur"`, etc.

3. **Insert** the card into the ESP32’s microSD slot.

#### 3. Flash the Firmware
1. Install Python 3 and required tools:
   ```bash
   pip install esptool pyserial
   ```
2. Make sure `flash.py` and `firmware-X.X.X.bin` are in the root folder.  
3. Run the flashing script:
   ```bash
   python flash.py
   ```

#### 4. Assembly & Power
1. **Print** `base.stl` using PLA or ABS (0.2mm layer height)  
2. **Insert** the microSD card  
3. **Connect** the USB cable to power the ESP32  
4. **Press-fit** the display into the base.  

#### 5. First Boot & Operation
- On boot, a splash screen shows Wi-Fi, NTP, and API status.  
- In the main view, **tap** the screen to adjust brightness.

---

### Support This Project

☕ Found this project useful? [Buy me a coffee on Ko-fi](https://ko-fi.com/vumaq) to support future updates!
