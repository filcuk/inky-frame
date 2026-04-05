import gc
import time

import inky_helper as ih
from inky_frame import BLUE, GREEN, WHITE
from machine import reset
from picographics import PicoGraphics

# Match your hardware / firmware (7.3" colour = Spectra).

# secrets.py on device:
# WIFI_SSID = "..."
# WIFI_PASSWORD = "..."
from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY
# from picographics import DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY  # Newer 2025 revision

# Give USB time to initialise
time.sleep(0.5)

graphics = PicoGraphics(DISPLAY)
WIDTH, HEIGHT = graphics.get_bounds()
graphics.set_font("bitmap8")

network_online = False

def launcher():
    ih.led_warn.off()

    if HEIGHT == 448:
        y_offset = 20
    elif HEIGHT == 480:
        y_offset = 35
    else:
        y_offset = 0

    # Draw the menu
    graphics.set_pen(WHITE)
    graphics.clear()

    ## Title
    graphics.set_pen(BLACK)
    graphics.rectangle(0, 0, WIDTH, 50)
    graphics.set_pen(WHITE)
    title = "Inky Gallery"
    title_len = graphics.measure_text(title, 4) // 2
    graphics.text(title, (WIDTH // 2 - title_len), 10, WIDTH, 4)

    graphics.set_pen(GREEN)
    graphics.rectangle(30, HEIGHT - (340 + y_offset), WIDTH - 100, 50)
    graphics.set_pen(1)
    graphics.text("A. Offline (SD card)", 35, HEIGHT - (325 + y_offset), 600, 3)

    graphics.set_pen(BLUE)
    graphics.rectangle(30, HEIGHT - (280 + y_offset), WIDTH - 150, 50)
    graphics.set_pen(1)
    graphics.text("B. Online (GitHub sync)", 35, HEIGHT - (265 + y_offset), 600, 3)

    graphics.set_pen(1)
    note = "Hold A + E, then press Reset, to return here"
    note_len = graphics.measure_text(note, 2) // 2
    graphics.text(note, (WIDTH // 2 - note_len), HEIGHT - 30, 600, 2)

    ih.led_warn.on()
    graphics.update()
    ih.led_warn.off()

    # Now we've drawn the menu to the screen, we wait here for the user to select an app.
    # Then once an app is selected, we set that as the current app and reset the device and load into it.

    while True:
        if ih.inky_frame.button_a.read():
            ih.inky_frame.button_a.led_on()
            ih.update_state("gallery_offline")
            time.sleep(0.5)
            reset()
        if ih.inky_frame.button_b.read():
            if not network_online:
                time.sleep(0.3)
                continue
            ih.inky_frame.button_b.led_on()
            ih.update_state("gallery_online")
            time.sleep(0.5)
            reset()


ih.clear_button_leds()
ih.led_warn.off()

# Load WiFi credentials and attempt to connect
try:
    from gallery_config import WIFI_PASSWORD, WIFI_SSID

    ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
    network_online = network.WLAN(network.STA_IF).status() == 3
except ImportError:
    print("Add WiFi credentials to gallery_config.py")

if ih.inky_frame.button_a.read() and ih.inky_frame.button_e.read():
    launcher()

ih.clear_button_leds()

if ih.file_exists("state.json"):
    ih.load_state()
    ih.launch_app(ih.state["run"])
    ih.app.graphics = graphics
    ih.app.WIDTH = WIDTH
    ih.app.HEIGHT = HEIGHT
else:
    launcher()

gc.collect()

while True:
    ih.app.update()
    ih.led_warn.on()
    ih.app.draw()
    ih.led_warn.off()
    ih.sleep(ih.app.UPDATE_INTERVAL)
