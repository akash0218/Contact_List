from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from datetime import datetime

conn = sqlite3.connect("contacts.db")
root = Tk()
root.title("Contact List")
width = 400
height = 720
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw / 2) - (width / 2)
y = (sh / 2) - ((height / 2) + 50)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

ADDRESS_TYPES = [
    "Home",
    "Work",
    "Other"
]
PHONENUMBER_TYPES = [
    "Home",
    "Work",
    "Cell",
    "Fax",
    "Other"
]
DATE_TYPES = [
    "Birthday",
    "Anniversary",
    "Other"
]

FIRSTNAME = StringVar()
MIDDLENAME = StringVar()
LASTNAME = StringVar()
ADDRESSTYPE = StringVar()
ADDRESSTYPE.set(ADDRESS_TYPES[0])
STREET = StringVar()
CITY = StringVar()
STATE = StringVar()
ZIP = IntVar()
PHONETYPE = StringVar()
PHONETYPE.set(PHONENUMBER_TYPES[0])
PHONEAREACD = StringVar()
PHONENUMBER = StringVar()
DATETYPE = StringVar()
DATETYPE.set(DATE_TYPES[0])
DATE = StringVar()
SEARCHTERM = StringVar()


def Database():
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `contact` (Contact_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, Fname TEXT, Mname TEXT, Lname TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `address` (address_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, address_type TEXT, address TEXT, city TEXT, state TEXT, zip INTEGER, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `phone` (phone_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, phone_type TEXT, area_code TEXT, number TEXT, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `date` (date_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, date_type TEXT, date TEXT, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
    cursor.execute("SELECT * FROM `contact` ORDER BY `lname` ASC")
    fetch = cursor.fetchall()
    tree.delete(*tree.get_children())
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()


def SearchDatabase():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `contact` ORDER BY `lname` ASC")
    if SEARCHTERM.get() == "":
        fetch = cursor.fetchall()
    else:
        cursor.execute("SELECT DISTINCT contact.contact_id, contact.fname, contact.mname, contact.lname"
                       " FROM `contact` LEFT JOIN address ON(contact.contact_id = address.contact_id) "
                       "LEFT JOIN phone ON(contact.contact_id = phone.contact_id) WHERE "
                       "LOWER(contact.fname) LIKE :search "
                       "OR LOWER(contact.mname) LIKE :search "
                       "OR LOWER(contact.lname) LIKE :search "
                       "OR LOWER(address.address) LIKE :search "
                       "OR LOWER(address.city) LIKE :search "
                       "OR LOWER(address.state) LIKE :search "
                       "OR address.zip like :search "
                       "OR phone.area_code like :search "
                       "OR phone.number like :search "
                       "ORDER BY contact.lname ASC", {"search": SEARCHTERM.get()})
        fetch = cursor.fetchall()
    tree.delete(*tree.get_children())
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()

def Add_cnt(flag):
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" \
            or ADDRESSTYPE.get() == "" or STREET.get() == "" or CITY.get() == "" or STATE.get() == "" or ZIP.get() == "" \
            or PHONETYPE.get() == "" \
            or PHONEAREACD.get() == "" or PHONENUMBER.get() == "" or DATETYPE.get() == "" or DATE.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        return
    else:
        if len(str(ZIP.get()).replace(" ", "")) != 5 or str(ZIP.get()).isnumeric() != True:
            result = tkMessageBox.showwarning('', 'ZIP Code is INVALID', icon="warning")
            return
        if len(str(PHONEAREACD.get()).replace(" ", "")) != 3:
            result = tkMessageBox.showwarning('', 'Area Code is INVALID(must be 3 digits)', icon="warning")
            return
        if len(str(PHONENUMBER.get()).replace(" ", "")) != 7:
            result = tkMessageBox.showwarning('', 'Phone number is INVALID(must be 7 digits)', icon="warning")
            return
        try:
            date_format = '%m/%d/%Y'
            date_obj = datetime.strptime(DATE.get(), date_format)
        except ValueError:
            result = tkMessageBox.showwarning('', 'Date Must be MM/DD/YYYY', icon="warning")
            return

        tree.delete(*tree.get_children())
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `contact` (Fname, MName, Lname) VALUES(?, ?, ?)",
                        (str(FIRSTNAME.get()), str(MIDDLENAME.get()), str(LASTNAME.get())))
        new_contact_id = cursor.lastrowid

        cursor.execute("INSERT INTO `address` (contact_id, address_type, address, city, state, zip) "
                        "VALUES(?, ?, ?, ?, ?, ?)",
                        (new_contact_id, str(ADDRESSTYPE.get()), str(STREET.get()), str(CITY.get()),
                        str(STATE.get()), str(ZIP.get())))
        cursor.execute("INSERT INTO `phone` (contact_id, phone_type, area_code, number) "
                        "VALUES(?, ?, ?, ?)",
                        (new_contact_id, str(PHONETYPE.get()), str(PHONEAREACD.get()), str(PHONENUMBER.get())))
        cursor.execute("INSERT INTO `date` (contact_id, date_type, date) "
                        "VALUES(?, ?, ?)",
                        (new_contact_id, str(DATETYPE.get()), str(DATE.get())))
        conn.commit()
        if 'NewWindow' in globals():
            NewWindow.destroy()
        cursor.execute("SELECT * FROM `contact` ORDER BY `lname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        FIRSTNAME.set("")
        MIDDLENAME.set("")
        LASTNAME.set("")
        ADDRESSTYPE.set("")
        STREET.set("")
        CITY.set("")
        STATE.set("")
        ZIP.set("")
        PHONETYPE.set("")
        PHONEAREACD.set("")
        PHONENUMBER.set("")
        DATETYPE.set("")
        DATE.set("")
        if flag == 'addMore':
            OnSelected(new_contact_id)


def Update_cnt():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        return
    else:
        tree.delete(*tree.get_children())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE `contact` SET `fname` = ?, `mname` = ?, `lname` = ? WHERE `contact_id` = ?",
             (str(FIRSTNAME.get()), str(MIDDLENAME.get()), str(LASTNAME.get()), int(contact_id)))
        conn.commit()
        tree.delete(*tree.get_children())
        if 'UpdateWindow' in globals():
            UpdateWindow.destroy()
        cursor.execute("SELECT * FROM `contact` ORDER BY `lname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        FIRSTNAME.set("")
        MIDDLENAME.set("")
        LASTNAME.set("")
        ADDRESSTYPE.set("")
        STREET.set("")
        CITY.set("")
        STATE.set("")
        ZIP.set("")
        PHONETYPE.set("")
        PHONEAREACD.set("")
        PHONENUMBER.set("")
        DATETYPE.set("")
        DATE.set("")
        SEARCHTERM.set("")

def UpdateAddrData(selectedAddr):
    print('UPDATEADDRESS', selectedAddr, str(ZIP.get()).isdigit())
    if ADDRESSTYPE.get() == "" or STREET.get() == "" or CITY.get() == "" or STATE.get() == "" or ZIP.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        return
    elif len(str(ZIP.get()).replace(" ", "")) != 5:
        result = tkMessageBox.showwarning('', 'ZIP Code is INVALID', icon="warning")
        return
    else:
        if selectedAddr:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE `address` SET `address_type` = ?, `address` = ?, `city` = ?, `state` = ?, `zip` = ? WHERE `address_id` = ?",
                (str(ADDRESSTYPE.get()), str(STREET.get()), str(CITY.get()), str(STATE.get()), str(ZIP.get()),
                 int(selectedAddr)))
            conn.commit()
            if 'UpdateAddrWindow' in globals():
                UpdateAddrWindow.destroy()
            cursor.close()
            ADDRESSTYPE.set("")
            STREET.set("")
            CITY.set("")
            STATE.set("")
            ZIP.set("")
            print("Save Address for Contact", int(contact_id))
            OnSelected(int(contact_id))
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO `address` (contact_id, address_type, address, city, state, zip) "
                            "VALUES(?, ?, ?, ?, ?, ?)",
                            (int(contact_id), str(ADDRESSTYPE.get()), str(STREET.get()), str(CITY.get()),
                            str(STATE.get()), str(ZIP.get())))
            conn.commit()
            if 'AddAddrWindow' in globals():
                AddAddrWindow.destroy()
            cursor.close()
            ADDRESSTYPE.set("")
            STREET.set("")
            CITY.set("")
            STATE.set("")
            ZIP.set("")
            print("Save Address for Contact", int(contact_id))
            OnSelected(int(contact_id))


def UpdatePhnData(selectedPhn):
    if PHONETYPE.get() == "" or PHONEAREACD.get() == "" or PHONENUMBER.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        return
    elif len(str(PHONEAREACD.get()).replace(" ", "")) != 3:
        result = tkMessageBox.showwarning('', 'Area Code is INVALID', icon="warning")
        return
    elif len(str(PHONENUMBER.get()).replace(" ", "")) != 7:
        result = tkMessageBox.showwarning('', 'Phone Number is INVALID', icon="warning")
        return
    else:
        if selectedPhn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE `phone` SET `phone_type` = ?, `area_code` = ?, `number` = ? WHERE `phone_id` = ?",
                (str(PHONETYPE.get()), str(PHONEAREACD.get()), str(PHONENUMBER.get()),
                 int(selectedPhn)))
            conn.commit()
            if 'UpdatePhnWindow' in globals():
                UpdatePhnWindow.destroy()
            cursor.close()
            PHONETYPE.set("")
            PHONEAREACD.set("")
            PHONENUMBER.set("")
            OnSelected(int(contact_id))
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO `phone` (contact_id, phone_type, area_code, number) "
                            "VALUES(?, ?, ?, ?)",
                            (int(contact_id), str(PHONETYPE.get()), str(PHONEAREACD.get()), str(PHONENUMBER.get())))
            conn.commit()
            if 'AddPhnWindow' in globals():
                AddPhnWindow.destroy()
            cursor.close()
            PHONETYPE.set("")
            PHONEAREACD.set("")
            PHONENUMBER.set("")
            print("Save Phone Number for Contact", int(contact_id))
            OnSelected(int(contact_id))


