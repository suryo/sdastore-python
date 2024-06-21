import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

class BrandPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Brand Management")
        
        # Create a frame for UI elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Label for heading
        self.heading_label = tk.Label(self.frame, text="Manage Brands", font=("Helvetica", 18, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Listbox to display brands
        self.brand_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.brand_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Scrollbar for listbox
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=3, sticky=tk.NS)
        self.brand_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.brand_listbox.yview)

        # Buttons for CRUD operations
        self.add_btn = tk.Button(self.frame, text="Add Brand", command=self.add_brand)
        self.add_btn.grid(row=2, column=0, padx=5, pady=5)

        self.edit_btn = tk.Button(self.frame, text="Edit Brand", command=self.edit_brand)
        self.edit_btn.grid(row=2, column=1, padx=5, pady=5)

        self.delete_btn = tk.Button(self.frame, text="Delete Brand", command=self.delete_brand)
        self.delete_btn.grid(row=2, column=2, padx=5, pady=5)

        # Load brands from API
        self.load_brands()

    def load_brands(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/brands")
            if response.status_code == 200:
                brands = response.json()
                self.brand_listbox.delete(0, tk.END)
                for brand in brands:
                    self.brand_listbox.insert(tk.END, f"{brand['id']} - {brand['name']}")
            else:
                messagebox.showerror("Error", f"Failed to fetch brands: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching brands: {e}")

    def add_brand(self):
        brand_name = simpledialog.askstring("Add Brand", "Enter brand name:")
        if brand_name:
            try:
                response = requests.post("http://127.0.0.1:8000/api/brands", json={"name": brand_name})
                if response.status_code == 201:
                    messagebox.showinfo("Success", "Brand added successfully")
                    self.load_brands()
                else:
                    messagebox.showerror("Error", f"Failed to add brand: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error adding brand: {e}")

    def edit_brand(self):
        selected_brand = self.brand_listbox.curselection()
        if selected_brand:
            brand_id = selected_brand[0] + 1  # Assuming brand IDs start from 1
            brand_name = simpledialog.askstring("Edit Brand", "Enter new brand name:")
            if brand_name:
                try:
                    response = requests.put(f"http://127.0.0.1:8000/api/brands/{brand_id}", json={"name": brand_name})
                    if response.status_code == 200:
                        messagebox.showinfo("Success", "Brand updated successfully")
                        self.load_brands()
                    else:
                        messagebox.showerror("Error", f"Failed to update brand: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Error updating brand: {e}")
        else:
            messagebox.showerror("Error", "Please select a brand to edit")

    def delete_brand(self):
        selected_brand = self.brand_listbox.curselection()
        if selected_brand:
            brand_id = selected_brand[0] + 1  # Assuming brand IDs start from 1
            confirmation = messagebox.askyesno("Delete Brand", "Are you sure you want to delete this brand?")
            if confirmation:
                try:
                    response = requests.delete(f"http://127.0.0.1:8000/api/brands/{brand_id}")
                    if response.status_code == 204:
                        messagebox.showinfo("Success", "Brand deleted successfully")
                        self.load_brands()
                    else:
                        messagebox.showerror("Error", f"Failed to delete brand: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Error deleting brand: {e}")
        else:
            messagebox.showerror("Error", "Please select a brand to delete")

if __name__ == "__main__":
    root = tk.Tk()
    app = BrandPage(root)
    root.mainloop()
