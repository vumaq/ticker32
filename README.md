# ticker32

**ticker32** is a beginner-friendly ESP32-S3 project that displays live and 1-hour price trends for any cryptocurrency (available on CoinGecko) on a 1.8″ Waveshare AMOLED touchscreen.

### Current Release  
**Version:** 1.0.1

#### Features
- **Live price & trend**: current price, 1-hour average, percentage change, and a 13-point mini-graph  
- **Touch control**: tap the screen to adjust brightness  
- **Built-in clock & Wi-Fi status**: see local time and signal strength at a glance  

---

## Setup

### Parts and Tools Required

![Parts and Tools Required](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/parts.jpg?raw=true)

- **WAVESHARE ESP32-S3 1.8″ AMOLED Touch Display Development Board**  
  Available from: waveshare.com/esp32-s3-touch-amoled-1.8.htm [waveshare.com/esp32-s3-touch-amoled-1.8.htm](waveshare.com/esp32-s3-touch-amoled-1.8.htm)
- **Ticker32 3D printed power stand** (PETG)  
  The STL 3D print file is available free from:  [ticker32.com](https://ticker32.com) and [github.com/vumaq/ticker32](https://github.dev/vumaq/ticker32/)
- **NOTOW Elbow USB-A to USB-C 90° braided cable**  
  Available from AliExpress: [aliexpress.com/w/wholesale--notow-elbow-usb-to-type-c-90-degrees-braid.html](https://aliexpress.com/w/wholesale--notow-elbow-usb-to-type-c-90-degrees-braid.html)
- **Teaspoon or dessert spoon** with a handle that fits sideways into the cavity in the base.
- **Tube of CA glue** (optional)

### microSD Card Configuration
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

> **Note:** On boot, the Wi-Fi PASSWORD field is encrypted, copied to the device and removed from the microSD card. To change your Wi-Fi password afterward, re-add the PASSWORD key and it's new value to config json on the microSD card.


#### Flash the Firmware
1. Install Python 3 and required tools:  
   ```bash
   pip install esptool pyserial
   ```
2. Make sure `flash.py` and `firmware-X.X.X.bin` are in the root folder.  
3. Run the flashing script:  
   ```bash
   python flash.py
   ```

### Assembly Steps

| ![Fig 1](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig1.jpg?raw=true) | ![Fig 2](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig2.jpg?raw=true) | ![Fig 3](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig3.jpg?raw=true) |
|-------------------------------|-------------------------------|-------------------------------|
| ![Fig 4](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig4.jpg?raw=true) | ![Fig 5](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig5.jpg?raw=true) | ![Fig 6](https://github.com/vumaq/ticker32/blob/2f52a1c628bf5823aa7d4f3847caa8ab03c659d2/docs/images/fig6.jpg?raw=true) |

1. Turn the power stand upside down and observe the cable cavities (see Fig 1).  
2. Insert the USB-C (90°) end of the cable into the cavity in the base, with the metal connector protruding through the passthrough (see Fig 2).  
3. Using the spoon handle, gently press the USB-C plug forward and down into place (see Fig 3).  
4. Align the protruding metal part of the USB-C plug with the oblong hole on the inside of the power stand and adjust if necessary (see Fig 5).  
5. Press firmly on the back of the USB-C plug until it locks into place (see Fig 4).  
6. Ensure the plastic surrounding the metal connector is nearly flush with the bottom surface of the display guide (see Fig 5).  
7. Gently press the braided cable into the slot provided; the slot is designed to retain the cable without adhesives.  
8. Slide the Waveshare 1.8″ AMOLED display into the power stand using the rear guides; the USB-C plug should insert 3–4 mm without resistance, clicking into place when fully inserted (see Fig 6).

**Check your work!** Gently slide the WAVESHARE 1.8” OLED Display into the power stand using the rear guides, the USB-C plug should slide into the display about 3 to 4mm without any resistance, if not check your work, if correct the display will click into place when pressed down fully, see fig 6.

> **Note:** If the display fits correctly, you may optionally apply a small drop of CA glue to the back of the USB-C plug for extra security.

## Disclaimer
This 3D USB-C power stand design, including the associated STL file(s), is provided free of charge by our software development group **for informational and prototyping purposes only.**

- The **software team does not supply** any physical components, including the 3D-printed parts, USB-C cables, or other hardware.  
- Assembly and use of this USB-C power stand is performed **at your own risk.**  
- We make **no guarantees** regarding fit, function, durability, electrical safety, or compatibility with your specific hardware setup.  
- Always follow appropriate **electrical safety** and **mechanical stability** precautions when assembling or using custom hardware.  
- The provided STL files and associated design are for **personal and non-commercial use only**, unless otherwise stated.  
- By downloading or using the provided design files, you acknowledge that you are solely responsible for the correct and safe use of the components involved.

By downloading or using the provided design files, you acknowledge that you are solely responsible for the correct and safe use of the components involved.

---

## Support This Project

☕ Found this project useful? [Buy me a coffee on Ko-fi](https://ko-fi.com/vumaq) to support future updates!
