import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000"

class ProductPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        
        # Create a frame for UI elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Label for heading
        self.heading_label = tk.Label(self.frame, text="Manage Products", font=("Helvetica", 18, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=6, pady=10)

        # Search fields and buttons
        self.search_label = tk.Label(self.frame, text="Search By:")
        self.search_label.grid(row=1, column=0, pady=5)

        self.search_option = tk.StringVar()
        self.search_option.set("SKU")

        self.search_menu = ttk.Combobox(self.frame, textvariable=self.search_option, values=["SKU", "Name", "Brand", "Category", "Product Type"])
        self.search_menu.grid(row=1, column=1, pady=5)
        self.search_menu.bind("<<ComboboxSelected>>", self.on_search_option_change)

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=1, column=2, pady=5, padx=5)

        self.search_button = tk.Button(self.frame, text="Search", command=self.search_product)
        self.search_button.grid(row=1, column=3, pady=5)

        # Treeview to display products
        self.product_tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Type", "Price", "Status"), show='headings', height=10)
        self.product_tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        
        # Define columns
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Type", text="Type")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Status", text="Status")

        # Set column width
        self.product_tree.column("ID", width=50, anchor=tk.CENTER)
        self.product_tree.column("Name", width=250, anchor=tk.W)
        self.product_tree.column("Type", width=100, anchor=tk.W)
        self.product_tree.column("Price", width=100, anchor=tk.E)
        self.product_tree.column("Status", width=100, anchor=tk.CENTER)

        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.scrollbar.grid(row=2, column=6, sticky=tk.NS)
        self.product_tree.configure(yscrollcommand=self.scrollbar.set)

        # Load products from API
        self.load_products()

        # Alert button to display selected search option
        self.alert_button = tk.Button(self.frame, text="Show Selected Option", command=self.show_selected_option)
        self.alert_button.grid(row=1, column=4, pady=5)

    def on_search_option_change(self, event):
        # Method to handle change in search option
        selected_option = self.search_menu.get()
        self.search_option.set(selected_option.lower().replace(" ", "_"))
        print(f"Selected Search Option: {self.search_option.get()}")

    def show_selected_option(self):
        # Method to display selected search option in an alert
        selected_option = self.search_option.get()
        messagebox.showinfo("Selected Search Option", f"Selected Option: {selected_option}")

    def load_products(self):
        try:
            response = requests.get(f"{BASE_URL}/api/products")
            if response.status_code == 200:
                products = response.json()
                self.insert_products(products)
            else:
                messagebox.showerror("Error", f"Failed to fetch products: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching products: {e}")

    def insert_products(self, products):
        for product in products:
            self.product_tree.insert('', tk.END, values=(
                product['id'], 
                product['name'], 
                product['product_type'], 
                product.get('price', 'N/A'), 
                product['status']
            ))

    def search_product(self):
        search_value = self.search_entry.get()
        search_option = self.search_option.get()

        if search_value:
            try:
                response = requests.get(f"{BASE_URL}/api/products/search?{search_option}={search_value}")
                if response.status_code == 200:
                    products = response.json()
                    for row in self.product_tree.get_children():
                        self.product_tree.delete(row)
                    self.insert_products(products)
                else:
                    messagebox.showerror("Error", f"Failed to fetch products: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error fetching products: {e}")
        else:
            messagebox.showerror("Error", "Search field cannot be empty")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductPage(root)
    root.mainloop()
