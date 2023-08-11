from tkinter import*
from tkinter import messagebox as mb
import sqlite3
from PIL import Image, ImageTk, ImageFilter


com=Tk()
com.title('Parking Management System')
com.geometry("800x600")
com.iconbitmap("logo.png")
image=Image.open("parking.jpg")
background_image=ImageTk.PhotoImage(image)
background_label=Label (com,image=background_image)
background_label.pack(expand=True)
name=Label(background_label,text="Username",fg="black")
name.place(x=90,y=90)
e1 = Entry(background_label)
e1.place(x=190, y=90)
password_label = Label(background_label, text="Password",fg="black")
password_label.place(x=90, y=120)
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
     import backend
databaseInitialize() 
e2 = Entry(background_label, show="*")
e2.place(x=190, y=120)
def login1():
  
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
  comn=Tk()
  
  
  comn.title('Parking Management System')
  
  
  comn.geometry("400x400")
  comn.iconbitmap("logo.png")
    
  def change_color():
   canvas.configure(bg='blue')

# Create a canvas widget
  canvas= Canvas(comn, bg='skyblue')
  canvas.pack()
 
  conn=sqlite3.connect('project.db')

  Label(comn,text="Parking Registration System",font="1").place(x=1,y=0)
  Email = Label(comn,text="Email id")
  name=Label(comn,text="Username")
  password=Label(comn,text="password")
  confirm=Label(comn,text="confirm password")
 
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
      query_label=Label(comn,text=print_record)
      query_label.grid(row=12,column=0,columnspan=2)
  
  def signupuser():
     try:
        if(passwordvalue.get()!=confirmvalue.get()):
           raise BaseException("Password and confirm password do not match")
        addUserToTable(namevalue.get(),Emailvalue.get(),passwordvalue.get())
        mb.askokcancel(title="Success",message="User has been signed up succesfully")
        comn.destroy()
     except BaseException as e:
        mb.showerror(message=str(e),title="Error")
  sign_up=Button(comn,text="sign up",padx=10,pady=10,command=signupuser).place(x=150,y=280)
  

  
 
#close field
  Email.place(x=40,y=50)
  name.place(x=40,y=90)
  password.place(x=40,y=130)
  confirm.place(x=15,y=170)
  
#variable for storing data
  Emailvalue= StringVar(comn)
  namevalue= StringVar(comn)
  passwordvalue= StringVar(comn)
  confirmvalue= StringVar(comn)


#creating entry field
  Emailentry = Entry(comn,textvariable=Emailvalue)
  nameentry = Entry(comn,textvariable=namevalue)
  passwordentry = Entry(comn,textvariable=passwordvalue)
  confirmentry = Entry(comn,textvariable=confirmvalue)
#packing entry fields
  Emailentry.place(x=120,y=50)
  nameentry.place(x=120,y=90)
  passwordentry.place(x=120,y=130)
  confirmentry.place(x=120,y=175)

  comn.mainloop()


#login button

login=Button(background_label,text="LOGIN",padx=2,pady=2,command= login1).place(x=100,y=180)

sign_up=Button(background_label,text="sign up",padx=2,pady=2,command=sign_up).place(x=170,y=180)

com.mainloop()
