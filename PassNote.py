from tkinter import *
import mysql.connector
import csv
from tkinter import ttk

# general setup
root = Tk()
root.title("PassNote Version 1")
root.geometry("350x250")

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = ''' use password as the same  ''',
        database = "mypassword",
        )

my_cursor = mydb.cursor()

title_label = Label(root, text="PassNote", font=("comicsans", 16)).grid(row=0, column=0, columnspan=2, padx=50, pady=10)

def clear():
    program_box.delete(0, END)
    email_box.delete(0, END)
    password_box.delete(0, END)
    start_date_box.delete(0, END)


def add_database():
    sql_command = "INSERT INTO password (program, email, password_name, start_date) VALUES (%s, %s, %s, %s)"
    values = (program_box.get(), email_box.get(), password_box.get(), start_date_box.get())
    my_cursor.execute(sql_command, values)

    mydb.commit()
    clear()


def show_password():
    new_win = Tk()
    new_win.title("Show Password")
    new_win.geometry("400x400")

    my_cursor.execute("SELECT * FROM password")
    result = my_cursor.fetchall()

    for row, i in enumerate(result):
        lookup_label = Label(new_win, text=i)
        lookup_label.grid(row=row, sticky=W, padx=10)

    csv_button = Button(new_win, text="Save to Excel", command=lambda: write_to_csv(result))
    csv_button.grid(row=row+1, column=0)


def write_to_csv(result):
    with open("password.csv", "a", newline="") as f:
        w = csv.writer(f, dialect="excel")
        w.writerow(result)


# search password
def search():
    new_win_search = Tk()
    new_win_search.title("Search Program Name")
    new_win_search.geometry("600x400")

    def search_now():
        sql = ""
        selected = drop.get()

        if selected == "Search by":
            search_by = Label(new_win_search, text="Please select something")
            search_by.grid(row=2, column=0, padx=5)

        if selected == "program":           
            sql = "SELECT * FROM password WHERE program = %s"           
            

        if selected == "email":
            sql = "SELECT * FROM password WHERE email = %s" 
            
       
        searched = search_box.get()
        # sql = "SELECT * FROM password WHERE program = %s"
        name = (searched, )
        result = my_cursor.execute(sql, name)
        result = my_cursor.fetchall()

        if not result:
            result = "Record not found"
            search_label = Label(new_win_search, text=result)
            search_label.grid(row=3, column=0, padx=10, columnspan=2)

        else:
            for row, i in enumerate(result):
                row = row + 2
                lookup_label = Label(new_win_search, text=i)
                lookup_label.grid(row=row, sticky=W, padx=10)
                
       
        # search_label = Label(new_win_search, text=result)
        # search_label.grid(row=3, column=0, padx=10, columnspan=2)
        

    # create entry box search
    search_box = Entry(new_win_search)
    search_box.grid(row=0, column=1, padx=10, pady=10)

    search_label = Label(new_win_search, text="Search by")
    search_label.grid(row=0, column=0, padx=10, pady=10)

    search_button = Button(new_win_search, text="Search", command=search_now)
    search_button.grid(row=1, column=0,columnspan=2, padx=10)

    # create drop down box
    drop = ttk.Combobox(new_win_search, value=["Search by","program","email"])
    drop.current(0) # set "Search by" to be default
    drop.grid(row=0, column=2)



# Creating Label
program_label = Label(root, text="Program",).grid(row=1, column=0, sticky=W, padx=10)
email_label = Label(root, text="Email",).grid(row=2, column=0, sticky=W, padx=10)
password_label = Label(root, text="Password",).grid(row=3, column=0, sticky=W, padx=10)
start_label = Label(root, text="Start Date",).grid(row=4, column=0, sticky=W, padx=10)

# Creating Entry
program_box = Entry(root, width=35)
program_box.grid(row=1, column=1)

email_box = Entry(root, width=35)
email_box.grid(row=2, column=1, pady=5)

password_box = Entry(root, width=35)
password_box.grid(row=3, column=1, pady=5)

start_date_box = Entry(root, width=35)
start_date_box.grid(row=4, column=1, pady=5)

# Creating Button
submit_button = Button(root, text="Remember", command=add_database)
submit_button.grid(row=5, column=0,padx=10,pady=10)

clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=5, column=1, pady=10)

show_password_btn = Button(root, text="Show Password", command=show_password)
show_password_btn.grid(row=6, column=0, padx =5)

# Search Program
search_program = Button(root, text="Search", command=search)
search_program.grid(row=6, column=1, sticky=W, padx=10)


root.mainloop()

