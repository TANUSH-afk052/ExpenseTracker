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
