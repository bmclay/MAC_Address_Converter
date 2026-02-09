# Fedora Prerequisites
# sudo dnf install python3-tkinter

# sample mac address: AA:BB:CC:DD:EE:FF

import tkinter as tk
from tkinter import font as tkfont
import re
import sys
import os
import platform

# Modern color scheme - sleek dark theme
COLORS = {
    "bg": "#1a1a1a",  # Deep dark background
    "card_bg": "#2d2d2d",  # Card/panel background
    "input_bg": "#3a3a3a",  # Input field background
    "text": "#ffffff",  # White text
    "text_secondary": "#a0a0a0",  # Gray text
    "primary": "#0d7377",  # Teal primary
    "primary_hover": "#14FFEC",  # Bright teal hover
    "button_bg": "#323941",  # Subtle dark gray
    "button_hover": "#3e4753",  # Lighter gray on hover
    "border": "#404040",  # Subtle borders
}

# Toast notification configuration
TOAST = {
    "width": 360,
    "height": 200,
    "taskbar_margin": 10,
    "slide_step_px": 8,
    "slide_interval_ms": 10,
    "auto_dismiss_ms": 5000,
}

# Platform detection
_os = platform.system()

# Animation and timer state
_animation_id = None
_dismiss_timer_id = None


def format_mac_address(mac, format_style="colons"):
    """
    Format MAC address in various styles.
    :param mac: The input MAC address
    :param format_style: The format style - "colons", "dashes", "no_delimiters", "dot_separated"
    :return: Formatted MAC address
    """
    mac = re.sub(r"[^0-9A-Fa-f]", "", mac)  # Remove any non-hexadecimal characters
    if len(mac) != 12:  # Ensure it's a valid MAC address length
        return mac

    if format_style == "colons":
        return ":".join(mac[i : i + 2] for i in range(0, 12, 2))
    elif format_style == "dashes":
        return "-".join(mac[i : i + 2] for i in range(0, 12, 2))
    elif format_style == "no_delimiters":
        return mac
    elif format_style == "dot_separated":
        return ".".join(mac[i : i + 4] for i in range(0, 12, 4))
    return mac


def is_mac_address(text):
    """
    Check if the input text matches any MAC address format.
    """
    mac_patterns = [
        r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$",  # XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
        r"^[0-9A-Fa-f]{12}$",  # XXXXXXXXXXXX
        r"^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$",  # XXXX.XXXX.XXXX
    ]
    return any(re.match(pattern, text) for pattern in mac_patterns)


def update_button_labels(mac):
    """
    Update the button text with the formatted MAC addresses.
    """
    colons_button.config(text=format_mac_address(mac, "colons"))
    dashes_button.config(text=format_mac_address(mac, "dashes"))
    no_delimiters_button.config(text=format_mac_address(mac, "no_delimiters"))
    dot_separated_button.config(text=format_mac_address(mac, "dot_separated"))


def on_button_click(format_style):
    """
    Handle button clicks to format the MAC address and copy to clipboard.
    """
    mac_address = mac_entry.get()
    formatted_mac = format_mac_address(mac_address, format_style)
    # Use Tkinter's clipboard instead of pyperclip to avoid focus stealing
    window.clipboard_clear()
    window.clipboard_append(formatted_mac)
    window.update()  # Ensure clipboard is updated
    window.after(100, dismiss_toast)


def convert_case():
    """
    Convert the case of the MAC address and copy to clipboard.
    """
    mac_address = mac_entry.get()
    if mac_address.isupper():
        formatted_mac = mac_address.lower()
    else:
        formatted_mac = mac_address.upper()
    # Use Tkinter's clipboard instead of pyperclip to avoid focus stealing
    window.clipboard_clear()
    window.clipboard_append(formatted_mac)
    window.update()  # Ensure clipboard is updated
    window.after(100, dismiss_toast)


def create_styled_button(parent, text, command, row=0, column=0):
    """
    Create a modern styled button with hover effects.
    """
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=COLORS["button_bg"],
        fg=COLORS["text"],
        activebackground=COLORS["button_hover"],
        activeforeground=COLORS["text"],
        font=("Consolas", 9),
        bd=0,
        padx=8,
        pady=6,
        cursor="hand2",
        relief=tk.FLAT,
    )

    def on_enter(e):
        button.config(bg=COLORS["button_hover"], fg=COLORS["primary_hover"])

    def on_leave(e):
        button.config(bg=COLORS["button_bg"], fg=COLORS["text"])

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    button.grid(row=row, column=column, padx=3, pady=3, sticky="ew")
    return button


def get_toast_position(offscreen=False):
    """
    Calculate bottom-right screen position for the toast.
    Returns (x, y) coordinates.
    """
    toast_w = TOAST["width"]
    toast_h = TOAST["height"]
    margin = TOAST["taskbar_margin"]

    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()

    # On Windows, query the actual work area (excludes taskbar)
    if _os == "Windows":
        try:
            import ctypes
            from ctypes import wintypes

            rect = wintypes.RECT()
            ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
            screen_w = rect.right
            screen_h = rect.bottom
        except Exception:
            pass

    x = screen_w - toast_w - margin

    if offscreen:
        y = screen_h + toast_h
    else:
        y = screen_h - toast_h - margin

    return x, y


