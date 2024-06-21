import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import dashboard  # Import file dashboard

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SDASore-Desktop Login")
        self.center_window(300, 350)
        self.root.configure(bg="white")

        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_widgets(self):
        # Adding logo
        try:
            self.logo_img = Image.open("logo-sda.png")  # Use the PNG image
            self.logo_img = self.logo_img.resize((100, 100), Image.ANTIALIAS)
            self.logo = ImageTk.PhotoImage(self.logo_img)
            self.logo_label = tk.Label(self.root, image=self.logo, bg="white")
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Label for username
        self.label_user = tk.Label(self.root, text="Username:", bg="white")
        self.label_user.pack(pady=5)
        
        # Entry for username
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)

        # Label for password
        self.label_pass = tk.Label(self.root, text="Password:", bg="white")
        self.label_pass.pack(pady=5)

        # Entry for password
        self.entry_pass = tk.Entry(self.root, show='*')
        self.entry_pass.pack(pady=5)

        # Login button
        self.login_btn = tk.Button(self.root, text="Login", command=self.check_login)
        self.login_btn.pack(pady=10)

    def check_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if username == "adminsdastore" and password == "12345678":
            self.root.destroy()
            self.open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_dashboard(self):
        dashboard_root = tk.Tk()
        app = dashboard.DashboardApp(dashboard_root)
        dashboard_root.attributes('-fullscreen', True)
        dashboard_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
