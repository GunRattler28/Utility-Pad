import board
import busio
import displayio
import terminalio
import rtc
import time
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
displayio.release_displays()

i2c = busio.I2C(board.D5, board.D4)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

r = rtc.RTC()

# Hard coded default time
r.datetime = time.struct_time((2026, 6, 25, 21, 21, 0, 0, -1, -1))

splash = displayio.Group()
text_area = label.Label(
    terminalio.FONT, 
    text="STARDANCE   00:00", 
    color=0xFFFF, 
    x=10, 
    y=15
)
splash.append(text_area)
display.root_group = splash

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

keyboard.pins = (board.D3, board.D6, board.D7, board.D8, board.D9, board.D10)

layers_encoder = EncoderHandler()
keyboard.modules.append(layers_encoder)
layers_encoder.pins = ((board.D0, board.D1, False),)

TASK_MANAGER = KC.LCTRL(KC.LSHIFT(KC.ESC))  # Ctrl + Shift + Esc
CLIPBOARD = KC.LWIN(KC.V)                   # Win + V
SCREENSHOT = KC.LWIN(KC.PSCR)               # Win + PrintScreen
LOCK_PC = KC.LWIN(KC.L)                     # Win + L (Lock Windows PC)
SHOW_DESKTOP = KC.LWIN(KC.D)                # Win + D
NVIDIA_RECORD = KC.LALT(KC.F2)              # Alt + F2

keyboard.keymap = [
    [
        TASK_MANAGER,  CLIPBOARD,     SCREENSHOT,
        LOCK_PC,       SHOW_DESKTOP,  NVIDIA_RECORD,
        KC.AUDIO_MUTE, 
    ]
]

layers_encoder.map = [
    ( (KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN), )
]

last_time = time.monotonic()

def update_screen_clock():
    global last_time
    if time.monotonic() - last_time >= 1.0:
        last_time = time.monotonic()
        t = r.datetime
        time_string = f"{t.tm_hour:02d}:{t.tm_min:02d}"
        text_area.text = f"STARDANCE   {time_string}"

keyboard.before_matrix_scan.append(update_screen_clock)

if __name__ == '__main__':
    keyboard.go()