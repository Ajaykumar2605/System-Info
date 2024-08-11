import tkinter as tk
from tkinter import filedialog, messagebox
import platform
import psutil
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import requests
from io import BytesIO


# Function to download and load images from a URL
def load_image_from_url(url, size):
    response = requests.get(url)
    response.raise_for_status()  # Check for errors
    image = Image.open(BytesIO(response.content))
    image = image.resize(size)
    return ImageTk.PhotoImage(image)


# URLs for images with raw=true to get the actual image file
app_logo_url = "https://github.com/Ajaykumar2605/System-Info/blob/main/source%20files/icon/Appicon.png?raw=true"
app_system_url = "https://github.com/Ajaykumar2605/System-Info/blob/main/source%20files/icon/system.png?raw=true"

# Setting up the main application window
root = tk.Tk()
root.title("System Info")
root.geometry("502x483")
root.resizable(False, False)

# Load and display application logo and system image
try:
    app_logo_photo = load_image_from_url(app_logo_url, (150, 150))
    app_system_logo = load_image_from_url(app_system_url, (150, 150))

    app_logo_label = tk.Label(root, image=app_logo_photo)
    app_logo_label.pack(pady=10)

    root.iconphoto(False, app_system_logo)
except Exception as e:
    print(f"Error loading images: {e}")


# Get system information
def get_system_info():
    uname = platform.uname()
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_info = {
        "System": uname.system,
        "Model Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor,
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB",
        "Python Version": platform.python_version(),
        "Date": current_date,
    }
    return system_info


# Update the GUI with system information
def update_info():
    loading_label.pack()
    info_label.pack_forget()

    def update_info_thread():
        info = get_system_info()
        time.sleep(2)  # Simulate loading animation

        info_text.set(
            f"System: {info['System']}\n"
            f"Model Name: {info['Model Name']}\n"
            f"Release: {info['Release']}\n"
            f"Version: {info['Version']}\n"
            f"Machine: {info['Machine']}\n"
            f"Processor: {info['Processor']}\n"
            f"RAM: {info['RAM']}\n"
            f"Python Version: {info['Python Version']}\n"
            f"Date: {info['Date']}"
        )

        loading_label.pack_forget()
        info_label.pack()
        refresh_button.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL)

    threading.Thread(target=update_info_thread).start()


# Save system information to a text file
def save_info():
    info = info_text.get()
    if not info:
        messagebox.showwarning("No Information", "There is no information to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(info)
        messagebox.showinfo("Saved", f"System information saved to {file_path}")


info_text = tk.StringVar()
info_label = tk.Label(root, textvariable=info_text, justify=tk.LEFT, font=("Arial", 12), padx=10, pady=10, bg='#387ba1',
                      fg='white')

# Loading
loading_text = tk.StringVar()
loading_text.set("Loading...")
loading_label = tk.Label(root, textvariable=loading_text, font=("Arial bold", 12))


def animate_loading():
    loading_states = ["Loading.", "Loading..", "Loading..."]
    idx = 0
    while True:
        loading_text.set(loading_states[idx % len(loading_states)])
        idx += 1
        time.sleep(0.5)


# Start loading animation
threading.Thread(target=animate_loading, daemon=True).start()

# Initialize with system information
update_info()
refresh_button = tk.Button(root, text="Refresh", command=update_info, bg='#ffffff', fg='#19858c')
refresh_button.place(x=20, y=370, width=100, height=50)

# Save button
save_button = tk.Button(root, text="Save Info", command=save_info, bg='#ffffff', fg='#19858c')
save_button.place(x=360, y=370, width=100, height=50)

# Copyright logo
footer_frame = tk.Frame(root, pady=10)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
copyright_notice = tk.Label(footer_frame, text="© 2024 Ajay Kumar. All rights reserved.", anchor='e')
copyright_notice.pack(side=tk.BOTTOM, padx=10)

# Start the Tkinter event loop
root.mainloop()
