from tkinter import*
from tkinter import messagebox as mb
import sqlite3

com=Tk()
com.title('Parking Management System')
com.geometry("600x600")
name=Label(com,text="Username",fg="black")
name.place(x=30,y=50)
e1 = Entry(com)
e1.place(x=150, y=50)
password_label = Label(com, text="Password",fg="black")
password_label.place(x=30, y=90)
def addUserToTable(username,emailId,password):
    conn=sqlite3.connect('project.db')
    cursor=conn.cursor()
    cursor.execute("INSERT into user (email_id,username,password) values (?,?,?)",[emailId,username,password])
    conn.commit()
    cursor.close()

def databaseInitialize():
  conn=sqlite3.connect('project.db')
  cursor=conn.cursor()
  cursor.executescript('''Create table if not exists user (
          email_id text NOT NULL,
          username text NOT NULL,
          password text NOT NULL )
          ''')
  conn.commit()
  cursor.close()

def loginUser(username, password):
  conn=sqlite3.connect('project.db')
  cursor=conn.cursor()
  cursor.execute("SELECT * from user WHERE username = ? and password = ?",[username,password])
  data = cursor.fetchone()
  if(data == None):
     mb.showerror(message="Not found")
  else:
     mb.showinfo(message="LOGIN DONE")   
     com.destroy()

databaseInitialize() 
e2 = Entry(com, show="*")
e2.place(x=150, y=90)
def login1():
  com=Tk()
  conn=sqlite3.connect('project.db')
    
  username = e1.get()
  password = e2.get()
  loginUser(username,password)
  return
  if username == "" and password == "":
        print("Login successful")
        com.destroy()
       
  else:
 
        print("Invalid username or password")
def login():
  mb.askokcancel(title="sucess",Message="user have login sucessfully")
  com.destroy()



#field name
def sign_up():
  com=Tk()
  conn=sqlite3.connect('project.db')
  c=conn.cursor()
  com.title('Parking Management System')
  com.geometry("400x400")
  Label(com,text="Parking Registration System",font="1").place(x=1,y=0)
  Email = Label(com,text="Email id")
  name=Label(com,text="Username")
  password=Label(com,text="password")
  confirm=Label(com,text="confirm password")
  def query():
    conn=sqlite3.connect('project.db')

 #create cursor
    c=conn.cursor()

 #query of the database
    c.execute("SELECT *,oid FROM addresses")
    records=c.fetchall()
  
#print records
    print_record=''

    for record in records:
#str(record[6])added for dispalying the id
      print_record+=(record[0])+''+(record[1])+''+'\t'+str(record[6])
      query_label=Label(com,text=print_record)
      query_label.grid(row=12,column=0,columnspan=2)
  
  def signupuser():
     try:
        if(passwordvalue.get()!=confirmvalue.get()):
           raise BaseException("Password and confirm password do not match")
        addUserToTable(namevalue.get(),Emailvalue.get(),passwordvalue.get())
        mb.askokcancel(title="Success",message="User has been signed up succesfully")
        com.destroy()
     except BaseException as e:
        mb.showerror(message=str(e),title="Erro")
  sign_up=Button(com,text="sign up",padx=10,pady=10,command=signupuser).place(x=150,y=280)
  

  
 
#close field
  Email.place(x=40,y=50)
  name.place(x=40,y=90)
  password.place(x=40,y=130)
  confirm.place(x=15,y=170)
  
#variable for storing data
  Emailvalue= StringVar(com)
  namevalue= StringVar(com)
  passwordvalue= StringVar(com)
  confirmvalue= StringVar(com)


#creating entry field
  Emailentry = Entry(com,textvariable=Emailvalue)
  nameentry = Entry(com,textvariable=namevalue)
  passwordentry = Entry(com,textvariable=passwordvalue)
  confirmentry = Entry(com,textvariable=confirmvalue)
#packing entry fields
  Emailentry.place(x=120,y=50)
  nameentry.place(x=120,y=90)
  passwordentry.place(x=120,y=130)
  confirmentry.place(x=120,y=175)


#login button

login=Button(text="LOGIN",padx=2,pady=2,command= login1).place(x=80,y=150)

sign_up=Button(com,text="sign up",padx=2,pady=2,command=sign_up).place(x=150,y=150)
com.mainloop()
