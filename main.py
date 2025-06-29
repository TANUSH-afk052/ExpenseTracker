import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import datetime
import os

FILE_NAME="Expense.csv" #creating a file with certain name

if not os.path.exists(FILE_NAME):
  df=pd.DataFrame(columns=["Date","Category","Amount","Note"])
  df.to_csv(FILE_NAME, index="false")
  
def addthe_expense():
  date = datetime.now().strftime("%d-%m-%y")
  category=category_var.get()
  amount=amount_var.get()
  note=note_var.get()

  if not amount:
    messagebox.showwarning("Input Error","Amount is not provided")
    return

  try:
    amount=float(amount)
  except ValueError:
    messagebox.showerror("Invalid Input", "Amount Must Be Like a Amount")
    return
  df=pd.read_csv(FILE_NAME)
  new_data=pd.DataFrame([[date,category,amount,note]],columns=df.columns)
  df=pd.concat([df,new_data],ignore_index=True)
  df.to_csv(FILE_NAME,index=False)

  messagebox.showinfo('success','expense added.')
  amount_var.set('')
  note_var.set('')
  refresh_table()

def refresh_table():
  for row in tree.get_children():
    tree.delete.row
  df=pd.read_csv(FILE_NAME)
  for _, row in df.iterrows():
    tree.insert("","end", values=list(row))

#Basic UI
root=tk.Tk()
root.tittle('Expense tracker')
root.geometry('600x400')

input_frame=tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text='Amount').grid(row=0, column=0)
tk.Lable(input_frame, text='Category').grid(row=0,column=1)
tk.Label(input_frame,text="Note").grid(row=0,column=2)

amount_var=tk.StringVar()
category_var=tk.StringVar(value='food')
note_var=tk.StringVar()

tk.Entry(input_frame,textvariable=amoun_var,width=10).grid(row=1,column=0)
ttk.Combobox(input_frame,textvariable=category_var, values=['food','transport','shopping','other'],width=10).grid(row=1,colum=1)
tk.Entry(input_frame,textvariable=note_var,width=20).grid(row=1. column=2)
tk.Button(input_frame, text="ADD EXPENSE", command=addthe_expense).grid(row=1,column=3,padx=10)

tree=ttk.Treeview(root,colums=("Date","Category","Amount",'Note'),show="headings")
for col in ("Date","Category","Amount","Note"):
  tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

refresh_table()
root.mainloop()