def UpdateDateData(selectedDate):
    if DATETYPE.get() == "" or DATE.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        return
    try:
        date_format = '%m/%d/%Y'
        date_obj = datetime.strptime(DATE.get(), date_format)
    except ValueError:
        result = tkMessageBox.showwarning('', 'Date Must be MM/DD/YYYY', icon="warning")
        return
    if selectedDate:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE `date` SET `date_type` = ?, `date` = ? WHERE `date_id` = ?",
            (str(DATETYPE.get()), str(DATE.get()),
             int(selectedDate)))
        conn.commit()
        if 'UpdateDateWindow' in globals():
            UpdateDateWindow.destroy()
        cursor.close()
        DATETYPE.set("")
        DATE.set("")
        OnSelected(int(contact_id))
    else:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `date` (contact_id, date_type, date) "
                        "VALUES(?, ?, ?)",
                        (int(contact_id), str(DATETYPE.get()), str(DATE.get())))
        conn.commit()
        if 'AddDateWindow' in globals():
            AddDateWindow.destroy()
        cursor.close()
        DATETYPE.set("")
        DATE.set("")
        print("Save Date", int(contact_id))
        OnSelected(int(contact_id))


def AddAddr():
    print('Add Address')
    global address_id, AddAddrWindow
    ADDRESSTYPE.set(ADDRESS_TYPES[0])
    STREET.set("")
    CITY.set("")
    STATE.set("")
    ZIP.set("")
    if 'UpdateAddrWindow' in globals():
        UpdateAddrWindow.destroy()
    AddAddrWindow = Toplevel(root)
    AddAddrWindow.title("Add Address")
    width = 400
    height = 250
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    AddAddrWindow.resizable(0, 0)
    AddAddrWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()
    FormTitle = Frame(AddAddrWindow)
    FormTitle.pack(side=TOP)
    AddressForm = Frame(AddAddrWindow, width=300)
    AddressForm.pack(side=TOP)

    lbl_AddressType = Label(AddressForm, text="AddressType", font=('arial', 14), bd=5)
    lbl_AddressType.grid(row=3, sticky=W)
    lbl_Street = Label(AddressForm, text="Street", font=('arial', 14), bd=5)
    lbl_Street.grid(row=4, sticky=W)
    lbl_City = Label(AddressForm, text="City", font=('arial', 14), bd=5)
    lbl_City.grid(row=5, sticky=W)
    lbl_State = Label(AddressForm, text="State", font=('arial', 14), bd=5)
    lbl_State.grid(row=6, sticky=W)
    lbl_Zip = Label(AddressForm, text="Zip", font=('arial', 14), bd=5)
    lbl_Zip.grid(row=7, sticky=W)

    addresstype = OptionMenu(AddressForm, ADDRESSTYPE, *ADDRESS_TYPES)
    addresstype.grid(row=3, column=1)
    street = Entry(AddressForm, textvariable=STREET, font=('arial', 14))
    street.grid(row=4, column=1)
    city = Entry(AddressForm, textvariable=CITY, font=('arial', 14))
    city.grid(row=5, column=1)
    state = Entry(AddressForm, textvariable=STATE, font=('arial', 14))
    state.grid(row=6, column=1)
    zip = Entry(AddressForm, textvariable=ZIP, font=('arial', 14))
    zip.grid(row=7, column=1)

    btn_addAddr = Button(AddressForm, text="Save Address", width=50, command=lambda: UpdateAddrData(''))
    btn_addAddr.grid(row=13, columnspan=2, pady=10)


