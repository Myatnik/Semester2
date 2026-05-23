import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

DATABASE_FILE = "database.db"

def create_database():
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id_category INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            name_category TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS products (
            id_product INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            name_of_product TEXT NOT NULL,
            price REAL NOT NULL,
            id_category INTEGER NOT NULL,
            quantity_at_storage REAL NOT NULL,
            FOREIGN KEY(id_category) REFERENCES categories(id_category)
        );
        
        CREATE TABLE IF NOT EXISTS receipts (
            id_check INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS sale_items (
            id_sale INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            id_check INTEGER NOT NULL,
            id_product INTEGER NOT NULL,
            quantity REAL NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY(id_check) REFERENCES receipts(id_check),
            FOREIGN KEY(id_product) REFERENCES products(id_product)
        );
    """)
    
    connection.commit()
    connection.close()
#
def run_select_query(sql_query, parameters=()):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(sql_query, parameters)
    result_rows = cursor.fetchall()
    connection.close()
    return result_rows
#
def run_modify_query(sql_query, parameters=()):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute(sql_query, parameters)
    connection.commit()
    last_inserted_id = cursor.lastrowid
    connection.close()
    return last_inserted_id
#
customer_product_tree = None
manager_product_tree = None
cart_items = []
customer_cart_tree = None
customer_product_id_entry = None
customer_quantity_entry = None
manager_date_entry = None
manager_report_text = None
#
def refresh_product_list():
    products_data = run_select_query("""
        SELECT p.id_product, p.name_of_product, c.name_category, p.price, p.quantity_at_storage
        FROM products p
        JOIN categories c ON p.id_category = c.id_category
        ORDER BY p.id_product
    """)
    
    if customer_product_tree is not None:
        for row in customer_product_tree.get_children():
            customer_product_tree.delete(row)
        
        for product_record in products_data:
            customer_product_tree.insert("", "end", values=product_record)
    
    if manager_product_tree is not None:
        for row in manager_product_tree.get_children():
            manager_product_tree.delete(row)
        
        for product_record in products_data:
            manager_product_tree.insert("", "end", values=product_record)
#
def open_add_category_dialog(manager_window):
    dialog = tk.Toplevel(manager_window)
    dialog.title("Add New Category")
    dialog.geometry("300x150")
    
    tk.ttk.Label(dialog, text="Category Name:").grid(row=0, column=0, padx=5, pady=20, sticky="w")
    category_name_entry = tk.ttk.Entry(dialog, width=25)
    category_name_entry.grid(row=0, column=1, padx=5, pady=20)
    
    def save_new_category():
        try:
            category_name = category_name_entry.get().strip()
            
            if not category_name:
                raise ValueError("Category name cannot be empty")
            
            existing = run_select_query(
                "SELECT id_category FROM categories WHERE name_category = ?",
                (category_name,)
            )
            
            if existing:
                raise ValueError(f"Category '{category_name}' already exists")
            
            run_modify_query(
                "INSERT INTO categories (name_category) VALUES (?)",
                (category_name,)
            )
            dialog.destroy()
            
        except Exception as error:
            messagebox.showerror("Input Error", str(error))
    
    tk.ttk.Button(dialog, text="Save Category", command=save_new_category).grid(row=1, column=0, columnspan=2, pady=10)
#
def open_add_product_dialog(manager_window):
    dialog = tk.Toplevel(manager_window)
    dialog.title("Add New Product")
    dialog.geometry("300x250")
    
    tk.ttk.Label(dialog, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_input = tk.ttk.Entry(dialog, width=25)
    name_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Price per unit:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    price_input = tk.ttk.Entry(dialog, width=25)
    price_input.grid(row=1, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    categories_list = run_select_query("SELECT id_category, name_category FROM categories")
    category_options = [f"{cat_id} - {cat_name}" for cat_id, cat_name in categories_list]
    category_combo = tk.ttk.Combobox(dialog, values=category_options, width=22)
    category_combo.grid(row=2, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Initial Stock:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    stock_input = tk.ttk.Entry(dialog, width=25)
    stock_input.grid(row=3, column=1, padx=5, pady=5)
    
    def save_new_product():
        try:
            product_name = name_input.get().strip()
            unit_price = float(price_input.get())
            category_selection = category_combo.get()
            category_id = int(category_selection.split(" - ")[0])
            stock_quantity = float(stock_input.get())
            
            if not product_name:
                raise ValueError("Product name cannot be empty")
            
            run_modify_query("""
                INSERT INTO products (name_of_product, price, id_category, quantity_at_storage) 
                VALUES (?,?,?,?)
            """, (product_name, unit_price, category_id, stock_quantity))
            
            refresh_product_list()
            dialog.destroy()
        except Exception as error:
            messagebox.showerror("Input Error", str(error))
    
    tk.ttk.Button(dialog, text="Save Product", command=save_new_product).grid(row=4, column=0, columnspan=2, pady=15)
#
def open_edit_product_dialog(manager_window):
    if manager_product_tree is None:
        messagebox.showwarning("Error", "Product table not available")
        return
    
    selected_item = manager_product_tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Required", "Please select a product to edit")
        return
    
    current_values = manager_product_tree.item(selected_item, "values")
    product_id = int(current_values[0])
    current_name = current_values[1]
    current_category = current_values[2]
    current_price = current_values[3]
    current_stock = current_values[4]
    
    dialog = tk.Toplevel(manager_window)
    dialog.title("Edit Product")
    dialog.geometry("300x280")
    
    tk.ttk.Label(dialog, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_input = tk.ttk.Entry(dialog, width=25)
    name_input.insert(0, current_name)
    name_input.grid(row=0, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Price per unit:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    price_input = tk.ttk.Entry(dialog, width=25)
    price_input.insert(0, current_price)
    price_input.grid(row=1, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    categories_list = run_select_query("SELECT id_category, name_category FROM categories")
    category_options = [f"{cat_id} - {cat_name}" for cat_id, cat_name in categories_list]
    category_combo = tk.ttk.Combobox(dialog, values=category_options, width=22)
    
    current_category_id = run_select_query("""
        SELECT id_category FROM products WHERE id_product=?
    """, (product_id,))[0][0]
    current_category_display = f"{current_category_id} - {current_category}"
    
    if current_category_display in category_options:
        category_combo.set(current_category_display)
    category_combo.grid(row=2, column=1, padx=5, pady=5)
    
    tk.ttk.Label(dialog, text="Stock Quantity:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    stock_input = tk.ttk.Entry(dialog, width=25)
    stock_input.insert(0, current_stock)
    stock_input.grid(row=3, column=1, padx=5, pady=5)
    
    def save_edits():
        try:
            updated_name = name_input.get().strip()
            updated_price = float(price_input.get())
            updated_stock = float(stock_input.get())
            category_selection = category_combo.get()
            updated_category_id = int(category_selection.split(" - ")[0])
            
            if not updated_name:
                raise ValueError("Product name cannot be empty")
            
            run_modify_query("""
                UPDATE products 
                SET name_of_product=?, price=?, quantity_at_storage=?, id_category=? 
                WHERE id_product=?
            """, (updated_name, updated_price, updated_stock, updated_category_id, product_id))
            
            refresh_product_list()
            dialog.destroy()
        except Exception as error:
            messagebox.showerror("Input Error", str(error))
    
    tk.ttk.Button(dialog, text="Update Product", command=save_edits).grid(row=4, column=0, columnspan=2, pady=15)
#
def display_sales_report():
    selected_date = manager_date_entry.get().strip()
    manager_report_text.delete("1.0", tk.END)
    
    revenue_result = run_select_query("""
        SELECT COALESCE(SUM(si.quantity * si.price_per_unit), 0)
        FROM sale_items si
        JOIN receipts r ON si.id_check = r.id_check
        WHERE r.created_at = ?
    """, (selected_date,))
    
    total_revenue = revenue_result[0][0]
    manager_report_text.insert(tk.END, f"Sales Report for {selected_date}\n")
    manager_report_text.insert(tk.END, f"{'='*40}\n")
    manager_report_text.insert(tk.END, f"Total Revenue: {total_revenue:.2f}\n\n")
    
    sold_items = run_select_query("""
        SELECT p.id_product, p.name_of_product, SUM(si.quantity) AS total_qty
        FROM sale_items si
        JOIN receipts r ON si.id_check = r.id_check
        JOIN products p ON si.id_product = p.id_product
        WHERE r.created_at = ?
        GROUP BY p.id_product, p.name_of_product
        ORDER BY p.id_product
    """, (selected_date,))
    
    if sold_items:
        manager_report_text.insert(tk.END, "Products Sold:\n")
        manager_report_text.insert(tk.END, "-" * 30 + "\n")
        for product_id, product_name, quantity_sold in sold_items:
            manager_report_text.insert(
                tk.END, 
                f"ID: {product_id} | {product_name} - {quantity_sold:.2f} units\n"
            )
    else:
        manager_report_text.insert(tk.END, "No sales recorded for this date.")
#
def update_cart_display():
    if customer_cart_tree is None:
        return
    
    for row in customer_cart_tree.get_children():
        customer_cart_tree.delete(row)
    
    for cart_item in cart_items:
        product_info = run_select_query("""
            SELECT name_of_product, price FROM products WHERE id_product=?
        """, (cart_item["id"],))[0]
        
        product_name, unit_price = product_info
        line_total = unit_price * cart_item["qty"]
        
        customer_cart_tree.insert("", "end", values=(
            cart_item["id"], 
            product_name, 
            cart_item["qty"], 
            unit_price, 
            round(line_total, 2)
        ))
#
def add_item_to_cart():
    product_id_text = customer_product_id_entry.get()
    quantity_text = customer_quantity_entry.get()
    
    if not product_id_text or not quantity_text:
        messagebox.showwarning("Missing Data", "Please enter both product ID and quantity")
        return
    
    try:
        product_id = int(product_id_text)
        requested_qty = float(quantity_text)
        if requested_qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values")
        return
    
    product_data = run_select_query("""
        SELECT name_of_product, price, quantity_at_storage 
        FROM products WHERE id_product=?
    """, (product_id,))
    
    if not product_data:
        messagebox.showerror("Not Found", f"Product with ID {product_id} does not exist")
        return
    
    product_name, unit_price, available_stock = product_data[0]
    
    already_in_cart = sum(item["qty"] for item in cart_items if item["id"] == product_id)
    
    if already_in_cart + requested_qty > available_stock:
        messagebox.showerror(
            "Stock Error", 
            f"Insufficient stock! Available: {available_stock - already_in_cart}"
        )
        return
    
    cart_items.append({"id": product_id, "qty": requested_qty})
    update_cart_display()
    
    customer_product_id_entry.delete(0, tk.END)
    customer_quantity_entry.delete(0, tk.END)
#
def process_purchase():
    if not cart_items:
        messagebox.showwarning("Empty Cart", "Cannot process empty cart")
        return
    
    database_connection = sqlite3.connect(DATABASE_FILE)
    database_connection.execute("PRAGMA foreign_keys = ON")
    db_cursor = database_connection.cursor()
    
    try:
        db_cursor.execute("BEGIN")
        
        today_date = date.today().isoformat()
        db_cursor.execute("INSERT INTO receipts (created_at) VALUES (?)", (today_date,))
        receipt_number = db_cursor.lastrowid
        
        for cart_item in cart_items:
            product_id = cart_item["id"]
            quantity = cart_item["qty"]
            
            db_cursor.execute("SELECT price FROM products WHERE id_product = ?", (product_id,))
            price_data = db_cursor.fetchone()
            if not price_data:
                raise Exception(f"Product {product_id} not found in database")
            
            current_price = price_data[0]
            
            db_cursor.execute("""
                UPDATE products 
                SET quantity_at_storage = quantity_at_storage - ? 
                WHERE id_product = ? AND quantity_at_storage >= ?
            """, (quantity, product_id, quantity))
            
            if db_cursor.rowcount == 0:
                raise Exception(f"Stock insufficient for product ID {product_id}")
            
            db_cursor.execute("""
                INSERT INTO sale_items (id_check, id_product, quantity, price_per_unit) 
                VALUES (?,?,?,?)
            """, (receipt_number, product_id, quantity, current_price))
        
        database_connection.commit()
        messagebox.showinfo("Success", f"Receipt #{receipt_number} has been created")
        
        cart_items.clear()
        update_cart_display()
        refresh_product_list()
        
    except Exception as error:
        database_connection.rollback()
        messagebox.showerror("Transaction Failed", f"Purchase error: {error}")
    finally:
        database_connection.close()
#
def setup_customer_window():
    global customer_product_tree, customer_cart_tree, customer_product_id_entry, customer_quantity_entry
    
    customer_window = tk.Tk()
    customer_window.title("Store - Customer Interface")
    customer_window.geometry("720x500")
    
    #product table
    products_frame = tk.ttk.LabelFrame(customer_window, text="Available Products", padding=5)
    products_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    customer_product_tree = tk.ttk.Treeview(
        products_frame,
        columns=("id", "name", "category", "price", "stock"),
        show="headings",
        height=8
    )
    
    column_configs = [
        ("id", "ID", 40),
        ("name", "Product Name", 150),
        ("category", "Category", 100),
        ("price", "Unit Price", 80),
        ("stock", "Stock", 80)
    ]
    
    for col_id, col_label, col_width in column_configs:
        customer_product_tree.heading(col_id, text=col_label)
        customer_product_tree.column(col_id, width=col_width)
    
    customer_product_tree.pack(fill="both", expand=True)
    
    #refresh button
    refresh_btn = tk.ttk.Button(products_frame, text="Refresh List", command=refresh_product_list)
    refresh_btn.pack(pady=5)
    
    #cart section
    cart_frame = tk.ttk.LabelFrame(customer_window, text="Shopping Cart", padding=5)
    cart_frame.pack(fill="x", padx=5, pady=5)
    
    #input row
    tk.ttk.Label(cart_frame, text="Product ID:").grid(row=0, column=0, sticky="w", padx=2)
    customer_product_id_entry = tk.ttk.Entry(cart_frame, width=8)
    customer_product_id_entry.grid(row=0, column=1, sticky="w", padx=2)
    
    tk.ttk.Label(cart_frame, text="Quantity:").grid(row=0, column=2, sticky="w", padx=2)
    customer_quantity_entry = tk.ttk.Entry(cart_frame, width=8)
    customer_quantity_entry.grid(row=0, column=3, sticky="w", padx=2)
    
    tk.ttk.Button(cart_frame, text="Add to Cart", command=add_item_to_cart).grid(row=0, column=4, padx=5)
    
    #cart
    customer_cart_tree = tk.ttk.Treeview(
        cart_frame,
        columns=("id", "name", "qty", "price", "total"),
        show="headings",
        height=4
    )
    
    cart_columns = [
        ("id", "ID", 40),
        ("name", "Product", 120),
        ("qty", "Quantity", 60),
        ("price", "Price", 70),
        ("total", "Total", 80)
    ]
    
    for col_id, col_label, col_width in cart_columns:
        customer_cart_tree.heading(col_id, text=col_label)
        customer_cart_tree.column(col_id, width=col_width)
    
    customer_cart_tree.grid(row=1, column=0, columnspan=5, pady=5, sticky="nsew")
    
    tk.ttk.Button(cart_frame, text="Complete Purchase", command=process_purchase).grid(
        row=2, column=0, columnspan=5, pady=2
    )
    
    cart_frame.columnconfigure(0, weight=1)
    cart_frame.columnconfigure(1, weight=1)
    cart_frame.columnconfigure(2, weight=1)
    cart_frame.columnconfigure(3, weight=1)
    cart_frame.columnconfigure(4, weight=1)
    
    return customer_window
#
def setup_manager_window():
    global manager_product_tree, manager_date_entry, manager_report_text
    
    manager_window = tk.Tk()
    manager_window.title("Store - Manager Interface")
    manager_window.geometry("720x580")
    
    #product table
    products_frame = tk.ttk.LabelFrame(manager_window, text="Product Inventory Management", padding=5)
    products_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    manager_product_tree = tk.ttk.Treeview(
        products_frame,
        columns=("id", "name", "category", "price", "stock"),
        show="headings",
        height=8
    )
    
    column_configs = [
        ("id", "ID", 40),
        ("name", "Product Name", 150),
        ("category", "Category", 100),
        ("price", "Unit Price", 80),
        ("stock", "Stock", 80)
    ]
    
    for col_id, col_label, col_width in column_configs:
        manager_product_tree.heading(col_id, text=col_label)
        manager_product_tree.column(col_id, width=col_width)
    
    manager_product_tree.pack(fill="both", expand=True)
    
    #buttons
    button_container = tk.ttk.Frame(products_frame)
    button_container.pack(fill="x", pady=5)
    
    tk.ttk.Button(button_container, text="Add Category", 
                  command=lambda: open_add_category_dialog(manager_window)).pack(side="left", padx=2)
    tk.ttk.Button(button_container, text="Add Product", 
                  command=lambda: open_add_product_dialog(manager_window)).pack(side="left", padx=2)
    tk.ttk.Button(button_container, text="Edit Product", 
                  command=lambda: open_edit_product_dialog(manager_window)).pack(side="left", padx=2)
    tk.ttk.Button(button_container, text="Refresh List", 
                  command=refresh_product_list).pack(side="left", padx=2)
    
    #reports section
    reports_frame = tk.ttk.LabelFrame(manager_window, text="Daily Sales Report", padding=5)
    reports_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    tk.ttk.Label(reports_frame, text="Select Date (YYYY-MM-DD):").pack(side="left", padx=2)
    manager_date_entry = tk.ttk.Entry(reports_frame, width=12)
    manager_date_entry.pack(side="left", padx=2)
    manager_date_entry.insert(0, date.today().isoformat())
    
    tk.ttk.Button(reports_frame, text="Generate Report", command=display_sales_report).pack(side="left", padx=5)
    
    manager_report_text = tk.Text(reports_frame, height=6, width=80)
    manager_report_text.pack(fill="both", expand=True, pady=5)
    
    return manager_window
#
def add_data_if_empty():
    database_connection = sqlite3.connect(DATABASE_FILE)
    database_cursor = database_connection.cursor()
    
    database_cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = database_cursor.fetchone()[0]
    
    if category_count == 0:
        database_cursor.execute("INSERT INTO categories (name_category) VALUES ('Beverages')")
        database_cursor.execute("INSERT INTO categories (name_category) VALUES ('Bakery')")
        
        database_cursor.execute("""
            INSERT INTO products (name_of_product, price, id_category, quantity_at_storage) 
            VALUES ('Cola 0.5L', 75.0, 1, 50)""")
        database_cursor.execute("""
            INSERT INTO products (name_of_product, price, id_category, quantity_at_storage) 
            VALUES ('Sliced loaf', 40.0, 2, 30)""")
        
        database_connection.commit()
    
    database_connection.close()
#
if __name__ == "__main__":
    create_database()
    add_data_if_empty()
    customer_win = setup_customer_window()
    manager_win = setup_manager_window()
    refresh_product_list()
    customer_win.mainloop()