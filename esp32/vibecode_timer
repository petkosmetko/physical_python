from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time

# ============================
# Display / ST7735 wiring
# ============================
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(4), mosi=Pin(6), miso=Pin(5))
tft = TFT(spi, 2, 3, 7)
tft.initr()
tft.rgb(True)

W, H = tft.size()

# ============================
# Colors (RGB565)
# ============================
def rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

C_BLACK     = TFT.BLACK
C_WHITE     = TFT.WHITE
C_RED       = TFT.RED
C_GREEN     = TFT.GREEN
C_BLUE      = TFT.BLUE
C_YELLOW    = TFT.YELLOW
C_CYAN      = TFT.CYAN
C_PURPLE    = TFT.PURPLE
C_DARKGREY  = rgb565(40, 40, 40)
C_LIGHTGREY = rgb565(180, 180, 180)

# ============================
# Buttons (PULL_UP) - Pressed = 0
# ============================
BTN_UP_PIN = 9
BTN_DOWN_PIN = 10
BTN_SELECT_PIN = 5

btn_up = Pin(BTN_UP_PIN, Pin.IN, Pin.PULL_UP)
btn_down = Pin(BTN_DOWN_PIN, Pin.IN, Pin.PULL_UP)
btn_sel = Pin(BTN_SELECT_PIN, Pin.IN, Pin.PULL_UP)

# ============================
# Debounced edge detection (fixed)
#
# Why v4 buttons "didn't work":
# In v4 we were still using your "sleep then confirm" method,
# but the app also sleeps in other places and redraws; short presses
# can be missed depending on loop timing.
#
# This version uses a non-blocking debounce with a latch:
# - you can press briefly and it will still be captured
# - no time.sleep_ms() inside the button read path
# ============================
class DebouncedButton:
    def __init__(self, pin, debounce_ms=50):
        self.pin = pin
        self.debounce_ms = debounce_ms
        self.stable = pin.value()         # last stable state
        self.last_raw = self.stable       # last raw read
        self.last_change = time.ticks_ms()
        self._press_event = False

    def update(self):
        raw = self.pin.value()
        now = time.ticks_ms()

        if raw != self.last_raw:
            self.last_raw = raw
            self.last_change = now

        # If raw has stayed the same long enough, accept it as stable
        if time.ticks_diff(now, self.last_change) >= self.debounce_ms:
            if self.stable != raw:
                self.stable = raw
                if self.stable == 0:     # pressed (pull-up)
                    self._press_event = True

    def fell(self):
        # Consume one press event
        if self._press_event:
            self._press_event = False
            return True
        return False

up = DebouncedButton(btn_up)
down = DebouncedButton(btn_down)
sel = DebouncedButton(btn_sel)

# ============================
# App state
# ============================
MODE_CLOCK = 0
MODE_MENU = 1
MODE_STOPWATCH = 2
MODE_TIMER = 3
MODE_SETTINGS = 4

mode = MODE_CLOCK

ui_color = C_WHITE
ui_scale = 2  # 1..4

timer_running = False
timer_total_s = 25 * 60
timer_end_ticks = None

POMO_WORK_S = 25 * 60
POMO_BREAK_S = 5 * 60

sw_running = False
sw_start_ticks = 0
sw_elapsed_ms = 0

menu_items = [
    "Pomodoro: Start Work",
    "Pomodoro: Start Break",
    "Custom Timer: +1 min (demo)",
    "Stopwatch",
    "Settings",
    "Back"
]
menu_index = 0
custom_total_s = 25 * 60

settings_field = 0  # 0=color, 1=scale

# ============================
# Drawing helpers (low flicker)
# ============================
def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def draw_text(x, y, text, color, scale):
    tft.text((x, y), text, color, sysfont, scale, nowrap=True)

def clear_rect(x, y, w, h):
    tft.fillrect((x, y), (w, h), C_BLACK)

