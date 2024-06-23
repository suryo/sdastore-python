import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000"

class SubProductPage:
    def __init__(self, root, product_id):
        self.root = root
        self.root.title("Sub Product Details")
        
        self.product_id = product_id
        self.subproducts = []
        self.field_names = []  # List to store field names

        # Create a frame for UI elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Label for heading
        self.heading_label = tk.Label(self.frame, text="Sub Product Details", font=("Helvetica", 18, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a Treeview with scrollbars
        self.create_treeview()

        # Load field names and sub products
        self.load_field_names()
        self.load_subproducts()

        # Double click event on treeview
        self.subproduct_tree.bind("<Double-1>", self.on_treeview_double_click)

    def create_treeview(self):
        # Treeview with scrollbars
        self.subproduct_tree = ttk.Treeview(self.frame, columns=[], show='headings', height=10)
        self.subproduct_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Scrollbars
        self.tree_scrollx = ttk.Scrollbar(self.frame, orient="horizontal", command=self.subproduct_tree.xview)
        self.tree_scrollx.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.tree_scrolly = ttk.Scrollbar(self.frame, orient="vertical", command=self.subproduct_tree.yview)
        self.tree_scrolly.grid(row=1, column=2, sticky="ns")
        self.subproduct_tree.configure(xscrollcommand=self.tree_scrollx.set, yscrollcommand=self.tree_scrolly.set)

    def load_field_names(self):
        try:
            response = requests.get(f"{BASE_URL}/api/products/{self.product_id}/fields")
            if response.status_code == 200:
                fields = response.json()
                self.field_names = [field['name'] for field in fields]
                self.set_treeview_columns()
            else:
                messagebox.showerror("Error", f"Failed to fetch field names: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching field names: {e}")

    def set_treeview_columns(self):
        # Set columns and headings
        self.subproduct_tree["columns"] = ["ID", "Name"] + self.field_names
        self.subproduct_tree["displaycolumns"] = ["ID", "Name"] + self.field_names

        # Set column headings
        self.subproduct_tree.heading("ID", text="ID")
        self.subproduct_tree.heading("Name", text="Name")
        for field_name in self.field_names:
            self.subproduct_tree.heading(field_name, text=field_name)

        # Set column widths dynamically
        total_width = sum(len(field_name) * 10 for field_name in self.field_names)  # Approximate width calculation
        self.subproduct_tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.subproduct_tree.column("ID", stretch=tk.NO, minwidth=50, width=50)
        self.subproduct_tree.column("Name", stretch=tk.NO, minwidth=150, width=150)
        for field_name in self.field_names:
            column_width = len(field_name) * 10  # Adjust as needed
            self.subproduct_tree.column(field_name, stretch=tk.NO, minwidth=column_width, width=column_width)

    def load_subproducts(self, product_id=None):
        self.product_id = product_id if product_id is not None else self.product_id  # Update the instance variable if product_id is provided
        try:
            response = requests.get(f"{BASE_URL}/api/subproducts-by-product?product_id={self.product_id}")
            if response.status_code == 200:
                self.subproducts = response.json()
                self.insert_subproducts()
            else:
                messagebox.showerror("Error", f"Failed to fetch sub products: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching sub products: {e}")


    def insert_subproducts(self):
        # Clear existing entries
        for item in self.subproduct_tree.get_children():
            self.subproduct_tree.delete(item)

        for subproduct in self.subproducts:
            field_values = {fp['field']['name']: f"{fp['value']} ({fp['satuan']})" for fp in subproduct['field_products']}
            row_values = [subproduct['id'], subproduct['name']] + [field_values.get(field_name, "") for field_name in self.field_names]
            self.subproduct_tree.insert('', tk.END, values=row_values)

    def on_treeview_double_click(self, event):
        item = self.subproduct_tree.identify('item', event.x, event.y)
        column = self.subproduct_tree.identify_column(event.x)
        if item and column:
            column_idx = int(column.replace('#', '')) - 1
            if column_idx >= 2:  # To exclude ID and Name columns
                field_name = self.subproduct_tree["columns"][column_idx]
                subproduct_id = self.subproduct_tree.item(item, 'values')[0]
                self.show_field_value(subproduct_id, field_name)

    def show_field_value(self, subproduct_id, field_name):
        # Find subproduct by ID
        subproduct = next((sp for sp in self.subproducts if sp['id'] == int(subproduct_id)), None)
        if not subproduct:
            messagebox.showerror("Error", f"Subproduct with ID {subproduct_id} not found.")
            return

        # Find field product by field name
        field_product = next((fp for fp in subproduct['field_products'] if fp['field']['name'] == field_name), None)
        if not field_product:
            messagebox.showerror("Error", f"Field product for {field_name} not found in subproduct {subproduct_id}.")
            return

        # Prompt for new value and satuan
        new_value = simpledialog.askstring("Update Field Value", f"Enter new value for {field_name}:",
                                           initialvalue=field_product['value'])
        new_satuan = simpledialog.askstring("Update Field Satuan", f"Enter new satuan for {field_name}:",
                                            initialvalue=field_product['satuan'])
        if new_value is not None and new_satuan is not None:
            field_product['value'] = new_value
            field_product['satuan'] = new_satuan
            self.update_field_product(field_product)

    def update_field_product(self, field_product):
        try:
            response = requests.put(f"{BASE_URL}/api/field-products/{field_product['id']}",
                                    json={"value": field_product['value'], "satuan": field_product['satuan']})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Field value updated successfully.")
                # Update UI if needed
                self.load_subproducts()  # Reload subproducts after update
            else:
                messagebox.showerror("Error", f"Failed to update field value: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error updating field value: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SubProductPage(root, 22)  # Replace 22 with actual product ID
    root.mainloop()
