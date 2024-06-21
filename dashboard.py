import tkinter as tk
from tkinter import Menu
import brand_page  # Import halaman Brand

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDASore-Desktop Dashboard")

        self.create_widgets()

    def create_widgets(self):
        # Create a menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Create Items menu
        items_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Items", menu=items_menu)

        # Submenu for Brand
        items_menu.add_command(label="Brand", command=self.open_brand_page)

        # Create Orders menu
        orders_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Orders", menu=orders_menu)

        # Create Report menu
        report_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Report", menu=report_menu)

        # Label on Dashboard
        self.label = tk.Label(self.root, text="Welcome to the Dashboard", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Button to exit fullscreen
        self.exit_fullscreen_btn = tk.Button(self.root, text="Exit Fullscreen", command=self.exit_fullscreen)
        self.exit_fullscreen_btn.pack(pady=10)

        # Button to quit application
        self.quit_btn = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_btn.pack(pady=10)

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)

    def open_brand_page(self):
        brand_root = tk.Tk()
        app = brand_page.BrandPage(brand_root)
        brand_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.attributes('-fullscreen', True)
    root.mainloop()
