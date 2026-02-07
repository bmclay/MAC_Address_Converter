# Fedora Prerequisites
# sudo dnf install python3-tkinter

import tkinter as tk
from tkinter import font as tkfont
import re
import sys

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
    # Hide window after copying
    window.after(100, window.withdraw)


def convert_case():
    """
    Convert the case of the MAC address and copy to clipboard.
    """
    mac_address = mac_entry.get()
    formatted_mac = ""
    if mac_address.isupper():
        formatted_mac = mac_address.lower()
    else:
        formatted_mac = mac_address.upper()
    # Use Tkinter's clipboard instead of pyperclip to avoid focus stealing
    window.clipboard_clear()
    window.clipboard_append(formatted_mac)
    window.update()  # Ensure clipboard is updated
    # Hide window after copying
    window.after(100, window.withdraw)


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
        pady=8,
        cursor="hand2",
        relief=tk.FLAT,
    )

    # Hover effects
    def on_enter(e):
        button.config(bg=COLORS["button_hover"], fg=COLORS["primary_hover"])

    def on_leave(e):
        button.config(bg=COLORS["button_bg"], fg=COLORS["text"])

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    button.grid(row=row, column=column, padx=4, pady=4, sticky="ew")
    return button


def check_clipboard():
    """
    Monitor the clipboard for MAC addresses using Tkinter's native clipboard.
    This avoids focus stealing and screen flickering on Linux.
    """
    try:
        # Use Tkinter's clipboard_get() which doesn't steal focus
        current_clipboard_content = window.clipboard_get()

        # Check if clipboard content changed and is a MAC address
        if hasattr(check_clipboard, "prev_content"):
            prev_content = check_clipboard.prev_content
        else:
            prev_content = ""

        if current_clipboard_content != prev_content and is_mac_address(
            current_clipboard_content
        ):
            mac_entry.delete(0, tk.END)
            mac_entry.insert(0, current_clipboard_content)
            update_button_labels(current_clipboard_content)
            window.deiconify()  # Show the window
            check_clipboard.prev_content = current_clipboard_content
        elif current_clipboard_content != prev_content:
            # Update prev_content even if it's not a MAC address
            check_clipboard.prev_content = current_clipboard_content
    except tk.TclError:
        # Clipboard is empty or contains non-text data
        pass
    except Exception as e:
        # Log error but don't crash
        print(f"Clipboard check error: {e}", file=sys.stderr)

    # Schedule next check (500ms for good responsiveness without being aggressive)
    window.after(500, check_clipboard)


# Create the main application window
window = tk.Tk()

# Set WM_CLASS for Linux desktop environment icon matching
try:
    # Set the application name (first part of WM_CLASS)
    # This allows the desktop environment to match the window with the .desktop file
    window.tk.call('tk', 'appname', 'mac-address-converter')
    # Try to set the window class (second part of WM_CLASS)
    # This may fail on some Tk versions, but the appname alone is sufficient
    try:
        window.tk.call('wm', 'class', window._w, 'MacAddressConverter')
    except:
        pass  # Expected to fail on some Tk versions, appname is sufficient
except Exception as e:
    print(f"Could not set application name: {e}", file=sys.stderr)

window.title("MAC Address Converter")
window.resizable(False, False)
window_width = 620
window_height = 240
window.geometry(f"{window_width}x{window_height}")
window.configure(bg=COLORS["bg"])

# Set application icon
try:
    import os

    # Get the correct path for both development and PyInstaller bundled scenarios
    if getattr(sys, "frozen", False):
        # Running as compiled executable (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_path, "icon.png")

    if os.path.exists(icon_path):
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(True, icon)
    else:
        print(f"Icon not found at: {icon_path}", file=sys.stderr)
except Exception as e:
    print(f"Could not load icon: {e}", file=sys.stderr)

# Create main container
main_frame = tk.Frame(window, bg=COLORS["bg"])
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Card container for content
card = tk.Frame(
    main_frame,
    bg=COLORS["card_bg"],
    highlightthickness=1,
    highlightbackground=COLORS["border"],
)
card.pack(fill=tk.BOTH, expand=True)

card_inner = tk.Frame(card, bg=COLORS["card_bg"])
card_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Title
header_label = tk.Label(
    card_inner,
    text="MAC Address Converter",
    font=("Segoe UI", 12, "bold"),
    bg=COLORS["card_bg"],
    fg=COLORS["text"],
)
header_label.pack(pady=(0, 3))

# Subtitle
subtitle_label = tk.Label(
    card_inner,
    text="Select format to copy",
    font=("Segoe UI", 8),
    bg=COLORS["card_bg"],
    fg=COLORS["text_secondary"],
)
subtitle_label.pack(pady=(0, 10))

# MAC address input
entry_frame = tk.Frame(
    card_inner,
    bg=COLORS["input_bg"],
    highlightthickness=1,
    highlightbackground=COLORS["border"],
)
entry_frame.pack(pady=(0, 12))

mac_entry = tk.Entry(
    entry_frame,
    width=20,
    font=("Consolas", 11, "bold"),
    bg=COLORS["input_bg"],
    fg=COLORS["primary_hover"],
    insertbackground=COLORS["primary_hover"],
    bd=0,
    relief=tk.FLAT,
    justify="center",
)
mac_entry.pack(padx=12, pady=8)

# Format buttons in single row
button_frame = tk.Frame(card_inner, bg=COLORS["card_bg"])
button_frame.pack(pady=(0, 10), fill=tk.X)

# Configure grid columns to expand evenly
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)

colons_button = create_styled_button(
    button_frame, "XX:XX:XX:XX:XX:XX", lambda: on_button_click("colons"), 0, 0
)
dashes_button = create_styled_button(
    button_frame, "XX-XX-XX-XX-XX-XX", lambda: on_button_click("dashes"), 0, 1
)
no_delimiters_button = create_styled_button(
    button_frame, "XXXXXXXXXXXX", lambda: on_button_click("no_delimiters"), 0, 2
)
dot_separated_button = create_styled_button(
    button_frame, "XXXX.XXXX.XXXX", lambda: on_button_click("dot_separated"), 0, 3
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
    font=("Segoe UI", 9, "bold"),
    bd=0,
    padx=20,
    pady=6,
    cursor="hand2",
    relief=tk.FLAT,
)
convert_case_button.pack(fill=tk.X, padx=40)


def on_convert_enter(e):
    convert_case_button.config(bg=COLORS["primary_hover"], fg=COLORS["bg"])


def on_convert_leave(e):
    convert_case_button.config(bg=COLORS["primary"], fg=COLORS["text"])


convert_case_button.bind("<Enter>", on_convert_enter)
convert_case_button.bind("<Leave>", on_convert_leave)


# Function to handle the close event
def on_close():
    window.withdraw()  # Hide the window instead of closing it


# Bind the close event (window close button)
window.protocol("WM_DELETE_WINDOW", on_close)

# Hide the window initially
window.withdraw()

# Start clipboard monitoring using Tkinter's event loop (no threading needed)
# This runs every 500ms without stealing focus or causing flicker
window.after(500, check_clipboard)

# Start the Tkinter event loop
window.mainloop()
