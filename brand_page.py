import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
from config import BASE_URL


class BrandPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Brand Management")
        
        # Create a frame for UI elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Label for heading
        self.heading_label = tk.Label(self.frame, text="Manage Brands", font=("Helvetica", 18, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Treeview to display brands
        self.brand_tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show='headings', height=10)
        self.brand_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        
        # Define columns
        self.brand_tree.heading("ID", text="ID")
        self.brand_tree.heading("Name", text="Name")

        # Set column width
        self.brand_tree.column("ID", width=50, anchor=tk.CENTER)
        self.brand_tree.column("Name", width=250, anchor=tk.W)

        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.brand_tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky=tk.NS)
        self.brand_tree.configure(yscrollcommand=self.scrollbar.set)

        # Bind double click event
        self.brand_tree.bind("<Double-1>", self.on_double_click)

        # Buttons for CRUD operations
        self.add_btn = tk.Button(self.frame, text="Add Brand", command=self.add_brand)
        self.add_btn.grid(row=2, column=0, padx=5, pady=5)

        self.delete_btn = tk.Button(self.frame, text="Delete Brand", command=self.delete_brand)
        self.delete_btn.grid(row=2, column=2, padx=5, pady=5)

        # Load brands from API
        self.load_brands()

    def load_brands(self):
        try:
            response = requests.get(f"{BASE_URL}/api/brands")
            if response.status_code == 200:
                brands = response.json()
                for row in self.brand_tree.get_children():
                    self.brand_tree.delete(row)
                for brand in brands:
                    self.brand_tree.insert("", tk.END, values=(brand['id'], brand['name']))
            else:
                messagebox.showerror("Error", f"Failed to fetch brands: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching brands: {e}")

    def add_brand(self):
        brand_name = simpledialog.askstring("Add Brand", "Enter brand name:")
        if brand_name:
            try:
                response = requests.post(f"{BASE_URL}/api/brands", json={"name": brand_name})
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Brand added successfully")
                    self.load_brands()
                else:
                    messagebox.showerror("Error", f"Failed to add brand: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error adding brand: {e}")

    def delete_brand(self):
        selected_item = self.brand_tree.selection()
        if selected_item:
            brand_id = self.brand_tree.item(selected_item)["values"][0]
            confirmation = messagebox.askyesno("Delete Brand", "Are you sure you want to delete this brand?")
            if confirmation:
                try:
                    response = requests.delete(f"{BASE_URL}/api/brands/{brand_id}")
                    if response.status_code == 204:
                        messagebox.showinfo("Success", "Brand deleted successfully")
                        self.load_brands()
                    else:
                        messagebox.showerror("Error", f"Failed to delete brand: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Error deleting brand: {e}")
        else:
            messagebox.showerror("Error", "Please select a brand to delete")

    def on_double_click(self, event):
        item = self.brand_tree.identify('item', event.x, event.y)
        column = self.brand_tree.identify('column', event.x, event.y)
        column_index = int(column[1:]) - 1  # Adjusting column index because it starts from "#1"

        if column_index == 1:  # We allow editing only for the "Name" column
            self.edit_brand(item)

    def edit_brand(self, item):
        brand_id, old_name = self.brand_tree.item(item, 'values')

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Brand")

        tk.Label(self.edit_window, text="Brand Name:").pack(pady=10)
        self.new_name_entry = tk.Entry(self.edit_window)
        self.new_name_entry.pack(pady=10)
        self.new_name_entry.insert(0, old_name)

        tk.Button(self.edit_window, text="Save", command=lambda: self.save_edited_brand(item, brand_id)).pack(pady=10)

    def save_edited_brand(self, item, brand_id):
        new_name = self.new_name_entry.get()

        if new_name:
            try:
                response = requests.put(f"{BASE_URL}/api/brands/{brand_id}", json={"name": new_name})
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Brand updated successfully")
                    self.edit_window.destroy()
                    self.load_brands()
                else:
                    messagebox.showerror("Error", f"Failed to update brand: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error updating brand: {e}")
        else:
            messagebox.showerror("Error", "Brand name cannot be empty")

if __name__ == "__main__":
    root = tk.Tk()
    app = BrandPage(root)
    root.mainloop()