def AddPhone():
    global phone_id, AddPhnWindow
    PHONETYPE.set(PHONENUMBER_TYPES[0])
    PHONEAREACD.set("")
    PHONENUMBER.set("")
    if 'UpdatePhnWindow' in globals():
        UpdatePhnWindow.destroy()
    AddPhnWindow = Toplevel(root)
    AddPhnWindow.title("Add Phone")
    width = 400
    height = 250
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    AddPhnWindow.resizable(0, 0)
    AddPhnWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()
    FormTitle = Frame(AddPhnWindow)
    FormTitle.pack(side=TOP)
    PhoneForm = Frame(AddPhnWindow, width=300)
    PhoneForm.pack(side=TOP)

    lbl_PhoneType = Label(PhoneForm, text="PhoneType", font=('arial', 14), bd=5)
    lbl_PhoneType.grid(row=3, sticky=W)
    lbl_Areacode = Label(PhoneForm, text="AreaCode", font=('arial', 14), bd=5)
    lbl_Areacode.grid(row=4, sticky=W)
    lbl_Phonenumber = Label(PhoneForm, text="PhoneNumber", font=('arial', 14), bd=5)
    lbl_Phonenumber.grid(row=5, sticky=W)

    Phonetype = OptionMenu(PhoneForm, PHONETYPE, *PHONENUMBER_TYPES)
    Phonetype.grid(row=3, column=1)
    Areacode = Entry(PhoneForm, textvariable=PHONEAREACD, font=('arial', 14))
    Areacode.grid(row=4, column=1)
    Phonenumber = Entry(PhoneForm, textvariable=PHONENUMBER, font=('arial', 14))
    Phonenumber.grid(row=5, column=1)

    btn_addPhn = Button(PhoneForm, text="Save Phone Number", width=50, command=lambda: UpdatePhnData(''))
    btn_addPhn.grid(row=13, columnspan=2, pady=10)


