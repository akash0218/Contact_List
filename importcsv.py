import sqlite3
import csv

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS `contact` (Contact_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, Fname TEXT, Mname TEXT, Lname TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `address` (address_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, address_type TEXT, address TEXT, city TEXT, state TEXT, zip INTEGER, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `phone` (phone_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, phone_type TEXT, area_code INTEGER, number INTEGER, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS `date` (date_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, date_type TEXT, date TEXT, contact_id INTEGER, FOREIGN KEY (contact_id) REFERENCES contact (contact_id) )")
cursor.close()


file = open('test.csv', 'r')
csvread = csv.reader(file)

count = 0
for row in csvread:
    if row[0] == "contact_id":
        pass
    else:
        cursor = conn.cursor()
        fname = str(row[1])
        mname = str(row[2])
        lname = str(row[3])
        cursor.execute("INSERT INTO `contact` (Fname, MName, Lname) VALUES(?, ?, ?)",
                       (fname, mname, lname))
        new_contact_id = cursor.lastrowid

        split_home_phone = str(row[4]).split("-", 2) if row[4] is not None else []
        if len(split_home_phone) == 3:
            phone_area_code = int(split_home_phone[0])
            phone_no = int(split_home_phone[1]+split_home_phone[2])
            cursor.execute("INSERT INTO `phone` (contact_id, phone_type, area_code, number) "
                           "VALUES(?, ?, ?, ?)",
                           (new_contact_id, "Home", phone_area_code, phone_no))

        split_cell_phone = str(row[5]).split("-", 2) if row[5] is not None else []
        if len(split_cell_phone) == 3:
            cell_area_code = int(split_cell_phone[0])
            cell_no = int(split_cell_phone[1]+split_cell_phone[2])
            cursor.execute("INSERT INTO `phone` (contact_id, phone_type, area_code, number) "
                           "VALUES(?, ?, ?, ?)",
                           (new_contact_id, "Cell", cell_area_code, cell_no))

        home_address = str(row[6]) if row[6] is not None else ""
        home_city = str(row[7]) if row[7] is not None else ""
        home_state = str(row[8]) if row[8] is not None else ""
        home_zip = None
        if row[9] == '':
            home_zip = ''
        else:
            home_zip = int(row[9])
        if home_city != "" and home_zip != "" and home_address != "" and home_state != "":
            cursor.execute("INSERT INTO `address` (contact_id, address_type, address, city, state, zip) "
                           "VALUES(?, ?, ?, ?, ?, ?)",
                           (new_contact_id, "Home", home_address, home_city,home_state, home_zip))

        split_work_phone = str(row[10]).split("-", 2) if row[10] is not None else []
        if len(split_work_phone) == 3:
            work_area_code = int(split_work_phone[0])
            work_no = int(split_work_phone[1]+split_work_phone[2])
            cursor.execute("INSERT INTO `phone` (contact_id, phone_type, area_code, number) "
                           "VALUES(?, ?, ?, ?)",
                           (new_contact_id, "Work", work_area_code, work_no))

        work_address = str(row[11]) if row[11] is not None else ""
        work_city = str(row[12]) if row[12] is not None else ""
        work_state = str(row[13]) if row[13] is not None else ""
        work_zip = 0
        if row[14] == '':
            work_zip =" "
        else:
            work_zip = int(row[14])

        if work_zip != "" and work_state != "" and work_address != "" and work_city != "":
            cursor.execute("INSERT INTO `address` (contact_id, address_type, address, city, state, zip) "
                           "VALUES(?, ?, ?, ?, ?, ?)",
                           (new_contact_id, "Work", work_address, work_city,work_state, work_zip))

        date_of_birth = str(row[15]) if row[15] is not None else ""
        if date_of_birth != "":
            cursor.execute("INSERT INTO `date` (contact_id, date_type, date) "
                           "VALUES(?, ?, ?)",
                           (new_contact_id, "Birthday", date_of_birth))
        conn.commit()
        cursor.close()
        count += 1
        print(count)