def center_x_for_text(text, scale):
    est_char_w = 8
    text_w = len(text) * est_char_w * scale
    return max(0, (W - text_w) // 2)

def draw_header(title):
    tft.fillrect((0, 0), (W, 20), C_BLACK)
    draw_text(2, 2, title, C_CYAN, 1)
    tft.hline((0, 19), W, C_DARKGREY)

def fmt_mm_ss(total_s):
    if total_s < 0:
        total_s = 0
    m = total_s // 60
    s = total_s % 60
    return "{:02d}:{:02d}".format(m, s)

# ============================
# Screen layout + incremental redraw state
# ============================
last_mode = None

CLOCK_Y = (H // 2) - 20
clock_last = None

TIMER_TIME_Y = (H // 2) - 18
timer_last = None
timer_status_last = None

SW_TIME_Y = (H // 2) - 10
sw_last = None

menu_last_index = None
settings_last = None

def draw_clock_static():
    tft.fill(C_BLACK)
    draw_text(2, H - 18, "SEL=Menu", C_GREEN, 1)

def update_clock_dynamic():
    global clock_last
    now_s = time.ticks_ms() // 1000
    mm = (now_s // 60) % 100
    ss = now_s % 60

    main = "{:02d}:".format(mm)
    sec = "{:02d}".format(ss)
    combined = main + sec
    if combined == clock_last:
        return
    clock_last = combined

    big_scale = clamp(ui_scale + 1, 2, 4)
    small_scale = clamp(ui_scale - 1, 1, 3)

    clear_rect(0, CLOCK_Y - 4, W, 60)

    x_main = center_x_for_text(combined, big_scale)
    draw_text(x_main, CLOCK_Y, main, ui_color, big_scale)

    x_sec = x_main + len(main) * 8 * big_scale
    draw_text(x_sec, CLOCK_Y + (8 * (big_scale - small_scale)), sec, C_YELLOW, small_scale)

def draw_menu_static():
    tft.fill(C_BLACK)
    draw_header("Menu (UP/DOWN, SEL)")

def draw_menu_list():
    global menu_last_index
    if menu_last_index == menu_index:
        return
    menu_last_index = menu_index

    clear_rect(0, 22, W, H - 22)

    y0 = 28
    line_h = 18
    for i, item in enumerate(menu_items):
        y = y0 + i * line_h
        if y > H - 10:
            break
        if i == menu_index:
            tft.fillrect((0, y - 2), (W, line_h), C_DARKGREY)
            draw_text(4, y, "> " + item, C_WHITE, 1)
        else:
            draw_text(4, y, "  " + item, C_LIGHTGREY, 1)

def draw_stopwatch_static():
    tft.fill(C_BLACK)
    draw_header("Stopwatch (SEL=Start/Stop)")
    draw_text(2, H - 18, "UP=Reset  DOWN=Back", C_GREEN, 1)

def update_stopwatch_dynamic():
    global sw_last
    ms = sw_elapsed_ms
    if sw_running:
        ms = sw_elapsed_ms + time.ticks_diff(time.ticks_ms(), sw_start_ticks)

    total_s = ms // 1000
    mm = (total_s // 60) % 100
    ss = total_s % 60
    cs = (ms % 1000) // 10
    txt = "{:02d}:{:02d}.{:02d}".format(mm, ss, cs)
    if txt == sw_last:
        return
    sw_last = txt

    clear_rect(0, SW_TIME_Y - 8, W, 40)
    x = center_x_for_text(txt, 2)
    draw_text(x, SW_TIME_Y, txt, ui_color, 2)

def draw_timer_static():
    tft.fill(C_BLACK)
    draw_header("Timer (SEL=Start/Stop)")
    draw_text(2, H - 18, "UP=Reset  DOWN=Back", C_GREEN, 1)

def update_timer_dynamic():
    global timer_last, timer_status_last

    if timer_running and timer_end_ticks is not None:
        remaining_ms = time.ticks_diff(timer_end_ticks, time.ticks_ms())
        remaining_s = remaining_ms // 1000
    else:
        remaining_s = timer_total_s

    txt = fmt_mm_ss(remaining_s)
    status = "Running" if timer_running else "Paused"

    if txt != timer_last:
        timer_last = txt
        clear_rect(0, TIMER_TIME_Y - 8, W, 60)
        x = center_x_for_text(txt, 3)
        draw_text(x, TIMER_TIME_Y, txt, ui_color, 3)

    if status != timer_status_last:
        timer_status_last = status
        clear_rect(0, H - 40, W, 18)
        draw_text(2, H - 40, status, C_YELLOW, 1)

def draw_settings_static():
    tft.fill(C_BLACK)
    draw_header("Settings")
    draw_text(4, 86, "SEL next field", C_GREEN, 1)
    draw_text(4, 102, "DOWN back to menu", C_GREEN, 1)

def update_settings_dynamic():
    global settings_last
    snap = (settings_field, ui_scale, ui_color)
    if snap == settings_last:
        return
    settings_last = snap

    clear_rect(0, 22, W, H - 22)

    field_name = "Color" if settings_field == 0 else "Scale"
    draw_text(4, 30, "Field: " + field_name, C_LIGHTGREY, 1)
    draw_text(4, 50, "UP changes value", C_LIGHTGREY, 1)
    draw_text(4, 66, "Scale: {}".format(ui_scale), C_LIGHTGREY, 1)
    draw_text(4, 120, "Sample", ui_color, ui_scale)

def enter_mode(new_mode):
    global mode, last_mode
    global clock_last, timer_last, timer_status_last, sw_last, menu_last_index, settings_last
    mode = new_mode
    last_mode = None  # force static redraw

    clock_last = None
    timer_last = None
    timer_status_last = None
    sw_last = None
    menu_last_index = None
    settings_last = None

def start_timer(seconds):
    global timer_total_s, timer_running, timer_end_ticks
    timer_total_s = int(seconds)
    timer_running = True
    timer_end_ticks = time.ticks_add(time.ticks_ms(), timer_total_s * 1000)

def stop_timer():
    global timer_running, timer_total_s, timer_end_ticks
    if timer_running and timer_end_ticks is not None:
        remaining_ms = time.ticks_diff(timer_end_ticks, time.ticks_ms())
        timer_total_s = max(0, remaining_ms // 1000)
    timer_running = False
    timer_end_ticks = None

def reset_timer():
    global timer_running, timer_end_ticks
    timer_running = False
    timer_end_ticks = None

def sw_toggle():
    global sw_running, sw_start_ticks, sw_elapsed_ms
    if sw_running:
        sw_elapsed_ms = sw_elapsed_ms + time.ticks_diff(time.ticks_ms(), sw_start_ticks)
        sw_running = False
    else:
        sw_start_ticks = time.ticks_ms()
        sw_running = True

def sw_reset():
    global sw_running, sw_start_ticks, sw_elapsed_ms
    sw_running = False
    sw_start_ticks = 0
    sw_elapsed_ms = 0

# ============================
# Main loop
# ============================
enter_mode(MODE_CLOCK)
draw_clock_static()
update_clock_dynamic()

last_tick = time.ticks_ms()

while True:
    # Update button debouncers every loop (non-blocking)
    up.update()
    down.update()
    sel.update()

    # Timer completion
    if mode == MODE_TIMER and timer_running and timer_end_ticks is not None:
        if time.ticks_diff(timer_end_ticks, time.ticks_ms()) <= 0:
            timer_running = False
            timer_end_ticks = None
            clear_rect(0, 22, W, H - 22)
            draw_text(center_x_for_text("DONE", 3), H // 2 - 10, "DONE", C_RED, 3)
            time.sleep_ms(800)
            draw_timer_static()
            update_timer_dynamic()

    # Input handling (now uses latched fell() events)
    if mode == MODE_CLOCK:
        if sel.fell():
            enter_mode(MODE_MENU)

    elif mode == MODE_MENU:
        if up.fell():
            menu_index = (menu_index - 1) % len(menu_items)
        elif down.fell():
            menu_index = (menu_index + 1) % len(menu_items)
        elif sel.fell():
            choice = menu_items[menu_index]
            if choice == "Pomodoro: Start Work":
                enter_mode(MODE_TIMER)
                start_timer(POMO_WORK_S)
            elif choice == "Pomodoro: Start Break":
                enter_mode(MODE_TIMER)
                start_timer(POMO_BREAK_S)
            elif choice == "Custom Timer: +1 min (demo)":
                custom_total_s += 60
                enter_mode(MODE_TIMER)
                start_timer(custom_total_s)
            elif choice == "Stopwatch":
                enter_mode(MODE_STOPWATCH)
            elif choice == "Settings":
                enter_mode(MODE_SETTINGS)
            elif choice == "Back":
                enter_mode(MODE_CLOCK)

    elif mode == MODE_STOPWATCH:
        if sel.fell():
            sw_toggle()
        elif up.fell():
            sw_reset()
        elif down.fell():
            enter_mode(MODE_MENU)

    elif mode == MODE_TIMER:
        if sel.fell():
            if timer_running:
                stop_timer()
            else:
                start_timer(timer_total_s)
        elif up.fell():
            reset_timer()
        elif down.fell():
            stop_timer()
            enter_mode(MODE_MENU)

    elif mode == MODE_SETTINGS:
        if down.fell():
            enter_mode(MODE_MENU)
        elif sel.fell():
            settings_field = (settings_field + 1) % 2
        elif up.fell():
            if settings_field == 0:
                palette = [C_WHITE, C_YELLOW, C_GREEN, C_CYAN, C_BLUE, C_PURPLE, C_RED]
                idx = palette.index(ui_color) if ui_color in palette else 0
                ui_color = palette[(idx + 1) % len(palette)]
            else:
                ui_scale = clamp(ui_scale + 1, 1, 4)

    # Static redraw on mode change
    if mode != last_mode:
        last_mode = mode
        if mode == MODE_CLOCK:
            draw_clock_static()
            update_clock_dynamic()
        elif mode == MODE_MENU:
            draw_menu_static()
            draw_menu_list()
        elif mode == MODE_STOPWATCH:
            draw_stopwatch_static()
            update_stopwatch_dynamic()
        elif mode == MODE_TIMER:
            draw_timer_static()
            update_timer_dynamic()
        elif mode == MODE_SETTINGS:
            draw_settings_static()
            update_settings_dynamic()

    # Dynamic refresh tick
    now = time.ticks_ms()
    if time.ticks_diff(now, last_tick) >= 100:
        last_tick = now
        if mode == MODE_CLOCK:
            update_clock_dynamic()
        elif mode == MODE_MENU:
            draw_menu_list()
        elif mode == MODE_STOPWATCH:
            update_stopwatch_dynamic()
        elif mode == MODE_TIMER:
            update_timer_dynamic()
        elif mode == MODE_SETTINGS:
            update_settings_dynamic()

    time.sleep_ms(10)