def AddDate():
    global date_id, AddDateWindow
    DATETYPE.set(DATE_TYPES[0])
    DATE.set("")
    if 'UpdateDateWindow' in globals():
        UpdateDateWindow.destroy()
    AddDateWindow = Toplevel(root)
    AddDateWindow.title("Add Date")
    width = 400
    height = 250
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    AddDateWindow.resizable(0, 0)
    AddDateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(AddDateWindow)
    FormTitle.pack(side=TOP)
    DateForm = Frame(AddDateWindow, width=300)
    DateForm.pack(side=TOP)

    lbl_DateType = Label(DateForm, text="DateType", font=('arial', 14), bd=5)
    lbl_DateType.grid(row=3, sticky=W)
    lbl_Date = Label(DateForm, text="Date", font=('arial', 14), bd=5)
    lbl_Date.grid(row=4, sticky=W)

    Datetype = OptionMenu(DateForm, DATETYPE, *DATE_TYPES)
    Datetype.grid(row=3, column=1)
    Date = Entry(DateForm, textvariable=DATE, font=('arial', 14))
    Date.grid(row=4, column=1)

    btn_addDate = Button(DateForm, text="Save Date", width=50, command=lambda: UpdateDateData(''))
    btn_addDate.grid(row=13, columnspan=2, pady=10)

