import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, Listbox, Scrollbar
import datetime
import os
class BillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Management System")
        self.root.geometry("700x600")
        self.root.config(bg="#f5f5f5")
        self.customer_name = tk.StringVar()
        self.item_name = tk.StringVar()
        self.quantity = tk.IntVar(value=0)
        self.price = tk.DoubleVar(value=0.0)
        self.items = {}
        self.bill_folder = "bills"
        os.makedirs(self.bill_folder, exist_ok=True)
        title = tk.Label(root, text="BILL MANAGEMENT SYSTEM",font=("Arial", 18, "bold"), bg="#4a90e2", fg="white",
         pady=10)
        title.pack(fill=tk.X)
        f1 = tk.Frame(root, bg="#f5f5f5")
        f1.place(x=20, y=70, width=660, height=50)
        tk.Label(f1, text="Customer Name:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
        e_customer = tk.Entry(f1, textvariable=self.customer_name, font=("Arial", 12), width=30)
        e_customer.grid(row=0, column=1)
        f2 = tk.Frame(root, bg="#f5f5f5")
        f2.place(x=20, y=130, width=660, height=120)
        tk.Label(f2, text="Item Name:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5)
        e_item = tk.Entry(f2, textvariable=self.item_name, font=("Arial", 12), width=20)
        e_item.grid(row=0, column=1, pady=5)
        tk.Label(f2, text="Quantity:", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5)
        e_qty = tk.Entry(f2, textvariable=self.quantity, font=("Arial", 12), width=20)
        e_qty.grid(row=1, column=1, pady=5)
        tk.Label(f2, text="Price per item:", font=("Arial", 12), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5)
        e_price = tk.Entry(f2, textvariable=self.price, font=("Arial", 12), width=20)
        e_price.grid(row=2, column=1, pady=5)
        def clear_qty(event):
            if self.quantity.get() == 0:
                e_qty.delete(0, tk.END)
        def reset_qty(event):
            if e_qty.get().strip() == "":
                self.quantity.set(0)
        def clear_price(event):
            if self.price.get() == 0.0:
                e_price.delete(0, tk.END)
        def reset_price(event):
            if e_price.get().strip() == "":
                self.price.set(0.0)
        e_qty.bind("<FocusIn>", clear_qty)
        e_qty.bind("<FocusOut>", reset_qty)
        e_price.bind("<FocusIn>", clear_price)
        e_price.bind("<FocusOut>", reset_price)
        btn_add = tk.Button(f2, text="Add Item", command=self.add_item,bg="#4CAF50", fg="white", 
        font=("Arial", 12, "bold"), width=15)
        btn_add.grid(row=1, column=2, padx=20)
        e_customer.bind("<Return>", lambda e: e_item.focus_set())
        e_item.bind("<Return>", lambda e: e_qty.focus_set())
        e_qty.bind("<Return>", lambda e: e_price.focus_set())
        e_price.bind("<Return>", lambda e: self.add_item() or e_item.focus_set())
        f3 = tk.Frame(root, bg="#f5f5f5")
        f3.place(x=20, y=270, width=660, height=250)
        self.txtarea = tk.Text(f3, font=("Courier New", 12))
        self.txtarea.pack(fill=tk.BOTH, expand=1)
        f4 = tk.Frame(root, bg="#f5f5f5")
        f4.place(x=20, y=540, width=660, height=50)
        tk.Button(f4, text="Generate Bill", command=self.generate_bill,bg="#2196F3", fg="white", 
        font=("Arial", 12, "bold"), width=15).grid(row=0, column=0, padx=10)
        tk.Button(f4, text="Save Bill", command=self.save_bill,bg="#9C27B0", fg="white", 
        font=("Arial", 12, "bold"), width=15).grid(row=0, column=1, padx=10)
        tk.Button(f4, text="View History", command=self.view_history,bg="#FF9800", fg="white", 
        font=("Arial", 12, "bold"), width=15).grid(row=0, column=2, padx=10)
        tk.Button(f4, text="Clear", command=self.clear_data,bg="#f44336", fg="white", 
        font=("Arial", 12, "bold"), width=10).grid(row=0, column=3, padx=10)
        self.welcome_bill()
    def welcome_bill(self):
        self.txtarea.delete(1.0, tk.END)
        self.txtarea.insert(tk.END, "\t  XYZ STORE\n")
        self.txtarea.insert(tk.END, f"Customer: {self.customer_name.get()}\n")
        self.txtarea.insert(tk.END, f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        self.txtarea.insert(tk.END, "="*50 + "\n")
        self.txtarea.insert(tk.END, f"{'Item':<20}{'Qty':<10}{'Price':<10}\n")
        self.txtarea.insert(tk.END, "-"*50 + "\n")
    def add_item(self):
        name = self.item_name.get().strip()
        qty = self.quantity.get()
        price = self.price.get()
        if name == "" or qty <= 0 or price <= 0:
            messagebox.showerror("Error", "Please enter valid item details!")
            return
        self.items[name] = (qty, price)
        messagebox.showinfo("Success", f"{name} added successfully!")
        self.item_name.set("")
        self.quantity.set(0)
        self.price.set(0.0)
    def generate_bill(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items added!")
            return
        self.welcome_bill()
        total = 0
        for item, data in self.items.items():
            qty, price = data
            amount = qty * price
            total += amount
            self.txtarea.insert(tk.END, f"{item:<20}{qty:<10}{amount:<10.2f}\n")
        self.txtarea.insert(tk.END, "-"*50 + "\n")
        self.txtarea.insert(tk.END, f"{'Total Amount:':<30} ₹{total:.2f}\n")
        self.txtarea.insert(tk.END, "="*50)
        messagebox.showinfo("Bill Generated", "Bill generated successfully!")
        filename = f"{self.customer_name.get()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(self.bill_folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.txtarea.get("1.0", tk.END))
    def save_bill(self):
        bill_content = self.txtarea.get("1.0", tk.END)
        file_name = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Bill As")
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(bill_content)
                messagebox.showinfo("Success", "Bill saved successfully!")
            except Exception as e:
                messagebox.showerror("Error saving bill", str(e))
    def view_history(self):
        history_window = Toplevel(self.root)
        history_window.title("Bill History")
        history_window.geometry("500x400")
        scrollbar = Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = Listbox(history_window, font=("Arial", 12))
        listbox.pack(fill=tk.BOTH, expand=1)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        files = os.listdir(self.bill_folder)
        if not files:
            listbox.insert(tk.END, "No bills found.")
            return
        for file in sorted(files):
            listbox.insert(tk.END, file)
        def open_bill(event):
            selected = listbox.get(listbox.curselection())
            path = os.path.join(self.bill_folder, selected)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            view_window = Toplevel(history_window)
            view_window.title(f"Bill: {selected}")
            text = tk.Text(view_window, font=("Courier New", 12))
            text.pack(fill=tk.BOTH, expand=1)
            text.insert(tk.END, content)
        listbox.bind("<Double-Button-1>", open_bill)
    def clear_data(self):
        self.customer_name.set("")
        self.item_name.set("")
        self.quantity.set(0)
        self.price.set(0.0)
        self.items.clear()
        self.welcome_bill()
root = tk.Tk()
app = BillApp(root)
root.mainloop()