def slide_up():
    """Animate the toast sliding up from below the screen edge."""
    global _animation_id

    toast_w = TOAST["width"]
    toast_h = TOAST["height"]
    target_x, target_y = get_toast_position(offscreen=False)
    step = TOAST["slide_step_px"]
    interval = TOAST["slide_interval_ms"]

    # If toast is already visible and near its resting position, just reset timer
    if window.winfo_viewable():
        current_y = window.winfo_y()
        if abs(current_y - target_y) < step * 2:
            start_auto_dismiss_timer()
            return

    # Cancel any running animation
    if _animation_id is not None:
        window.after_cancel(_animation_id)
        _animation_id = None

    # Set initial offscreen position
    start_x, start_y = get_toast_position(offscreen=True)
    window.geometry(f"{toast_w}x{toast_h}+{start_x}+{start_y}")
    window.deiconify()

    def animate():
        global _animation_id
        current_y = window.winfo_y()
        if current_y <= target_y:
            window.geometry(f"{toast_w}x{toast_h}+{target_x}+{target_y}")
            _animation_id = None
            start_auto_dismiss_timer()
            return
        new_y = max(current_y - step, target_y)
        window.geometry(f"{toast_w}x{toast_h}+{target_x}+{new_y}")
        _animation_id = window.after(interval, animate)

    # Check if Wayland is ignoring position requests
    window.update_idletasks()
    actual_y = window.winfo_y()
    if _os == "Linux" and actual_y == 0 and start_y > 0:
        # Compositor likely ignoring geometry - show without animation
        window.geometry(f"{toast_w}x{toast_h}+{target_x}+{target_y}")
        start_auto_dismiss_timer()
        return

    _animation_id = window.after(interval, animate)


def slide_down():
    """Animate the toast sliding down off screen, then withdraw."""
    global _animation_id

    toast_w = TOAST["width"]
    toast_h = TOAST["height"]
    screen_h = window.winfo_screenheight()
    step = TOAST["slide_step_px"]
    interval = TOAST["slide_interval_ms"]
    current_x = window.winfo_x()

    # Cancel any running animation
    if _animation_id is not None:
        window.after_cancel(_animation_id)
        _animation_id = None

    def animate():
        global _animation_id
        current_y = window.winfo_y()
        if current_y >= screen_h:
            window.withdraw()
            _animation_id = None
            return
        new_y = current_y + step
        window.geometry(f"{toast_w}x{toast_h}+{current_x}+{new_y}")
        _animation_id = window.after(interval, animate)

    _animation_id = window.after(interval, animate)


def start_auto_dismiss_timer():
    """Start or restart the auto-dismiss countdown."""
    global _dismiss_timer_id
    if _dismiss_timer_id is not None:
        window.after_cancel(_dismiss_timer_id)
    _dismiss_timer_id = window.after(TOAST["auto_dismiss_ms"], dismiss_toast)


def cancel_auto_dismiss_timer():
    """Cancel the auto-dismiss countdown (e.g., on mouse hover)."""
    global _dismiss_timer_id
    if _dismiss_timer_id is not None:
        window.after_cancel(_dismiss_timer_id)
        _dismiss_timer_id = None


def dismiss_toast():
    """Dismiss the toast with slide-down animation."""
    global _dismiss_timer_id
    if _dismiss_timer_id is not None:
        window.after_cancel(_dismiss_timer_id)
        _dismiss_timer_id = None
    slide_down()


def check_clipboard():
    """
    Monitor the clipboard for MAC addresses using Tkinter's native clipboard.
    This avoids focus stealing and screen flickering on Linux.
    """
    try:
        current_clipboard_content = window.clipboard_get()

        if hasattr(check_clipboard, "prev_content"):
            prev_content = check_clipboard.prev_content
        else:
            prev_content = ""

        if current_clipboard_content != prev_content and is_mac_address(
            current_clipboard_content
        ):
            mac_entry.config(state="normal")
            mac_entry.delete(0, tk.END)
            mac_entry.insert(0, current_clipboard_content)
            mac_entry.config(state="readonly")
            update_button_labels(current_clipboard_content)
            slide_up()
            check_clipboard.prev_content = current_clipboard_content
        elif current_clipboard_content != prev_content:
            check_clipboard.prev_content = current_clipboard_content
    except tk.TclError:
        pass
    except Exception as e:
        print(f"Clipboard check error: {e}", file=sys.stderr)

    window.after(500, check_clipboard)


# --- Window setup ---

window = tk.Tk()