def OnSelected(contact):
    global contact_id, UpdateWindow
    # close other windows
    if 'NewWindow' in globals():
        NewWindow.destroy()
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    curItem = tree.focus()
    if curItem:
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        contact_id = selecteditem[0]
    else:
        contact_id = contact
    FIRSTNAME.set("")
    MIDDLENAME.set("")
    LASTNAME.set("")
    ADDRESSTYPE.set(ADDRESS_TYPES[0])
    STREET.set("")
    CITY.set("")
    STATE.set("")
    ZIP.set("")
    PHONETYPE.set(PHONENUMBER_TYPES[0])
    PHONEAREACD.set("")
    PHONENUMBER.set("")
    DATETYPE.set(DATE_TYPES[0])
    DATE.set("")
    UpdateWindow = Toplevel(root)
    UpdateWindow.title("Update")
    width = 500
    height = 680
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 451) - (width / 2)
    y = ((sh / 2) + 50) - ((height / 2) + 100)
    UpdateWindow.resizable(1, 1)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    FormTitle = Frame(UpdateWindow)
    FormTitle.grid(row=0)
    ContactForm = Frame(UpdateWindow)
    ContactForm.grid(row=1)
    AddressForm = Frame(UpdateWindow)
    AddressForm.grid(row=2)
    PhoneForm = Frame(UpdateWindow)
    PhoneForm.grid(row=3)
    DateForm = Frame(UpdateWindow)
    DateForm.grid(row=4)

    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_middlename = Label(ContactForm, text="Middlename", font=('arial', 14), bd=5)
    lbl_middlename.grid(row=1, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=2, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    middlename = Entry(ContactForm, textvariable=MIDDLENAME, font=('arial', 14))
    middlename.grid(row=1, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=2, column=1)

    scrollbarx = Scrollbar(AddressForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(AddressForm, orient=VERTICAL)
    Addrtree = ttk.Treeview(AddressForm, columns=("AddressID", "AddressType", "Street", "City", "State", "Zip"),
                           height=4, yscrollcommand=scrollbary.set,
                           xscrollcommand=scrollbarx.set)
    scrollbary.config(command=Addrtree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=Addrtree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    Addrtree.heading('AddressID', text="AddressID", anchor=W)
    Addrtree.heading('AddressType', text="AddressType", anchor=W)
    Addrtree.heading('Street', text="Street", anchor=W)
    Addrtree.heading('City', text="City", anchor=W)
    Addrtree.heading('State', text="State", anchor=W)
    Addrtree.heading('Zip', text="Zip", anchor=W)
    Addrtree.column('#0', stretch=NO, minwidth=0, width=0)
    Addrtree.column('#1', stretch=NO, minwidth=0, width=0)
    Addrtree.column('#2', stretch=NO, minwidth=0, width=75)
    Addrtree.column('#3', stretch=NO, minwidth=125, width=100)
    Addrtree.column('#4', stretch=NO, minwidth=0, width=50)
    Addrtree.column('#5', stretch=NO, minwidth=0, width=50)
    Addrtree.pack()
    Addrtree.bind('<Double-Button-1>', lambda e: OnAddrSelected((Addrtree.item(Addrtree.focus()))['values'][0]))

    Datescrollbarx = Scrollbar(DateForm, orient=HORIZONTAL)
    Datescrollbary = Scrollbar(DateForm, orient=VERTICAL)
    Datetree = ttk.Treeview(DateForm, columns=("DateID", "DateType", "Date"),
                            height=4, yscrollcommand=Datescrollbary.set,
                            xscrollcommand=Datescrollbarx.set)
    Datescrollbary.config(command=Datetree.yview)
    Datescrollbary.pack(side=RIGHT, fill=Y)
    Datescrollbarx.config(command=Datetree.xview)
    Datescrollbarx.pack(side=BOTTOM, fill=X)
    Datetree.heading('DateID', text="DateID", anchor=W)
    Datetree.heading('DateType', text="DateType", anchor=W)
    Datetree.heading('Date', text="Date", anchor=W)

    Datetree.column('#0', stretch=NO, minwidth=0, width=0)
    Datetree.column('#1', stretch=NO, minwidth=0, width=0)
    Datetree.column('#2', stretch=NO, minwidth=0, width=75)
    Datetree.pack()
    Datetree.bind('<Double-Button-1>', lambda e: OnDateSelected((Datetree.item(Datetree.focus()))['values'][0]))

    Phnscrollbarx = Scrollbar(PhoneForm, orient=HORIZONTAL)
    Phnscrollbary = Scrollbar(PhoneForm, orient=VERTICAL)
    Phntree = ttk.Treeview(PhoneForm, columns=("PhoneID", "PhoneType", "Area Code", "Number"),
                           height=4, yscrollcommand=Phnscrollbary.set,
                           xscrollcommand=Phnscrollbarx.set)
    Phnscrollbary.config(command=Phntree.yview)
    Phnscrollbary.pack(side=RIGHT, fill=Y)
    Phnscrollbarx.config(command=Phntree.xview)
    Phnscrollbarx.pack(side=BOTTOM, fill=X)
    Phntree.heading('PhoneID', text="PhoneID", anchor=W)
    Phntree.heading('PhoneType', text="PhoneType", anchor=W)
    Phntree.heading('Area Code', text="Area Code", anchor=W)
    Phntree.heading('Number', text="Number", anchor=W)
    Phntree.column('#0', stretch=NO, minwidth=0, width=0)
    Phntree.column('#1', stretch=NO, minwidth=0, width=0)
    Phntree.column('#2', stretch=NO, minwidth=0, width=75)
    Phntree.column('#3', stretch=NO, minwidth=0, width=125)
    Phntree.pack()
    Phntree.bind('<Double-Button-1>', lambda e: OnPhnSelected((Phntree.item(Phntree.focus()))['values'][0]))

    btn_updatecon = Button(ContactForm, text="Update name", width=50, command=Update_cnt)
    btn_updatecon.grid(row=13, columnspan=2, pady=10)
    btn_AddPhn = Button(ContactForm, text="Add Phone", width=50, command=AddPhone)
    btn_AddPhn.grid(row=14, columnspan=2, pady=10)
    btn_AddAddr = Button(ContactForm, text="Add Address", width=50, command=AddAddr)
    btn_AddAddr.grid(row=15, columnspan=2, pady=10)
    btn_AddDate = Button(ContactForm, text="Add Dates", width=50, command=AddDate)
    btn_AddDate.grid(row=16, columnspan=2, pady=10)
    cursor = conn.cursor()

    cursor.execute("SELECT a.contact_id, a.Fname,a.Mname,a.Lname FROM contact a "
                   "WHERE a.Contact_id = ?", (int(contact_id),))
    contactData = cursor.fetchone()
    print("CD ", contactData, contact_id)
    FIRSTNAME.set(contactData[1])
    MIDDLENAME.set(contactData[2])
    LASTNAME.set(contactData[3])
    cursor.execute("SELECT * FROM address WHERE Contact_id = ? ", (int(contact_id),))
    AddrData = cursor.fetchall()
    cursor.execute("SELECT * FROM phone WHERE Contact_id = ? ", (int(contact_id),))
    PhnData = cursor.fetchall()
    cursor.execute("SELECT * FROM date WHERE Contact_id = ? ", (int(contact_id),))
    DateData = cursor.fetchall()
    for data in AddrData:
        Addrtree.insert('', 'end', values=(data))
    for data in PhnData:
        Phntree.insert('', 'end', values=(data))
    for data in DateData:
        Datetree.insert('', 'end', values=(data))
    cursor.close()


def DeleteData():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `contact` WHERE `contact_id` = %d" % selecteditem[0])
            cursor.execute("DELETE FROM `address` WHERE `contact_id` = %d" % selecteditem[0])
            cursor.execute("DELETE FROM `phone` WHERE `contact_id` = %d" % selecteditem[0])
            cursor.execute("DELETE FROM `date` WHERE `contact_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()

def AddMoreFields(type):
    if type == 'Address':
        print("Add more Addresses")
        AddressForm = Frame(NewWindow)
        AddressForm.pack(side=TOP)
        addresstype1 = OptionMenu(AddressForm, ADDRESSTYPE, *ADDRESS_TYPES)
        addresstype1.grid(row=8, column=1)
        street1 = Entry(AddressForm, textvariable=STREET, font=('arial', 14))
        street1.grid(row=9, column=1)
        city1 = Entry(AddressForm, textvariable=CITY, font=('arial', 14))
        city1.grid(row=10, column=1)
        state1 = Entry(AddressForm, textvariable=STATE, font=('arial', 14))
        state1.grid(row=11, column=1)
        zip1 = Entry(AddressForm, textvariable=ZIP, font=('arial', 14))
        zip1.grid(row=12, column=1)

        lbl_AddressType1 = Label(AddressForm, text="AddressType", font=('arial', 14), bd=5)
        lbl_AddressType1.grid(row=8, sticky=W)
        lbl_Street1 = Label(AddressForm, text="Street", font=('arial', 14), bd=5)
        lbl_Street1.grid(row=9, sticky=W)
        lbl_City1 = Label(AddressForm, text="City", font=('arial', 14), bd=5)
        lbl_City1.grid(row=10, sticky=W)
        lbl_State1 = Label(AddressForm, text="State", font=('arial', 14), bd=5)
        lbl_State1.grid(row=11, sticky=W)
        lbl_Zip1 = Label(AddressForm, text="Zip", font=('arial', 14), bd=5)
        lbl_Zip1.grid(row=12, sticky=W)

    elif type == 'phones':
        print("Add more phones")
    elif type == 'date':
        print("Add more dates")


def OnAddrSelected(selectedAddr):
    print(selectedAddr)
    global address_id, UpdateAddrWindow
    address_id = selectedAddr
    if 'UpdateAddrWindow' in globals():
        UpdateAddrWindow.destroy()
    ADDRESSTYPE.set(ADDRESS_TYPES[0])
    STREET.set("")
    CITY.set("")
    STATE.set("")
    ZIP.set("")
    UpdateAddrWindow = Toplevel(root)
    UpdateAddrWindow.title("Update Address")
    width = 400
    height = 300
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    UpdateAddrWindow.resizable(0, 0)
    UpdateAddrWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateAddrWindow)
    FormTitle.pack(side=TOP)
    AddressForm = Frame(UpdateAddrWindow, width=300)
    AddressForm.pack(side=TOP)

    lbl_AddressType = Label(AddressForm, text="AddressType", font=('arial', 14), bd=5)
    lbl_AddressType.grid(row=3, sticky=W)
    lbl_Street = Label(AddressForm, text="Street", font=('arial', 14), bd=5)
    lbl_Street.grid(row=4, sticky=W)
    lbl_City = Label(AddressForm, text="City", font=('arial', 14), bd=5)
    lbl_City.grid(row=5, sticky=W)
    lbl_State = Label(AddressForm, text="State", font=('arial', 14), bd=5)
    lbl_State.grid(row=6, sticky=W)
    lbl_Zip = Label(AddressForm, text="Zip", font=('arial', 14), bd=5)
    lbl_Zip.grid(row=7, sticky=W)

    addresstype = OptionMenu(AddressForm, ADDRESSTYPE, *ADDRESS_TYPES)
    addresstype.grid(row=3, column=1)
    street = Entry(AddressForm, textvariable=STREET, font=('arial', 14))
    street.grid(row=4, column=1)
    city = Entry(AddressForm, textvariable=CITY, font=('arial', 14))
    city.grid(row=5, column=1)
    state = Entry(AddressForm, textvariable=STATE, font=('arial', 14))
    state.grid(row=6, column=1)
    zip = Entry(AddressForm, textvariable=ZIP, font=('arial', 14))
    zip.grid(row=7, column=1)

    btn_updatecon = Button(AddressForm, text="Update Address", width=50, command=lambda: UpdateAddrData(address_id))
    btn_updatecon.grid(row=13, columnspan=2, pady=10)
    btn_delcon = Button(AddressForm, text="Delete Address", width=50, command=lambda: DeleteAddrData(address_id))
    btn_delcon.grid(row=14, columnspan=2, pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM address b WHERE address_id = ?", (int(address_id),))
    data = cursor.fetchone()
    cursor.close()
    print(data)
    ADDRESSTYPE.set(data[1])
    STREET.set(data[2])
    CITY.set(data[3])
    STATE.set(data[4])
    ZIP.set(data[5])

    def DeleteAddrData(address_id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM `address` WHERE `address_id` = %d" % address_id)
        conn.commit()
        cursor.close()
        OnSelected(int(contact_id))
        if 'UpdateAddrWindow' in globals():
            UpdateAddrWindow.destroy()


def OnPhnSelected(selectedPhn):
    global phone_id, UpdatePhnWindow
    phone_id = selectedPhn
    if 'UpdatePhnWindow' in globals():
        UpdatePhnWindow.destroy()
    PHONETYPE.set(PHONENUMBER_TYPES[0])
    PHONEAREACD.set("")
    PHONENUMBER.set("")
    UpdatePhnWindow = Toplevel(root)
    UpdatePhnWindow.title("Update PhoneNumber")
    width = 400
    height = 200
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    UpdatePhnWindow.resizable(0, 0)
    UpdatePhnWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdatePhnWindow)
    FormTitle.pack(side=TOP)
    PhoneForm = Frame(UpdatePhnWindow, width=300)
    PhoneForm.pack(side=TOP)

    lbl_PhoneType = Label(PhoneForm, text="Phone Type", font=('arial', 14), bd=5)
    lbl_PhoneType.grid(row=3, sticky=W)
    lbl_Areacode = Label(PhoneForm, text="Areacode", font=('arial', 14), bd=5)
    lbl_Areacode.grid(row=4, sticky=W)
    lbl_Number = Label(PhoneForm, text="Number", font=('arial', 14), bd=5)
    lbl_Number.grid(row=5, sticky=W)

    phonetype = OptionMenu(PhoneForm, PHONETYPE, *PHONENUMBER_TYPES)
    phonetype.grid(row=3, column=1)
    Areacode = Entry(PhoneForm, textvariable=PHONEAREACD, font=('arial', 14))
    Areacode.grid(row=4, column=1)
    Number = Entry(PhoneForm, textvariable=PHONENUMBER, font=('arial', 14))
    Number.grid(row=5, column=1)

    btn_updatecon = Button(PhoneForm, text="Update Number", width=50, command=lambda: UpdatePhnData(phone_id))
    btn_updatecon.grid(row=13, columnspan=2, pady=10)
    btn_delcon = Button(PhoneForm, text="Delete Number", width=50, command=lambda: DeletePhnData(phone_id))
    btn_delcon.grid(row=14, columnspan=2, pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phone b WHERE phone_id = ?", (int(phone_id),))
    data = cursor.fetchone()
    cursor.close()
    PHONETYPE.set(data[1])
    PHONEAREACD.set(data[2])
    PHONENUMBER.set(data[3])

def DeletePhnData(address_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `phone` WHERE `phone_id` = %d" % phone_id)
    conn.commit()
    cursor.close()
    OnSelected(int(contact_id))
    if 'UpdatePhnWindow' in globals():
        UpdatePhnWindow.destroy()

def OnDateSelected(selectedDate):
    global date_id, UpdateDateWindow
    date_id = selectedDate
    if 'UpdateDateWindow' in globals():
        UpdateDateWindow.destroy()
    DATETYPE.set(DATE_TYPES[0])
    DATE.set("")
    UpdateDateWindow = Toplevel(root)
    UpdateDateWindow.title("Update Date")
    width = 400
    height = 200
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) + 400) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) + 100)
    UpdateDateWindow.resizable(0, 0)
    UpdateDateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateDateWindow)
    FormTitle.pack(side=TOP)
    DateForm = Frame(UpdateDateWindow, width=300)
    DateForm.pack(side=TOP)

    lbl_DateType = Label(DateForm, text="Date Type", font=('arial', 14), bd=5)
    lbl_DateType.grid(row=3, sticky=W)
    lbl_Date = Label(DateForm, text="Date(mm/dd/yyyy)", font=('arial', 14), bd=5)
    lbl_Date.grid(row=4, sticky=W)

    Datetype = OptionMenu(DateForm, DATETYPE, *DATE_TYPES)
    Datetype.grid(row=3, column=1)
    Date = Entry(DateForm, textvariable=DATE, font=('arial', 14))
    Date.grid(row=4, column=1)

    btn_updatecon = Button(DateForm, text="Update Date", width=50, command=lambda: UpdateDateData(date_id))
    btn_updatecon.grid(row=13, columnspan=2, pady=10)
    btn_delcon = Button(DateForm, text="Delete Date", width=50, command=lambda: DeleteDateData(date_id))
    btn_delcon.grid(row=14, columnspan=2, pady=10)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM date b WHERE date_id = ?", (int(date_id),))
    data = cursor.fetchone()
    cursor.close()
    DATETYPE.set(data[1])
    DATE.set(data[2])

def DeleteDateData(address_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `date` WHERE `date_id` = %d" % date_id)
    conn.commit()
    cursor.close()
    OnSelected(int(contact_id))
    if 'UpdateDateWindow' in globals():
        UpdateDateWindow.destroy()


def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    MIDDLENAME.set("")
    LASTNAME.set("")
    ADDRESSTYPE.set(ADDRESS_TYPES[0])
    STREET.set("")
    CITY.set("")
    STATE.set("")
    ZIP.set("")
    PHONETYPE.set(PHONENUMBER_TYPES[0])
    PHONEAREACD.set("")
    PHONENUMBER.set("")
    DATETYPE.set(DATE_TYPES[0])
    DATE.set("")

    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 450
    height = 550
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = ((sw / 2) - 425) - (width / 2)
    y = ((sh / 2) + 20) - ((height / 2) +100)
    NewWindow.resizable(0, 1)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)

    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#66ff66", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_middlename = Label(ContactForm, text="Middlename", font=('arial', 14), bd=5)
    lbl_middlename.grid(row=1, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=2, sticky=W)
    lbl_AddressType = Label(ContactForm, text="AddressType", font=('arial', 14), bd=5)
    lbl_AddressType.grid(row=3, sticky=W)
    lbl_Street = Label(ContactForm, text="Street", font=('arial', 14), bd=5)
    lbl_Street.grid(row=4, sticky=W)
    lbl_City = Label(ContactForm, text="City", font=('arial', 14), bd=5)
    lbl_City.grid(row=5, sticky=W)
    lbl_State = Label(ContactForm, text="State", font=('arial', 14), bd=5)
    lbl_State.grid(row=6, sticky=W)
    lbl_Zip = Label(ContactForm, text="Zip", font=('arial', 14), bd=5)
    lbl_Zip.grid(row=7, sticky=W)
    lbl_PhoneType = Label(ContactForm, text="PhoneType", font=('arial', 14), bd=5)
    lbl_PhoneType.grid(row=17, sticky=W)
    lbl_PhoneAreaCd = Label(ContactForm, text="PhoneAreaCode", font=('arial', 14), bd=5)
    lbl_PhoneAreaCd.grid(row=18, sticky=W)
    lbl_PhoneNumber = Label(ContactForm, text="PhoneNumber", font=('arial', 14), bd=5)
    lbl_PhoneNumber.grid(row=19, sticky=W)
    lbl_DateType = Label(ContactForm, text="DateType", font=('arial', 14), bd=5)
    lbl_DateType.grid(row=20, sticky=W)
    lbl_Date = Label(ContactForm, text="Date(mm/dd/yyyy)", font=('arial', 14), bd=5)
    lbl_Date.grid(row=21, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    middlename = Entry(ContactForm, textvariable=MIDDLENAME, font=('arial', 14))
    middlename.grid(row=1, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=2, column=1)
    addresstype = OptionMenu(ContactForm, ADDRESSTYPE, *ADDRESS_TYPES)
    addresstype.grid(row=3, column=1)
    street = Entry(ContactForm, textvariable=STREET, font=('arial', 14))
    street.grid(row=4, column=1)
    city = Entry(ContactForm, textvariable=CITY, font=('arial', 14))
    city.grid(row=5, column=1)
    state = Entry(ContactForm, textvariable=STATE, font=('arial', 14))
    state.grid(row=6, column=1)
    zip = Entry(ContactForm, textvariable=ZIP, font=('arial', 14))
    zip.grid(row=7, column=1)
    phoneType = OptionMenu(ContactForm, PHONETYPE, *PHONENUMBER_TYPES)
    phoneType.grid(row=17, column=1)
    phoneareaCd = Entry(ContactForm, textvariable=PHONEAREACD, font=('arial', 14))
    phoneareaCd.grid(row=18, column=1)
    phonenumber = Entry(ContactForm, textvariable=PHONENUMBER, font=('arial', 14))
    phonenumber.grid(row=19, column=1)
    datetype = OptionMenu(ContactForm, DATETYPE, *DATE_TYPES)
    datetype.grid(row=20, column=1)
    date = Entry(ContactForm, textvariable=DATE, font=('arial', 14))
    date.grid(row=21, column=1)

    btn_addcon = Button(ContactForm, text="Save", width=25, command=lambda: Add_cnt(''))
    btn_addcon.grid(row=22, column=1, pady=10)
    btn_addMorecon = Button(ContactForm, text="Save and add more information", width=25, command=lambda: Add_cnt('addMore'))
    btn_addMorecon.grid(row=22, column=0, pady=10)

Top = Frame(root, width=300, bd=1, relief=SOLID)
Top.pack(side=TOP)
Options = Frame(root, width=300)
Options.columnconfigure(0, weight=1)
Options.columnconfigure(1, weight=1)
Options.pack(side=TOP, expand=True)
SearchForm = Frame(root, width=300)
SearchForm.columnconfigure(0, weight=3)
SearchForm.columnconfigure(1, weight=1)
SearchForm.pack(side=TOP, expand=True)
TableMargin = Frame(root, width=300)
TableMargin.pack(side=TOP)

searchTerm = Entry(SearchForm, textvariable=SEARCHTERM, font=('arial', 14))
searchTerm.grid(row=0, column=0, sticky=W+E, padx=5, pady=2)

btn_search = Button(SearchForm, text="Search", bg="#c4cfcc", command=SearchDatabase)
btn_search.grid(row=0, column=1, sticky=E+W, columnspan=1,padx=0, pady=2)
btn_add = Button(SearchForm, text="Add New", bg="#c4cfcc", command=AddNewWindow)
btn_add.grid(row=0, column=2, sticky=W+E, padx=15, pady=2)
btn_delete = Button(SearchForm, text="Delete", bg="#c4cfcc", command=DeleteData)
btn_delete.grid(row=1, column=2, sticky=E+W,padx=15, pady=2)
lbl_search = Label(SearchForm, text="(double click to update a contact)             ", font=('arial', 8, 'italic', 'bold'), bd=5)
lbl_search.grid(row=1, column=0, sticky=E+W,padx=15, pady=2)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("ContactID", "Firstname", "Middlename", "Lastname"),
                    height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ContactID', text="ContactID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Middlename', text="Middlename", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=125)
tree.column('#3', stretch=NO, minwidth=0, width=125)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()
    conn.close()

