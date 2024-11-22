import tkinter as tk
import re
import pyperclip
import time
import threading

def format_mac_address(mac, format_style="colons"):
    """
    Format MAC address in various styles.
    :param mac: The input MAC address
    :param format_style: The format style - "colons", "dashes", "no_delimiters", "dot_separated"
    :return: Formatted MAC address
    """
    mac = re.sub(r'[^0-9A-Fa-f]', '', mac)  # Remove any non-hexadecimal characters
    if len(mac) != 12:  # Ensure it's a valid MAC address length
        return mac

    if format_style == "colons":
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))
    elif format_style == "dashes":
        return '-'.join(mac[i:i+2] for i in range(0, 12, 2))
    elif format_style == "no_delimiters":
        return mac
    elif format_style == "dot_separated":
        return '.'.join(mac[i:i+4] for i in range(0, 12, 4))
    return mac

def is_mac_address(text):
    """
    Check if the input text matches any MAC address format.
    """
    mac_patterns = [
        r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$',  # XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
        r'^[0-9A-Fa-f]{12}$',                        # XXXXXXXXXXXX
        r'^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$'    # XXXX.XXXX.XXXX
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
    # formatted_mac_label.config(text=f"Formatted MAC: {formatted_mac}")
    pyperclip.copy(formatted_mac)  # Copy formatted MAC to clipboard

def clipboard_listener():
    """
    Monitor the clipboard for MAC addresses and update the UI when detected.
    """
    prev_clipboard_content = ""
    while True:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != prev_clipboard_content and is_mac_address(current_clipboard_content):
            mac_entry.delete(0, tk.END)
            mac_entry.insert(0, current_clipboard_content)
            update_button_labels(current_clipboard_content)
            window.deiconify()  # Show the window
            prev_clipboard_content = current_clipboard_content
        time.sleep(1)

# Create the main application window
window = tk.Tk()
window.title("MAC Address Converter")
window.geometry("600x200")

# Create input box for MAC address
mac_entry_label = tk.Label(window, text="Detected MAC address:")
mac_entry_label.pack(pady=10)

mac_entry = tk.Entry(window, width=20)
mac_entry.pack(pady=10)

# Create buttons for various formatting options
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

colons_button = tk.Button(button_frame, text="XX:XX:XX:XX:XX:XX", command=lambda: on_button_click("colons"))
colons_button.grid(row=0, column=0, padx=5)

dashes_button = tk.Button(button_frame, text="XX-XX-XX-XX-XX-XX", command=lambda: on_button_click("dashes"))
dashes_button.grid(row=0, column=1, padx=5)

no_delimiters_button = tk.Button(button_frame, text="XXXXXXXXXXXX", command=lambda: on_button_click("no_delimiters"))
no_delimiters_button.grid(row=0, column=2, padx=5)

dot_separated_button = tk.Button(button_frame, text="XXXX.XXXX.XXXX", command=lambda: on_button_click("dot_separated"))
dot_separated_button.grid(row=0, column=3, padx=5)

# Label to show the formatted MAC
# formatted_mac_label = tk.Label(window, text="Formatted MAC will appear here.")
# formatted_mac_label.pack(pady=10)

# Function to handle the close event
def on_close():
    # formatted_mac_label.config(text="Formatted MAC will appear here.")  # Reset the label
    window.withdraw()  # Hide the window instead of closing it

# Bind the close event (window close button)
window.protocol("WM_DELETE_WINDOW", on_close)

# Hide the window initially
window.withdraw()

# Run the clipboard listener in a separate thread
listener_thread = threading.Thread(target=clipboard_listener)
listener_thread.daemon = True
listener_thread.start()

# Start the Tkinter event loop
window.mainloop()
