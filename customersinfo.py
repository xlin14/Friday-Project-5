import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def initialize_database():
    """
    Connects to the SQLite database and creates the 'customers' table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()

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
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def add_customer_to_db(name, birthday, email, phone, address, contact_method):
    """
    Inserts a new customer record into the database.
    
    Args:
        name (str): Customer's name.
        birthday (str): Customer's birthday.
        email (str): Customer's email address.
        phone (str): Customer's phone number.
        address (str): Customer's physical address.
        contact_method (str): Customer's preferred contact method.
    """
    try:
        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()
    
        cursor.execute('''
            INSERT INTO customers (name, birthday, email, phone, address, contact_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, birthday, email, phone, address, contact_method))
        
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while saving data: {e}")
    finally:
        if conn:
            conn.close()



class CustomerApp:
    def __init__(self, root_window):
        """
        Initializes the GUI application window and its widgets.
        """
        self.root = root_window
        self.root.title("Customer Information Entry")
        self.root.geometry("450x300")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
   
        labels_text = ["Name:", "Birthday (YYYY-MM-DD):", "Email:", "Phone:", "Address:", "Preferred Contact:"]
        for i, text in enumerate(labels_text):
            label = ttk.Label(main_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
       
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.birthday_entry = ttk.Entry(main_frame, width=40)
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.phone_entry = ttk.Entry(main_frame, width=40)
        self.address_entry = ttk.Entry(main_frame, width=40)
        
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.birthday_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5)
        
        
        self.contact_method_var = tk.StringVar(value="Email") 
        contact_options = ["Email", "Phone", "Mail"]
        self.contact_menu = ttk.OptionMenu(main_frame, self.contact_method_var, contact_options[0], *contact_options)
        self.contact_menu.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        
        submit_button = ttk.Button(main_frame, text="Submit", command=self.submit_data)
        submit_button.grid(row=6, column=1, sticky=tk.E, padx=5, pady=15)
        
    def clear_form(self):
        """Clears all input fields in the GUI."""
        self.name_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_method_var.set("Email") 
        self.name_entry.focus_set() 

    def submit_data(self):
        """
        Handles the submit button click event. Gathers data, validates it,
        saves it to the database, and clears the form.
        """
        name = self.name_entry.get()
        birthday = self.birthday_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        contact_method = self.contact_method_var.get()
        
        if not name.strip():
            messagebox.showwarning("Input Error", "The 'Name' field is required.")
            return

        add_customer_to_db(name, birthday, email, phone, address, contact_method)

        messagebox.showinfo("Success", f"Customer '{name}' has been added to the database.")
        
        self.clear_form()



if __name__ == "__main__":
    initialize_database()
    
    root = tk.Tk()
    
    app = CustomerApp(root)
    
    root.mainloop()
