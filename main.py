import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk


# Function to handle the login button click event
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "your_username" and password == "your_password":
        messagebox.showinfo("Login Successful", "Welcome, " + username)
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")


# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("400x400")  # Set the window size to 400x200 pixels

# Create a header frame
header_frame = tk.Frame(root)
header_frame.pack(fill=tk.BOTH, expand=True)

# Load an image for the header
header_image = Image.open("assets/logo.png")  # Replace with the path to your image
header_image = header_image.resize((150, 150), Image.LANCZOS)
header_image = ImageTk.PhotoImage(header_image)
header_label = tk.Label(root, image=header_image)
header_label.pack()
# Create a label for the username
username_label = tk.Label(root, text="Username:")
username_label.pack()

# Create an entry widget for username input
username_entry = tk.Entry(root, width=40)
username_entry.pack()

# Add space between username and password
spacer = tk.Label(root, text="", height=1)
spacer.pack()

# Create a label for the password
password_label = tk.Label(root, text="Password:")
password_label.pack()

# Create an entry widget for password input (set show="*" for password masking)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack()

# Add space between password and login button
spacer = tk.Label(root, text="", height=1)
spacer.pack()

# Create a round login button using a canvas widget
canvas = tk.Canvas(root, width=150, height=50)
canvas.pack()
round_login_button = tk.Button(canvas, text="Login", command=login, borderwidth=3, relief="raised", width=10)
canvas.create_window(75, 25, window=round_login_button)

# Start the Tkinter main loop
root.mainloop()