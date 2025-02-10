import tkinter as tk
from tkinter import messagebox
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import os
from escpos.printer import Usb

# Function to generate and display barcode
def generate_barcode():
    item_name = item_name_entry.get()
    price = price_entry.get()

    if not item_name or not price:
        messagebox.showerror("Error", "Please enter both Item Name and Price.")
        return

    try:
        price = float(price)  # Ensure price is a valid number
    except ValueError:
        messagebox.showerror("Error", "Price must be a number.")
        return

    # Generate barcode content (combine item name and price)
    barcode_data = f"{item_name}-{price:.2f}"

    try:
        # Connect to USB printer (adjust VendorID and ProductID as needed)
        printer = Usb(0x04b8, 0x0202)  # Example VendorID and ProductID for Epson printers
        printer.text("Item: " + item_name + "\n")  # Print item name
        printer.text("Price: $" + str(price) + "\n")  # Print price
        printer.barcode(barcode_data, "CODE128", width=2, height=100, function_type="B")  # Print barcode
        printer.cut()
        messagebox.showinfo("Success", "Barcode printed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to print barcode: {e}")

# Function to check if the printer is connected
def check_printer():
    try:
        # Replace with your printer's VendorID and ProductID
        printer = Usb(0x04b8, 0x0202)
        printer.text("Printer is connected and ready.\n")  # Send a small test command
        printer.cut()
        messagebox.showinfo("Success", "Printer is connected and ready.")
    except Exception as e:
        messagebox.showerror("Error", f"Printer is not connected or not ready.\nError: {e}")

# Set up GUI
app = tk.Tk()
app.title("Barcode Generator & Printer")

# Item Name input
item_name_label = tk.Label(app, text="Item Name:")
item_name_label.grid(row=0, column=0, padx=10, pady=10)
item_name_entry = tk.Entry(app)
item_name_entry.grid(row=0, column=1, padx=10, pady=10)

# Price input
price_label = tk.Label(app, text="Price:")
price_label.grid(row=1, column=0, padx=10, pady=10)
price_entry = tk.Entry(app)
price_entry.grid(row=1, column=1, padx=10, pady=10)

# Generate and Print button
generate_button = tk.Button(app, text="Generate & Print Barcode", command=generate_barcode)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Check Printer button
check_button = tk.Button(app, text="Check Printer", command=check_printer)
check_button.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()
