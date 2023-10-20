import tkinter as tk
from tkinter import PhotoImage

# Create the main window
root = tk.Tk()
root.title("Home Page")

# Set window size
root.geometry("800x600")

# Load and display the background image
background_image = PhotoImage(file="assets/logo.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create widgets (buttons, labels, entry fields)
button1 = tk.Button(root, text="Depot", width=20, height=2)
button2 = tk.Button(root, text="Historique", width=20, height=2)
button3 = tk.Button(root, text="Button 3", width=20, height=2)
button4 = tk.Button(root, text="Retrait", width=20, height=2)
button5 = tk.Button(root, text="Solde", width=20, height=2)
button6 = tk.Button(root, text="Button 6", width=20, height=2)
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry3 = tk.Entry(root)

# Place the widgets in three rows, each with two widgets
button1.grid(row=0, column=0, padx=10, pady=10)
button4.grid(row=0, column=1, padx=10, pady=10)
button2.grid(row=1, column=0, padx=10, pady=10)
button5.grid(row=1, column=1, padx=10, pady=10)
button3.grid(row=2, column=0, padx=10, pady=10)
button6.grid(row=2, column=1, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()