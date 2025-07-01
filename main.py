
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkFont
import pandas as pd
from datetime import datetime, timedelta
import os
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILE_NAME = "expenses.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
    df.to_csv(FILE_NAME, index=False)

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')

        self.selected_item = None

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#34495e')
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=10)
        style.configure('Treeview', font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

        self.setup_ui()

    def setup_ui(self):
        title = ttk.Label(self.root, text="💰 Advanced Expense Tracker", font=('Arial', 18, 'bold'), background='#2c3e50', foreground='white')
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.add_tab = tk.Frame(self.notebook, bg='#34495e')
        self.view_tab = tk.Frame(self.notebook, bg='#34495e')
        self.analytics_tab = tk.Frame(self.notebook, bg='#34495e')

        self.notebook.add(self.add_tab, text="Add/Edit Expense")
        self.notebook.add(self.view_tab, text="View Expenses")
        self.notebook.add(self.analytics_tab, text="Analytics")

        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_analytics_tab()
        self.refresh_table()
        self.update_analytics()

    def setup_add_tab(self):
        frame = tk.Frame(self.add_tab, bg='#34495e')
        frame.pack(pady=20)

        self.date_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Food")
        self.note_var = tk.StringVar()

        tk.Label(frame, text="Date:", bg='#34495e', fg='white').grid(row=0, column=0, padx=10, pady=5)
        self.date_entry = DateEntry(frame, width=12, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=1, column=0, padx=10)

        tk.Label(frame, text="Amount (₹):", bg='#34495e', fg='white').grid(row=0, column=1, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.amount_var).grid(row=1, column=1, padx=10)

        tk.Label(frame, text="Category:", bg='#34495e', fg='white').grid(row=0, column=2, padx=10, pady=5)
        ttk.Combobox(frame, textvariable=self.category_var, values=["Food", "Transport", "Shopping", "Other"]).grid(row=1, column=2, padx=10)

        tk.Label(frame, text="Note:", bg='#34495e', fg='white').grid(row=0, column=3, padx=10, pady=5)
        tk.Entry(frame, textvariable=self.note_var, width=25).grid(row=1, column=3, padx=10)

        self.add_button = tk.Button(frame, text="Add Expense", command=self.add_expense, bg="#27ae60", fg='white')
        self.add_button.grid(row=1, column=4, padx=10)

        self.update_button = tk.Button(frame, text="Update", command=self.update_expense, bg='#f39c12', fg='white')
        self.cancel_button = tk.Button(frame, text="Cancel", command=self.cancel_edit, bg='#e74c3c', fg='white')

    def setup_view_tab(self):
        filter_frame = tk.Frame(self.view_tab, bg='#34495e')
        filter_frame.pack(fill='x', pady=10)

        self.filter_var = tk.StringVar(value="All")
        self.from_date = DateEntry(filter_frame, width=12)
        self.to_date = DateEntry(filter_frame, width=12)

        ttk.Label(filter_frame, text="Category:", background='#34495e', foreground='white').pack(side='left', padx=5)
        ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["All", "Food", "Transport", "Shopping", "Other"]).pack(side='left')

        ttk.Label(filter_frame, text="From:", background='#34495e', foreground='white').pack(side='left', padx=5)
        self.from_date.pack(side='left')

        ttk.Label(filter_frame, text="To:", background='#34495e', foreground='white').pack(side='left', padx=5)
        self.to_date.pack(side='left')

        tk.Button(filter_frame, text="Apply", command=self.refresh_table).pack(side='left', padx=5)
        tk.Button(filter_frame, text="Clear", command=self.clear_filters).pack(side='left')

        self.tree = ttk.Treeview(self.view_tab, columns=["Date", "Category", "Amount", "Note"], show="headings")
        for col in ["Date", "Category", "Amount", "Note"]:
            self.tree.heading(col, text=col)
        self.tree.column("Amount", width=100)
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', lambda e: self.edit_expense())

        action_frame = tk.Frame(self.view_tab, bg='#34495e')
        action_frame.pack()

        tk.Button(action_frame, text="Edit", command=self.edit_expense, bg="#3498db", fg='white').pack(side='left', padx=10)
        tk.Button(action_frame, text="Delete", command=self.delete_expense, bg="#e74c3c", fg='white').pack(side='left', padx=10)

        self.total_label = tk.Label(self.view_tab, text="Total: ₹0.00", font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
        self.total_label.pack(pady=5)

    def setup_analytics_tab(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, self.analytics_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        note = self.note_var.get()
        try:
            amount = float(self.amount_var.get())
        except:
            messagebox.showerror("Error", "Enter valid amount")
            return

        df = pd.read_csv(FILE_NAME)
        new = pd.DataFrame([[date, category, amount, note]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        self.clear_form()
        self.refresh_table()
        self.update_analytics()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = pd.read_csv(FILE_NAME)
        df["Date"] = pd.to_datetime(df["Date"])

        if self.filter_var.get() != "All":
            df = df[df["Category"] == self.filter_var.get()]

        try:
            from_d = self.from_date.get_date()
            to_d = self.to_date.get_date()
            df = df[(df["Date"].dt.date >= from_d) & (df["Date"].dt.date <= to_d)]
        except:
            pass

        total = 0
        for _, row in df.iterrows():
            total += row["Amount"]
            self.tree.insert("", "end", values=[row["Date"].strftime("%Y-%m-%d"), row["Category"], f"₹{row['Amount']:.2f}", row["Note"]])
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        df = pd.read_csv(FILE_NAME)
        df = df[~((df["Date"] == values[0]) & (df["Category"] == values[1]) &
                  (df["Amount"] == float(str(values[2]).replace("₹", ""))) &
                  (df["Note"] == values[3]))]
        df.to_csv(FILE_NAME, index=False)
        self.refresh_table()
        self.update_analytics()

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        self.date_entry.set_date(values[0])
        self.category_var.set(values[1])
        self.amount_var.set(str(values[2]).replace("₹", ""))
        self.note_var.set(values[3])

        self.add_button.grid_remove()
        self.update_button.grid(row=1, column=4, padx=10)
        self.cancel_button.grid(row=2, column=4, padx=10)
        self.selected_item = values
        self.notebook.select(self.add_tab)

    def update_expense(self):
        self.delete_expense()
        self.add_expense()
        self.cancel_edit()

    def cancel_edit(self):
        self.clear_form()
        self.update_button.grid_remove()
        self.cancel_button.grid_remove()
        self.add_button.grid(row=1, column=4, padx=10)

    def clear_form(self):
        self.amount_var.set("")
        self.note_var.set("")
        self.date_entry.set_date(datetime.now().date())

    def clear_filters(self):
        self.filter_var.set("All")
        self.from_date.set_date(datetime.now() - timedelta(days=180))
        self.to_date.set_date(datetime.now())
        self.refresh_table()

    def update_analytics(self):
      self.fig.clf()
      self.ax1 = self.fig.add_subplot(131)  # Pie Chart
      self.ax2 = self.fig.add_subplot(132)  # Monthly Trend
      self.ax3 = self.fig.add_subplot(133)  # Weekly Trend

      df = pd.read_csv(FILE_NAME)
      if df.empty:
          self.canvas.draw()
          return

      df["Date"] = pd.to_datetime(df["Date"])
      df["Weekday"] = df["Date"].dt.day_name()
      df["Month"] = df["Date"].dt.to_period("M")

      # Pie Chart - Category-wise
      category_total = df.groupby("Category")["Amount"].sum()
      colors = plt.cm.Set3.colors[:len(category_total)]
      self.ax1.pie(category_total, labels=category_total.index, autopct="%1.1f%%", startangle=90, colors=colors)
      self.ax1.set_title("Category-wise Distribution", fontsize=10)

      # Line Chart - Monthly showing
      monthly = df.groupby("Month")["Amount"].sum()
      self.ax2.plot(monthly.index.astype(str), monthly.values, marker="o", linestyle='-', color="#3498db")
      self.ax2.set_title("Monthly Trend", fontsize=10)
      self.ax2.set_xticklabels(monthly.index.astype(str), rotation=45)
      self.ax2.grid(True)

      # Bar Chart - Weekly Avg show
      weekly_avg = df.groupby("Weekday")["Amount"].mean().reindex([
          "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
      ])
      self.ax3.bar(weekly_avg.index, weekly_avg.values, color="#e67e22")
      self.ax3.set_title("Avg Spending by Day", fontsize=10)
      self.ax3.set_xticklabels(weekly_avg.index, rotation=45)
      self.ax3.grid(axis='y')

      self.fig.tight_layout()
      self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
