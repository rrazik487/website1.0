import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import os

class InventoryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Set paths for material types and inventory
        self.material_file = os.path.join(script_dir, "material_types.txt")
        self.inventory_file = os.path.join(script_dir, "inventory.xlsx")

        # Load material types from file or set default values
        if os.path.exists(self.material_file):
            with open(self.material_file, "r") as file:
                self.material_types = file.read().splitlines()
        else:
            self.material_types = ["Type A", "Type B", "Type C"]

        # Initialize DataFrame
        if os.path.exists(self.inventory_file):
            self.df = pd.read_excel(self.inventory_file)
        else:
            self.df = pd.DataFrame(columns=["Product Name", "Quantity", "Material Type"])

        self.material_var = tk.StringVar(self.root)
        self.material_dropdown = None

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry widgets for data entry
        self.lbl_name = tk.Label(self.root, text="Product Name:")
        self.lbl_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.lbl_quantity = tk.Label(self.root, text="Quantity:")
        self.lbl_quantity.grid(row=1, column=0, padx=10, pady=5)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5)

        self.lbl_material = tk.Label(self.root, text="Material Type:")
        self.lbl_material.grid(row=2, column=0, padx=10, pady=5)

        # Check if material types exist before setting the default value
        if self.material_types:
            self.material_var.set(self.material_types[0])  # default value
            self.material_dropdown = tk.OptionMenu(self.root, self.material_var, *self.material_types)
            self.material_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Button for adding and removing material types
        self.btn_add_material = tk.Button(self.root, text="Add Material", command=self.add_material)
        self.btn_add_material.grid(row=2, column=2, padx=5, pady=5)

        self.btn_remove_material = tk.Button(self.root, text="Remove Material", command=self.remove_material)
        self.btn_remove_material.grid(row=2, column=3, padx=5, pady=5)

        # Checkbox for exporting to Excel
        self.export_to_excel_var = tk.BooleanVar()
        self.export_to_excel_var.set(False)  # default value
        self.chk_export_to_excel = tk.Checkbutton(self.root, text="Export to Excel", variable=self.export_to_excel_var)
        self.chk_export_to_excel.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Button for adding entry
        self.btn_add = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.btn_add.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Search functionality
        self.lbl_search = tk.Label(self.root, text="Search:")
        self.lbl_search.grid(row=5, column=0, padx=10, pady=5)
        self.entry_search = tk.Entry(self.root)
        self.entry_search.grid(row=5, column=1, padx=10, pady=5)

        self.btn_search = tk.Button(self.root, text="Search", command=self.search_entry)
        self.btn_search.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def save_material_types(self):
        with open(self.material_file, "w") as file:
            file.write("\n".join(self.material_types))

    def add_material(self):
        new_material = simpledialog.askstring("Add Material", "Enter the name of the new material type:")
        if new_material:
            if new_material not in self.material_types:
                self.material_types.append(new_material)
                if self.material_dropdown:
                    self.material_dropdown['menu'].delete(0, 'end')
                    for material in self.material_types:
                        self.material_dropdown['menu'].add_command(label=material, command=tk._setit(self.material_var, material))
                self.save_material_types()
            else:
                messagebox.showerror("Error", "Material type already exists.")

    def remove_material(self):
        selected_material = self.material_var.get()
        if selected_material in self.material_types:
            if len(self.material_types) > 1:
                self.material_types.remove(selected_material)
                if self.material_dropdown:
                    self.material_dropdown.destroy()  # Destroy old dropdown menu
                    if self.material_types:  # Check if material types exist before recreating dropdown menu
                        self.material_var.set(self.material_types[0])
                        self.material_dropdown = tk.OptionMenu(self.root, self.material_var, *self.material_types)  # Recreate dropdown menu
                        self.material_dropdown.grid(row=2, column=1, padx=10, pady=5)  # Re-grid dropdown menu
                self.save_material_types()
            else:
                messagebox.showerror("Error", "Cannot remove the only material type.")

    def add_entry(self):
        # Get data from entry widgets
        name = self.entry_name.get()
        quantity_str = self.entry_quantity.get()
        material_type = self.material_var.get()

        # Validate data
        if name == '' or quantity_str == '':
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid integer")
            return

        # Check if the product name already exists in the DataFrame
        if name in self.df["Product Name"].values:
            # Check if the material type is the same for the existing product name
            if any((self.df["Product Name"] == name) & (self.df["Material Type"] == material_type)):
                # Alert user that the material type is the same for an existing product name
                messagebox.showerror("Error", "Product name already exists with the same material type.")
            else:
                # Update the quantity for the existing entry with a different material type
                self.df.loc[(self.df["Product Name"] == name), "Quantity"] += quantity
        else:
            # Add entry to DataFrame
            new_entry = pd.DataFrame({"Product Name": [name], "Quantity": [quantity], "Material Type": [material_type]})
            self.df = pd.concat([self.df, new_entry], ignore_index=True)
        
        # Clear entry widgets
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

        # Export DataFrame to Excel if checkbox is checked
        if self.export_to_excel_var.get():
            self.df.to_excel(self.inventory_file, index=False)
            messagebox.showinfo("Success", "Entry added successfully and data exported to Excel")
        else:
            messagebox.showinfo("Success", "Entry added successfully")

    def search_entry(self):
        # Get search query
        query = self.entry_search.get()

        # Search DataFrame
        if os.path.exists(self.inventory_file):
            self.df = pd.read_excel(self.inventory_file)
            result = self.df[self.df["Product Name"].str.contains(query, case=False)]

            # Display search result
            if not result.empty:
                messagebox.showinfo("Search Result", result.to_string(index=False))
            else:
                messagebox.showinfo("Search Result", "No matching entries found")
        else:
            messagebox.showinfo("Search Result", "Inventory file not found")

def main():
    root = tk.Tk()
    app = InventoryManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
