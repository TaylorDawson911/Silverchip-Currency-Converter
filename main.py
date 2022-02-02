#TODO; NOTHING :)


########################################################################################################################
################################################### IMPORT STUFF HERE ##################################################
########################################################################################################################

from datetime import datetime
import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import ttk
from threading import Thread
from time import sleep
from datetime import date

########################################################################################################################
############################################## ASSIGN GLOBAL VARIABLES HERE ############################################
########################################################################################################################

is_staff = False  # the user is not a staff first

OptionList1 = [  # This is the array to store the "FROM" Value. So just GBP
    "GBP",
]

OptionList2 = [  # This is the array to store the "TO" Value.
    "USD",
    "EUR",
    "BRL",
    "JPY",
    "TRY"
]


########################################################################################################################
################################################### ADD FUNCTIONS HERE #################################################
########################################################################################################################

# This function is the main login GUI. It asks for the users username and password, then it hands the variables off
# the function "login_verify()"

def view_2(tree):
    con1 = sqlite3.connect("transactions data.db")

    cur1 = con1.cursor()

    cur1.execute("SELECT Amount_GBP, Amount, Currency, Date FROM transactions")

    rows = cur1.fetchall()

    for row in rows:
        print(row)

        tree.insert("", tk.END, values=row)

    con1.close()

def View():
    global root

    con1 = sqlite3.connect("transactions data.db")

    cur1 = con1.cursor()

    root = tk.Tk()

    tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Amount(GBP)")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Amount(after conversion)")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Currency converted to")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Date")

    tree.pack()

    root.title("Previous Transactions")

    cur1.execute("SELECT Amount_GBP, Amount, Currency, Date FROM transactions")
    root.resizable(False, False)
    Button(tree, text="Clear", width=10, height=1, bg="orange", command=delete).place(x=720, y=200)
    view_2(tree)


def delete():
    temp = sqlite3.connect("transactions data.db")
    db = temp.cursor()
    db.execute("""DROP TABLE IF EXISTS transactions""")
    db.execute(("""CREATE TABLE IF NOT EXISTS transactions
    (Amount_GBP, Amount, Currency, Date )"""))
    root.destroy()
    View()

