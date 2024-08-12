import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import os
import subprocess
from tkinterweb import HtmlFrame

def generate_report():
    # Run the other script as a separate process
    result = subprocess.run(["python3", "proxtest.py"], capture_output=True, text=True)

    if result.returncode == 0 and os.path.exists("proxmox_cluster_report.html"):
        messagebox.showinfo("Success", "Report generated successfully!")
        webbrowser.open("proxmox_cluster_report.html")
    else:
        messagebox.showerror("Error", f"Failed to generate report.\n{result.stderr}")

root = tk.Tk()
root.title("Proxmox Report Generator")
root.geometry("400x200")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Proxmox Report Generator", font=("Helvetica", 16), bg="#f0f0f0")
title_label.pack(pady=10)

generate_button = tk.Button(
    root, 
    text="Generate Report", 
    command=generate_report, 
    font=("Helvetica", 14), 
    bg="#4CAF50", 
    fg="white",
    padx=20, 
    pady=10,
    relief="raised",
    borderwidth=2
)
generate_button.pack(pady=20)

root.eval('tk::PlaceWindow . center')
root.mainloop()
