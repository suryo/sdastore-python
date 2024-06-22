import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
from config import BASE_URL

class CategoryPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Category Management")
        
        # Create a frame for UI elements
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Label for heading
        self.heading_label = tk.Label(self.frame, text="Manage Categories", font=("Helvetica", 18, "bold"))
        self.heading_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Treeview to display categories
        self.category_tree = ttk.Treeview(self.frame, columns=("ID", "Name", "Parent ID"), show='headings', height=10)
        self.category_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        
        # Define columns
        self.category_tree.heading("ID", text="ID")
        self.category_tree.heading("Name", text="Name")
        self.category_tree.heading("Parent ID", text="Parent ID")

        # Set column width
        self.category_tree.column("ID", width=50, anchor=tk.CENTER)
        self.category_tree.column("Name", width=250, anchor=tk.W)
        self.category_tree.column("Parent ID", width=100, anchor=tk.CENTER)

        # Scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.category_tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky=tk.NS)
        self.category_tree.configure(yscrollcommand=self.scrollbar.set)

        # Bind double click event
        self.category_tree.bind("<Double-1>", self.on_double_click)

        # Load categories from API
        self.load_categories()

    def load_categories(self):
        try:
            response = requests.get("{BASE_URL}/api/categories-with-children")
            if response.status_code == 200:
                categories = response.json()
                for row in self.category_tree.get_children():
                    self.category_tree.delete(row)
                self.insert_categories(categories)
            else:
                messagebox.showerror("Error", f"Failed to fetch categories: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching categories: {e}")

    def insert_categories(self, categories, parent=''):
        for category in categories:
            item_id = self.category_tree.insert(parent, tk.END, values=(category['id'], category['name'], category['parent_id']))
            if 'children' in category and category['children']:
                self.insert_categories(category['children'], item_id)

    def on_double_click(self, event):
        item = self.category_tree.identify('item', event.x, event.y)
        column = self.category_tree.identify('column', event.x, event.y)
        column_index = int(column[1:]) - 1  # Adjusting column index because it starts from "#1"

        if column_index == 1 or column_index == 2:  # We allow editing for "Name" and "Parent ID" columns
            self.edit_category(item, column_index)

    def edit_category(self, item, column_index):
        category_id, old_name, old_parent_id = self.category_tree.item(item, 'values')

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Category")

        if column_index == 1:  # Editing "Name" column
            tk.Label(self.edit_window, text="Category Name:").pack(pady=10)
            self.new_value_entry = tk.Entry(self.edit_window)
            self.new_value_entry.pack(pady=10)
            self.new_value_entry.insert(0, old_name)
        elif column_index == 2:  # Editing "Parent ID" column
            tk.Label(self.edit_window, text="Parent ID:").pack(pady=10)
            self.new_value_entry = tk.Entry(self.edit_window)
            self.new_value_entry.pack(pady=10)
            self.new_value_entry.insert(0, old_parent_id if old_parent_id else '')

        tk.Button(self.edit_window, text="Save", command=lambda: self.save_edited_category(item, category_id, column_index)).pack(pady=10)

    def save_edited_category(self, item, category_id, column_index):
        new_value = self.new_value_entry.get()

        if column_index == 1:  # Updating "Name"
            data = {"name": new_value}
        elif column_index == 2:  # Updating "Parent ID"
            data = {"parent_id": int(new_value) if new_value else None}

        if new_value:
            try:
                response = requests.put(f"{BASE_URL}/api/categories/{category_id}", json=data)
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Category updated successfully")
                    self.edit_window.destroy()
                    self.load_categories()
                else:
                    error_message = response.json().get('errors', 'Failed to update category')
                    messagebox.showerror("Error", f"Failed to update category: {error_message}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Error updating category: {e}")
        else:
            messagebox.showerror("Error", "Field cannot be empty")

if __name__ == "__main__":
    root = tk.Tk()
    app = CategoryPage(root)
    root.mainloop()
