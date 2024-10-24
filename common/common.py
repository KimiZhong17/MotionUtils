import csv
from re import split as resplit
from tkinter import messagebox

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in resplit('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def write_csv(csv_file, csv_headers, csv_data):
    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(csv_headers)
        csv_writer.writerows(csv_data)
        
def return_to_main_menu(current_window, parent_window):
    if parent_window == None:
        messagebox.showerror("Parent window not exist.")
        return

    if current_window == None:
        messagebox.showerror("No window to close.")
        return
        
    current_window.destroy()
    parent_window.deiconify()