def login():
    db = sqlite3.connect("login.db")  # Connects to database
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS userlogin
    (Username, Password)''')
    c.execute('''INSERT INTO userlogin
       VALUES (?,?)''',
              ("admin", "admin"))

    db.commit()  # commits the changes
    db.close()  # closes the database

    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")

    # declaring variables

    global username_verify
    global password_verify

    global message

    username_verify = StringVar()
    password_verify = StringVar()
    message = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, width="300", text="Please enter details below", bg="orange", fg="white").pack()
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()

    Label(login_screen, text="").pack()
    Label(login_screen, text="", textvariable=message).pack(padx=0, pady=0)

    Button(login_screen, text="Login", width=10, height=1, bg="orange", command=login_verify).pack()


# This function verifies the login
# it gets the username and password from the "login" function, then checks in the database
# "login.db" to see if that is a correct login. If not then it  will say invalid password or username
def login_verify():
    # assigning variables
    global is_staff
    username1 = username_verify.get()
    password1 = password_verify.get()
    # connects to database
    db = sqlite3.connect('login.db')
    c = db.cursor()
    c.execute('SELECT * FROM userlogin WHERE Username = ? AND Password = ?', (username1, password1))

    # if username:password combo found
    if c.fetchall():
        global hide
        global test

        is_staff = True
        message.set("Login success")
        login_screen.destroy()
        tk.Button(main_screen, text="logout", command=logout, bg="orange",height=1, width=5).place(x=245, y=5)

        test = tk.Button(main_screen, text="previous transactions", command=View, bg="orange", height=1, width=16)
        test.place(x=170,y=210)
        con1 = sqlite3.connect("transactions data.db")

        cur1 = con1.cursor()

        cur1.execute("""CREATE tABLE IF NOT EXISTS transactions (Amount_GBP, Amount, Currency, Date)""")

        con1.commit()

        con1.close()



    else:  # if not found

        if not username1:  # error handling
            message.set("Username or Password cannot be blank")
        elif not password1:
            message.set("Username or Password cannot be blank")
        else:
            message.set("Wrong username or password!!!")


# this program logs the user out
# this only shows if the user is logged in

def logout():
    # assigning variables
    global is_staff
    is_staff = False
    test.place_forget()
    tk.Button(main_screen, text="login", command=login,bg="orange", height=1, width=5).place(x=245, y=5)


# this function is for viewing the exchange rates
# it has the exchange rates hard coded into the program.

def exchange_rates():
    ws = Tk()
    ws.title('Exchange Rates')
    ws.geometry('300x250')

    set = ttk.Treeview(ws)
    set.pack()

    set['columns'] = ('Currency', 'Rate')
    set.column("#0", width=0, stretch=NO)
    set.column("Currency", anchor=CENTER, width=80)
    set.column("Rate", anchor=CENTER, width=80)

    set.heading("#0", text="", anchor=CENTER)
    set.heading("Currency", text="Currency", anchor=CENTER)
    set.heading("Rate", text="Rate", anchor=CENTER)

    set.insert(parent='', index='end', iid=0, text='',
               values=('USD', '1 : 1.40'))

    set.insert(parent='', index='end', iid=1, text='',
               values=('EUR', "1 : 1.14"))

    set.insert(parent='', index='end', iid=3, text='',
               values=('BRL', '1 : 4.77'))

    set.insert(parent='', index='end', iid=4, text='',
               values=('JPY', '1 : 151.05'))

    set.insert(parent='', index='end', iid=5, text='',
               values=('TRY', '1 : 5.68'))
    ws.resizable(False, False)
    ws.mainloop()


# this function is for viewing the transaction fees
# it has the transaction fees hard coded into the program.
def transaction_fees():
    ws = Tk()
    ws.title('Transaction Fees')
    ws.geometry('300x250')

    set = ttk.Treeview(ws)
    set.pack()

    set['columns'] = ('Amount', 'Fee')
    set.column("#0", width=0, stretch=NO)
    set.column("Amount", anchor=CENTER, width=80)
    set.column("Fee", anchor=CENTER, width=80)

    set.heading("#0", text="", anchor=CENTER)
    set.heading("Amount", text="Amount", anchor=CENTER)
    set.heading("Fee", text="Fee", anchor=CENTER)

    # This is just the indexing for the transaction fees
    set.insert(parent='', index='end', iid=0, text='',
               values=('Up to £300', '3.5%'))

    set.insert(parent='', index='end', iid=1, text='',
               values=('Over £300', "3%"))

    set.insert(parent='', index='end', iid=3, text='',
               values=('Over £750', '2.5%'))

    set.insert(parent='', index='end', iid=4, text='',
               values=('Over £1000', '2%'))

    set.insert(parent='', index='end', iid=5, text='',
               values=('Over £2000', '1.5%'))
    ws.resizable(False, False)
    ws.mainloop()


# This function is the body of the program it does a plethora of things. it includes the buttons to go to these
# functions;calculate,login,logout,exchange rates,transaction rates and select currency to calculate. it basically
# acts as a body for all the other functions, also outputs the totals
def main_gui_screen(arg):
    # assigning variables
    global main_screen
    global e1
    global variable
    global variable1
    global total_conversion
    global total_transaction_fee
    global grand_total
    global message1
    global is_staff
    global total_time
    main_screen = Tk()
    main_screen.geometry('300x250')
    main_screen.title("Currency Converter")
    variable = tk.StringVar(main_screen)
    variable.set("GBP")

    tk.OptionMenu(main_screen, variable, *OptionList1)

    variable1 = tk.StringVar(main_screen)
    variable1.set(OptionList2[0])

    opt = tk.OptionMenu(main_screen, variable1, *OptionList2)
    opt.config(width=10,bg="orange", font=('Helvetica', 12))
    opt.place(x=75, y=40)

    # these variables just turns the variables into tkinter strings
    total_conversion = tk.StringVar()
    total_transaction_fee = tk.StringVar()
    grand_total = tk.StringVar()
    message1 = tk.StringVar()
    total_time = tk.StringVar()

    Label(main_screen, text="", fg='red', textvariable=message1).place(x=10, y=134)  # error handling output


    labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
    labelTest.pack(side="top")

    # This block of "code" is for making the gui look good for user experience
    tk.Label(main_screen, text="TIME",textvariable=total_time,font=('Helvetica', 8)).place(x=10, y=5)
    tk.Label(main_screen, text="To",font=('Helvetica', 12)).place(x=130, y=10)
    tk.Label(main_screen, text="Amount").place(x=10, y=80)
    tk.Label(main_screen, text="The Total Conversion:").place(x=10, y=155)
    tk.Label(main_screen, text="", font=('Helvetica', 8), fg='red', textvariable=total_conversion).place(x=130, y=156)
    tk.Label(main_screen, text="The Transaction Fee:").place(x=10, y=175)
    tk.Label(main_screen, text="", font=('Helvetica', 8), fg='red', textvariable=total_transaction_fee).place(x=125,
                                                                                                              y=176)
    tk.Label(main_screen, text="Grand Total:").place(x=10, y=195)
    tk.Label(main_screen, text="", font=('Helvetica', 8), fg='red', textvariable=grand_total).place(x=80, y=196)


    if is_staff:  # if is_staff = True
        tk.Button(main_screen, text="logout", command=logout,bg="orange", height=1, width=5).place(x=245, y=5)
        # Show the logout btn
    else:  # if is_staff = False
        tk.Button(main_screen, text="login", command=login,bg="orange", height=1, width=5).place(x=245, y=5)

    tk.Button(main_screen, text="exchange rates",bg="orange", command=exchange_rates, height=1, width=11).place(x=50, y=110)
    tk.Button(main_screen, text="transaction fees",bg="orange", command=transaction_fees, height=1, width=11).place(x=150, y=110)
    tk.Button(main_screen, text="save", bg="orange", command=save, height=1, width=4).place(x=210, y=75)

    e1 = tk.Entry(main_screen)
    e1.place(x=80, y=80)

    main_screen.resizable(False, False)
    main_screen.mainloop()


# This function is the logic of the program
# it gets the "to" variable, which is what exchange currency you want to use from the "main_gui_screen"
# it then does a formula to work out the conversion,transaction fee and Grand Total, which then passes through
# to "main_gui_screen"
def save():
    if 2500 >= amount >= 50:
        today = date.today()
        temp = sqlite3.connect("transactions data.db")
        db = temp.cursor()
        db.execute("""CREATE tABLE IF NOT EXISTS transactions (Amount_GBP, Amount, Currency, Date)""")
        db.execute("""INSERT INTO transactions 
        VALUES (?, ?, ?, ?)""", (amount, conversion, to, today))
        temp.commit()


def threaded_function(arg):
    global main_gui_screen

    while True:
        try:
            # assigning variables
            global message1
            global is_staff
            global main_gui_screen
            global variable
            global variable1
            global time
            global amount
            global conversion
            global to
            global current_time


            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            total_time.set(current_time)

            to = variable1.get()
            message1.set("")

            try:
                amount = e1.get()
                amount = float(e1.get())

            except ValueError:
                message1.set("Error: Input Has To Be A Number")

            if to == "USD":
                currency = 1.40
            if to == "EUR":
                currency = 1.14
            if to == "BRL":
                currency = 4.77
            if to == "JPY":
                currency = 151.05
            if to == "TRY":
                currency = 5.68
            if not amount:
                message1.set("Input a number from £50 - £2500")
            if amount < 50:
                message1.set("Error: Cannot Be Less Than £50")
                amount = 0
                transaction_fee = 0
            elif amount <= 300:  # up to 300 GBP
                transaction_fee = 0.035  # 3.5%
            elif 300 < amount <= 750:  # over 300 GBP
                transaction_fee = 0.03  # 3%
            elif 750 < amount <= 1000:  # over 750 GBP
                transaction_fee = 0.02  # 2%
            elif 1000 < amount <= 2500:  # over 100 and up to 2500
                transaction_fee = 0.015  # 1.5%
            elif amount >= 2501:
                message1.set("Error: Cannot Be More Than £2500")
                amount = 0
                transaction_fee = 0

            # this block of code is the algorithm for calculating the conversion and applying the discount, if needed
            conversion = amount * currency
            transaction_fee = conversion * transaction_fee
            if is_staff:
                discount = transaction_fee * 0.05  # 5
                transaction_fee = transaction_fee - discount
            total = conversion - transaction_fee

            conversion = round(conversion, 2)
            total = round(total, 2)
            transaction_fee = round(transaction_fee, 2)

            total_conversion.set(conversion)
            total_transaction_fee.set(transaction_fee)
            grand_total.set(total)


        except:

            pass



        sleep(1)


if __name__ == "__main__":
    thread2 = Thread(target=main_gui_screen, args=(12,))
    thread = Thread(target=threaded_function, args=(12,))
    thread2.start()
    thread.start()