# Set WM_CLASS for Linux desktop environment icon matching
try:
    window.tk.call("tk", "appname", "mac-address-converter")
    try:
        window.tk.call("wm", "class", window._w, "MacAddressConverter")
    except Exception:
        pass
except Exception as e:
    print(f"Could not set application name: {e}", file=sys.stderr)

window.title("MAC Address Converter")
window.overrideredirect(True)
window.resizable(False, False)
window.configure(bg=COLORS["border"])
window.attributes("-topmost", True)

# Platform-specific window hints
if _os == "Linux":
    try:
        window.attributes("-type", "notification")
    except tk.TclError:
        pass

# Set application icon
try:
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_path, "assets", "icon.png")
    if getattr(sys, "frozen", False):
        icon_path = os.path.join(base_path, "icon.png")

    if os.path.exists(icon_path):
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(True, icon)
except Exception as e:
    print(f"Could not load icon: {e}", file=sys.stderr)


# --- Toast layout ---

# Border frame (1px border via background color showing through padding)
card = tk.Frame(window, bg=COLORS["card_bg"])
card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

card_inner = tk.Frame(card, bg=COLORS["card_bg"])
card_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

# Top row: title + close button
top_row = tk.Frame(card_inner, bg=COLORS["card_bg"])
top_row.pack(fill=tk.X, pady=(0, 4))

header_label = tk.Label(
    top_row,
    text="MAC Address Converter",
    font=("Segoe UI", 9, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text"],
    anchor="w",
)
header_label.pack(side=tk.LEFT)

close_button = tk.Label(
    top_row,
    text="X",
    font=("Consolas", 9, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text_secondary"],
    cursor="hand2",
    padx=4,
)
close_button.pack(side=tk.RIGHT)


def on_close_enter(e):
    close_button.config(fg=COLORS["primary_hover"])


def on_close_leave(e):
    close_button.config(fg=COLORS["text_secondary"])


close_button.bind("<Enter>", on_close_enter)
close_button.bind("<Leave>", on_close_leave)
close_button.bind("<Button-1>", lambda e: dismiss_toast())

# MAC address display (readonly entry)
mac_entry = tk.Entry(
    card_inner,
    width=22,
    font=("Consolas", 10, "bold"),
    bg=COLORS["input_bg"],
    fg=COLORS["primary_hover"],
    insertbackground=COLORS["primary_hover"],
    bd=0,
    relief=tk.FLAT,
    justify="center",
    state="readonly",
    readonlybackground=COLORS["input_bg"],
)
mac_entry.pack(pady=(0, 8), ipady=4)

# Format buttons in 2x2 grid
button_frame = tk.Frame(card_inner, bg=COLORS["card_bg"])
button_frame.pack(pady=(0, 6), fill=tk.X)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

colons_button = create_styled_button(
    button_frame, "XX:XX:XX:XX:XX:XX", lambda: on_button_click("colons"), 0, 0
)
dashes_button = create_styled_button(
    button_frame, "XX-XX-XX-XX-XX-XX", lambda: on_button_click("dashes"), 0, 1
)
no_delimiters_button = create_styled_button(
    button_frame, "XXXXXXXXXXXX", lambda: on_button_click("no_delimiters"), 1, 0
)
dot_separated_button = create_styled_button(
    button_frame, "XXXX.XXXX.XXXX", lambda: on_button_click("dot_separated"), 1, 1
)

# Convert case button
convert_case_button = tk.Button(
    card_inner,
    text="Convert Case",
    command=lambda: convert_case(),
    bg=COLORS["primary"],
    fg=COLORS["text"],
    activebackground=COLORS["primary_hover"],
    activeforeground=COLORS["bg"],
    font=("Segoe UI", 8, "bold"),
    bd=0,
    padx=12,
    pady=4,
    cursor="hand2",
    relief=tk.FLAT,
)
convert_case_button.pack(fill=tk.X, padx=20)


def on_convert_enter(e):
    convert_case_button.config(bg=COLORS["primary_hover"], fg=COLORS["bg"])


def on_convert_leave(e):
    convert_case_button.config(bg=COLORS["primary"], fg=COLORS["text"])


convert_case_button.bind("<Enter>", on_convert_enter)
convert_case_button.bind("<Leave>", on_convert_leave)

# Pause auto-dismiss when mouse is over the toast
window.bind("<Enter>", lambda e: cancel_auto_dismiss_timer())
window.bind("<Leave>", lambda e: start_auto_dismiss_timer())

# Safety net for WM_DELETE_WINDOW (shouldn't fire with overrideredirect, but just in case)
window.protocol("WM_DELETE_WINDOW", dismiss_toast)

# Set initial geometry offscreen and hide
toast_w = TOAST["width"]
toast_h = TOAST["height"]
start_x, start_y = get_toast_position(offscreen=True)
window.geometry(f"{toast_w}x{toast_h}+{start_x}+{start_y}")
window.withdraw()

# Start clipboard monitoring
window.after(500, check_clipboard)

# Start the Tkinter event loop
window.mainloop()
