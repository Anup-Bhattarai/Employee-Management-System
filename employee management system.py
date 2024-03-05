from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as msg
import mysql.connector


# FUNCTION DECLARATIONS

def add_data():
    if t1.get() == "" or t2.get() == "" or t3.get() == "" or t4.get() == "":
        msg.showerror("Error", "All fields are required")
    else:
        try:
            conn = mysql.connector.connect(host='localhost', username='root', password='Ke200207@', database='Employee')
            my_cursor = conn.cursor()
            my_cursor.execute('INSERT INTO employee (Employee_ID, E_Name, Department, Salary) VALUES (%s, %s, %s, %s)',
                              (t1.get(), t2.get(), t3.get(), t4.get()))
            conn.commit()
            fetch_data()
            conn.close()
            msg.showinfo('Success', 'Employee Data has been Added', parent=root)
        except Exception as e:
            msg.showerror('Error', f"Due To: {str(e)}", parent=root)


def fetch_data():
    conn = mysql.connector.connect(host='localhost', username='root', password='Ke200207@', database='Employee')
    my_cursor = conn.cursor()
    my_cursor.execute('SELECT * FROM employee')
    data = my_cursor.fetchall()
    if len(data) != 0:
        employee_table.delete(*employee_table.get_children())
        for i in data:
            employee_table.insert('', END, values=i)
        conn.commit()
    conn.close()


def get_cursor(event=''):
    cursor_row = employee_table.focus()
    content = employee_table.item(cursor_row)
    data = content['values']

    t1.set(data[0])
    t2.set(data[1])
    t3.set(data[2])
    t4.set(data[3])


def update_data():
    if t1.get() == "" or t2.get() == "" or t3.get() == "" or t4.get() == "":
        msg.showerror("Error", "All fields are required")
    else:
        try:
            update = msg.askyesno('Update', 'Do you want to update this employee data?', parent=root)
            if update:
                conn = mysql.connector.connect(host='localhost', username='root', password='Ke200207@',
                                               database='Employee')
                my_cursor = conn.cursor()
                my_cursor.execute(
                    'UPDATE employee SET E_Name=%s, Department=%s, Salary=%s WHERE Employee_ID=%s',
                    (t2.get(), t3.get(), t4.get(), t1.get()))
                conn.commit()
                fetch_data()
                conn.close()
                msg.showinfo('Success', 'Employee Successfully Updated', parent=root)
        except Exception as e:
            msg.showerror('Error', f'Due To: {str(e)}', parent=root)


def delete_data():
    if t1.get() == '':
        msg.showerror('Error', 'Employee ID is required for deletion')
    else:
        try:
            Delete = msg.askyesno('Delete', 'Are you sure you want to delete this employee?', parent=root)
            if Delete:
                conn = mysql.connector.connect(host='localhost', username='root', password='Ke200207@',
                                               database='Employee')
                my_cursor = conn.cursor()
                sql = 'DELETE FROM employee WHERE Employee_ID=%s'
                value = (t1.get(),)
                my_cursor.execute(sql, value)
                conn.commit()
                fetch_data()
                conn.close()
                msg.showinfo('Delete', 'Employee Successfully Deleted', parent=root)
        except Exception as e:
            msg.showerror('Error', f'Due To: {str(e)}', parent=root)


def reset_data():
    t1.set("")
    t2.set("")
    t3.set("")
    t4.set("")


def search_data():
    if q.get() == '':
        fetch_data()
    else:
        try:
            conn = mysql.connector.connect(host='localhost', username='root', password='Ke200207@',
                                           database='Employee')
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM employee WHERE E_Name LIKE '%" + q.get() + "%'")
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                employee_table.delete(*employee_table.get_children())
                for i in rows:
                    employee_table.insert("", END, values=i)
            conn.commit()
            conn.close()
        except Exception as e:
            msg.showerror('Error', f'Due To: {str(e)}', parent=root)


# TKINTER WINDOW SETUP

root = Tk()
root.title("Employee Management System")
root.geometry("800x500")
root.resizable(False, False)

# Variables for employee attributes
t1 = StringVar()  # Employee ID
t2 = StringVar()  # Name
t3 = StringVar()  # Department
t4 = StringVar()  # Salary

# SETUP FRAMES
wrapper1 = LabelFrame(root, text="Employee Data")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text="Employee Information")
wrapper1.pack(fill=BOTH, expand="yes", padx=20, pady=10)
wrapper2.pack(fill=BOTH, expand="yes", padx=20, pady=10)
wrapper3.pack(fill=BOTH, expand="yes", padx=20, pady=10)

# Employee Data Section
Label(wrapper1, text="Employee ID").grid(row=0, column=0, padx=10, pady=5)
Label(wrapper1, text="Name").grid(row=1, column=0, padx=10, pady=5)
Label(wrapper1, text="Department").grid(row=2, column=0, padx=10, pady=5)
Label(wrapper1, text="Salary").grid(row=3, column=0, padx=10, pady=5)

Entry(wrapper1, textvariable=t1).grid(row=0, column=1, padx=10, pady=5)
Entry(wrapper1, textvariable=t2).grid(row=1, column=1, padx=10, pady=5)
Entry(wrapper1, textvariable=t3).grid(row=2, column=1, padx=10, pady=5)
Entry(wrapper1, textvariable=t4).grid(row=3, column=1, padx=10, pady=5)

Button(wrapper1, text="Add Employee", command=add_data).grid(row=4, column=0, padx=10, pady=5)
Button(wrapper1, text="Update Employee", command=update_data).grid(row=4, column=1, padx=10, pady=5)
Button(wrapper1, text="Delete Employee", command=delete_data).grid(row=4, column=2, padx=10, pady=5)
Button(wrapper1, text="Clear Fields", command=reset_data).grid(row=4, column=3, padx=10, pady=5)

# Search Section
q = StringVar()
Label(wrapper2, text="Search").pack(side=tk.LEFT, padx=10)
Entry(wrapper2, textvariable=q).pack(side=tk.LEFT, padx=10)
Button(wrapper2, text="Search", command=search_data).pack(side=tk.LEFT, padx=10)
Button(wrapper2, text="Show All", command=fetch_data).pack(side=tk.LEFT, padx=10)

# Employee Table
scroll_x = Scrollbar(wrapper3, orient=HORIZONTAL)
scroll_y = Scrollbar(wrapper3, orient=VERTICAL)
employee_table = ttk.Treeview(wrapper3, columns=("1", "2", "3", "4"), xscrollcommand=scroll_x.set,
                              yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=employee_table.xview)
scroll_y.config(command=employee_table.yview)
employee_table.heading("1", text="Employee ID")
employee_table.heading("2", text="Name")
employee_table.heading("3", text="Department")
employee_table.heading("4", text="Salary")
employee_table['show'] = 'headings'
employee_table.pack(fill=BOTH, expand=True)
employee_table.bind("<ButtonRelease-1>", get_cursor)

fetch_data()

root.mainloop()
