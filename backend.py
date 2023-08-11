import os
import datetime
import tkinter.messagebox as mb
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from PIL import Image, ImageTk, ImageFilter




connection = sqlite3.connect('project.db')
connector = connection.cursor()

connector.execute("""
    CREATE TABLE IF NOT EXISTS VEHICLE_MANAGEMENT (
        VEHICLE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT,
        ADDRESS TEXT,
        PHONE_NO TEXT,
        VEHICLE_TYPE TEXT,
        DOE TEXT,
        VEHICLE_NAME TEXT,
        SLOT TEXT,
        NUMBER_PLATE TEXT
    )
""")



main = Tk()
main.title('Vehicle Management System')
main.geometry('1200x700')
main.resizable(1, 1)

lf_bg = 'green'
cf_bg = 'grey'
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

name_strvar = StringVar()
address_strvar = StringVar()
contact_strvar = StringVar()
Vehicle_Type_strvar = StringVar()
vehicle_name_strvar = StringVar()
slot_strvar = StringVar()
vehicleid_strvar = StringVar()

Label(main, text="VEHICLE MANAGEMENT SYSTEM", font=headlabelfont, bg='Blue').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.3)
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main, bg="Gray")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)


Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(x=70, y=1)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(x=30, y=70)
Label(left_frame, text="Address", font=labelfont, bg=lf_bg).place(x=60, y=140)
Label(left_frame, text="Vehicle Type", font=labelfont, bg=lf_bg).place(x=60, y=420)
Label(left_frame, text="Date Of Entry", font=labelfont, bg=lf_bg).place(x=40, y=280)
Label(left_frame, text="Vehicle Name", font=labelfont, bg=lf_bg).place(x=40, y=210)
Label(left_frame, text="Slot No", font=labelfont, bg=lf_bg).place(x=70, y=350)
Label(left_frame, text="Vehicle Plate", font=labelfont, bg=lf_bg).place(x=50, y=490)

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, y=35)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, y=105)
Entry(left_frame, width=19, textvariable=address_strvar, font=entryfont).place(x=20, y=175)
Entry(left_frame, width=19, textvariable=vehicle_name_strvar, font=entryfont).place(x=20, y=245)
Entry(left_frame, width=19, textvariable=slot_strvar, font=entryfont).place(x=20, y=385)
Entry(left_frame, width=19, textvariable=vehicleid_strvar, font=entryfont).place(x=20, y=525)

OptionMenu(left_frame, Vehicle_Type_strvar, *['2 WHEEL', '4 WHEEL']).place(x=20, y=455, relwidth=0.5)

doe = DateEntry(left_frame, font=("Arial", 12), width=15)
doe.place(x=20, y=315)

def reset_fields():
    global name_strvar, address_strvar, contact_strvar, Vehicle_Type_strvar, doe, vehicle_name_strvar, slot_strvar, vehicleid_strvar
    name_strvar.set('')
    address_strvar.set('')
    contact_strvar.set('')
    Vehicle_Type_strvar.set('')
    doe.set_date(datetime.datetime.now())
    vehicle_name_strvar.set('')
    slot_strvar.set('')
    vehicleid_strvar.set('')

def reset_database():
    global tree
    tree.delete(*tree.get_children())
    reset_fields()
    connector.execute('DELETE FROM VEHICLE_MANAGEMENT')
    connection.commit()
    display_records()

def display_records():
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM VEHICLE_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)

def is_numeric(s):
    return s.isdigit()

def add_record():
    global name_strvar, address_strvar, contact_strvar, Vehicle_Type_strvar, doe, vehicle_name_strvar, slot_strvar, vehicleid_strvar

    name = name_strvar.get()
    address = address_strvar.get()
    contact = contact_strvar.get()
    Vehicle_Type = Vehicle_Type_strvar.get()
    DOE_type = doe.get_date().isoformat()
    vehicle_name = vehicle_name_strvar.get()
    slot = slot_strvar.get()
    vehicleid = vehicleid_strvar.get()

    if not name or not address or not contact or not Vehicle_Type or not DOE_type or not vehicle_name or not slot or not vehicleid:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    elif not is_numeric(contact):
        mb.showerror('Wrong type', 'The contact field can only contain numbers.')
    else:
        try:
            connector.execute(
                'INSERT INTO VEHICLE_MANAGEMENT (NAME, ADDRESS, PHONE_NO, VEHICLE_TYPE, DOE, VEHICLE_NAME, SLOT, NUMBER_PLATE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (name, address, contact, Vehicle_Type, DOE_type, vehicle_name, slot, vehicleid)
            )
            connection.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            display_records()
            reset_fields()
        except Exception as e:
            print("Error:", str(e))
            mb.showerror('Error', 'An error occurred while adding the record.')

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        connector.execute('DELETE FROM VEHICLE_MANAGEMENT WHERE VEHICLE_ID=%d' % selection[0])
        connection.commit()
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
        display_records()

def view_record():
    global name_strvar, address_strvar, contact_strvar, Vehicle_Type_strvar, doe, vehicle_name_strvar, slot_strvar, vehicleid_strvar
    if not tree.selection():
        mb.showerror('Error!', 'Please select a record to view')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        vehicle_type = selection[4]

        name_strvar.set(selection[1])
        address_strvar.set(selection[2])
        contact_strvar.set(selection[3])
        Vehicle_Type_strvar.set(vehicle_type)

        date_str = selection[5]
        date = datetime.date.fromisoformat(date_str)
        doe.set_date(date)

        vehicle_name_strvar.set(selection[6])
        slot_strvar.set(selection[7])
        vehicleid_strvar.set(selection[8])


Label(center_frame, text='Option', font=headlabelfont, bg='yellow', fg='black').pack(side=TOP, fill=X)
Button(left_frame, text='Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_database, width=15).place(relx=0.1, rely=0.55)
Label(text="Per day for 2 Wheeler: 50 ", font=labelfont).place(relx=0.2, rely=0.70)
Label(text="Per day for 4 Wheeler: 100", font=labelfont).place(relx=0.2, rely=0.80)


Label(right_frame, text='Vehicle Records', font=headlabelfont, bg='red', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE, columns=("VEHICLE_ID", "NAME", "ADDRESS", "PHONE_NO", "VEHICLE_TYPE", "DOE", "VEHICLE_NAME", "SLOT", "NUMBER_PLATE"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('VEHICLE_ID', text='S.N', anchor=CENTER)
tree.heading('NAME', text='Name', anchor=CENTER)
tree.heading('ADDRESS', text='Address', anchor=CENTER)
tree.heading('PHONE_NO', text='Contact Number', anchor=CENTER)
tree.heading('VEHICLE_TYPE', text='Vehicle Type', anchor=CENTER)
tree.heading('DOE', text='Date Of Entry', anchor=CENTER)
tree.heading('VEHICLE_NAME', text='Vehicle Name', anchor=CENTER)
tree.heading('SLOT', text='Slot No', anchor=CENTER)
tree.heading('NUMBER_PLATE', text='Vehicle Plate', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('VEHICLE_ID', width=50, stretch=NO)
tree.column('NAME', width=200, stretch=NO)
tree.column('ADDRESS', width=200, stretch=NO)
tree.column('PHONE_NO', width=150, stretch=NO)
tree.column('VEHICLE_TYPE', width=100, stretch=NO)
tree.column('DOE', width=120, stretch=NO)
tree.column('VEHICLE_NAME', width=150, stretch=NO)
tree.column('SLOT', width=80, stretch=NO)
tree.column('NUMBER_PLATE', width=150, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_records()

main.update()
main.mainloop()

connector.close()
connection.close()
