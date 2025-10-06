import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# --- 1. DATABASE SETUP ---
def setup_database():
    """Creates the database file and the customers table if they don't exist."""
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    
    # Create table with an auto-incrementing primary key for unique IDs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            contact_method TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- 2. GUI APPLICATION ---
class CustomerApp:
    def __init__(self, root):
        """Initializes the application window and its widgets."""
        self.root = root
        self.root.title("Customer Information Management")
        
        # --- Create main frame ---
        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(padx=10, pady=10)

        # --- GUI Widgets ---
        # Labels and Entry fields organized in a grid
        labels = ["Name:", "Birthday (YYYY-MM-DD):", "Email:", "Phone Number:", "Address:", "Preferred Contact Method:"]
        
        for i, label_text in enumerate(labels):
            label = tk.Label(main_frame, text=label_text, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

        # Entry fields
        self.name_entry = tk.Entry(main_frame, width=40)
        self.birthday_entry = tk.Entry(main_frame, width=40)
        self.email_entry = tk.Entry(main_frame, width=40)
        self.phone_entry = tk.Entry(main_frame, width=40)
        self.address_entry = tk.Entry(main_frame, width=40)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.birthday_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Dropdown for Preferred Contact Method
        self.contact_method_var = tk.StringVar()
        contact_options = ["Email", "Phone", "Mail"]
        self.contact_method_menu = ttk.OptionMenu(main_frame, self.contact_method_var, "Email", *contact_options)
        self.contact_method_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        # Submit Button
        submit_button = tk.Button(main_frame, text="Submit", command=self.submit_customer, font=('Helvetica', 10, 'bold'))
        submit_button.grid(row=6, column=0, columnspan=2, pady=15)
        
    def clear_form(self):
        """Clears all input fields after submission."""
        self.name_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_method_var.set("Email") # Reset dropdown to default
        
    def submit_customer(self):
        """Gathers data from the form and inserts it into the database."""
        # Get data from GUI fields
        name = self.name_entry.get()
        birthday = self.birthday_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        contact_method = self.contact_method_var.get()
        
        # Basic validation: ensure name is not empty
        if not name:
            messagebox.showerror("Error", "Name field cannot be empty.")
            return
            
        # --- 3. STORE DATA IN DATABASE ---
        try:
            conn = sqlite3.connect('customers.db')
            cursor = conn.cursor()
            
            # Use a parameterized query to prevent SQL injection
            cursor.execute('''
                INSERT INTO customers (name, birthday, email, phone, address, contact_method)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, birthday, email, phone, address, contact_method))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Customer information has been saved successfully!")
            self.clear_form()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    setup_database()  # Ensure the database and table exist
    
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()