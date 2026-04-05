# Inky Gallery

Custom gallery for **Pimoroni Inky Frame**, aimed at 7.3 with **Raspberry Pi Pico 1/2 W**.

Official Inky Frame guide: **[Getting started with Inky Frame](https://learn.pimoroni.com/article/getting-started-with-inky-frame)**.

---

## Flashing firmware with Raspberry Pi Imager

1. **Download image**  
   Pimoroni MicroPython: [pimoroni/inky-frame](https://github.com/pimoroni/inky-frame/releases/latest)
   - Choose *'with-filesystem'* if you want bundled launcher and examples

2. **Bootloader mode**  
   With the USB cable disconnected, **hold the BOOT button**, then connect the USB. The board should appear as a USB drive
   - *If the drive doesn't show up on Windows but shows up in Device Manager, you may need to open Disk Management and assign it a drive letter*

3. **Flash the UF2**
  Drag-and-drop the .uf2 file onto the mounted drive, it will restart automatically

## Repository structure

- **`inky-gallery-v1/`**: earlier offline-only experiment
- **`inky-gallery-v2/`**: launcher with gallery offline/online modes
- **`inky-frame-original/`**: reference copy of stock launcher-style files