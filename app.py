import tkinter as tk
from tkinter import messagebox

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

ROW_LIST = []
DEFAULT_ROWS = 3

def add_row():
    row_index = len(ROW_LIST) + 1
    percent_label = tk.Label(content, text=f"Row {row_index} Percentage:")
    percent_label.grid(row=row_index, column=0, pady=5)
    percent_entry = tk.Entry(content)
    percent_entry.grid(row=row_index, column=1, pady=5)
    amount_label = tk.Label(content, text=f"Row {row_index} Amount:")
    amount_label.grid(row=row_index, column=3, pady=5)
    amount_entry = tk.Entry(content)
    amount_entry.grid(row=row_index, column=4, pady=5)
    ROW_LIST.append((percent_entry, amount_entry))


def remove_row():
    if ROW_LIST:
        percent_entry, amount_entry = ROW_LIST.pop()
        percent_entry.grid_forget()
        amount_entry.grid_forget()
        percent_label = content.grid_slaves(row=len(ROW_LIST)+1, column=0)[0]
        amount_label = content.grid_slaves(row=len(ROW_LIST)+1, column=3)[0]
        percent_label.grid_forget()
        amount_label.grid_forget()
    



def get_row_data_by_index(index):
    percent_entry, amount_entry = ROW_LIST[index]
    try:
        percent = float(percent_entry.get())
    except ValueError:
        percent = None
    try:
        amount = float(amount_entry.get())
    except ValueError:
        amount = None
    return percent, amount

def validate_percentages():
    total_percentage = 0
    for percent_entry, _ in ROW_LIST:
        try:
            percent = float(percent_entry.get())
            if percent < 0 or percent > 100:
                messagebox.showerror("Input Error", "Percentages must be between 0 and 100.")
                return False
            total_percentage += percent
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric percentages.")
            return False
    if total_percentage != 100:
        messagebox.showerror("Input Error", "Total percentage must equal 100%.")
        return False
    return True

def validate_amounts():
    amount_count = 0
    for _, amount_entry in ROW_LIST:
        try:
            amount = float(amount_entry.get())
            if amount is not None:
                amount_count += 1
        except ValueError:
            pass
    if amount_count == 0:
        messagebox.showerror("Input Error", "Please enter at least one amount.")
        return False
    if amount_count > 1:
        messagebox.showerror("Input Error", "Please enter only one amount.")
        return False
    return True

def calculate_amounts():
    if not validate_percentages() or not validate_amounts():
        return

    total_amount = None
    for i in range(len(ROW_LIST)):
        percent, amount = get_row_data_by_index(i)
        if amount is not None:
            total_amount = amount * 100 / percent
            break

    if total_amount is None:
        messagebox.showerror("Calculation Error", "Unable to determine total amount.")
        return

    for i in range(len(ROW_LIST)):
        percent, amount = get_row_data_by_index(i)
        if amount is None:
            calculated_amount = (percent / 100) * total_amount
            ROW_LIST[i][1].delete(0, tk.END)
            ROW_LIST[i][1].insert(0, f"{calculated_amount:.2f}")

def clear_percentages():
    for percent_entry, _ in ROW_LIST:
        percent_entry.delete(0, tk.END)

def clear_amounts():
    for _, amount_entry in ROW_LIST:
        amount_entry.delete(0, tk.END)

def clear_all():
    clear_percentages()
    clear_amounts()


root = tk.Tk()
root.title("Percentage Composition Calculator")
root.geometry("500x800")

header = tk.Frame(root)
content = tk.Frame(root)
footer = tk.Frame(root)

header.pack(pady=10)
content.pack(pady=10)
footer.pack(pady=10)

header_label = tk.Label(header, text="Percentage Composition Calculator", font=("Arial", 16))
header_label.pack()


add_row_button = tk.Button(footer, text="Add Row", command=add_row)
add_row_button.grid(row=0, column=0, columnspan=1, pady=20)
remove_row_button = tk.Button(footer, text="Remove Row", command=remove_row)
remove_row_button.grid(row=0, column=1, columnspan=1, pady=20)
calculate_button = tk.Button(footer, text="Calculate Amounts", command=calculate_amounts)
calculate_button.grid(row=0, column=2, columnspan=1, pady=20)

reset_label = tk.Label(footer, text="Clear:", font=("Arial", 10))
reset_label.grid(row=1, column=0, pady=10)
clear_percentages_button = tk.Button(footer, text="Percentages", command=clear_percentages)
clear_percentages_button.grid(row=1, column=1, pady=10) 
clear_amounts_button = tk.Button(footer, text="Amounts", command=clear_amounts)
clear_amounts_button.grid(row=1, column=2, pady=10)
clear_all_button = tk.Button(footer, text="All", command=clear_all)
clear_all_button.grid(row=1, column=3, pady=10)

for _ in range(DEFAULT_ROWS):
    add_row()   
import os
basedir = os.path.abspath(os.path.dirname(__file__))
try:
    root.iconbitmap(os.path.join(basedir, 'flask.ico'))
except Exception:
    pass
root.mainloop()
