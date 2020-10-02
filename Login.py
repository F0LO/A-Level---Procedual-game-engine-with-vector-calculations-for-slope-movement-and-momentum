from tkinter import *
 
# creates the main window object, defines its name, and default size
login_window = Tk()
login_window.title('Login Menu')
login_window.geometry('225x150')
 
def clear_widget(event):
    if username_box == login_window.focus_get() and username_box.get() == 'Enter Username':
        username_box.delete(0, END)
    elif password_box == password_box.focus_get() and password_box.get() == '              ':
        password_box.delete(0, END)
 
def repopulate_defaults(event):
    if username_box != login_window.focus_get() and username_box.get() == '':
        username_box.insert(0, 'Enter Username')
    elif password_box != login_window.focus_get() and password_box.get() == '':
        password_box.insert(0, '              ')
 
def login(*event):
    print('Username: ' + username_box.get())
    print('Password: ' + password_box.get())
    if username_box.get() == "Enter Username":
        print("no username detected")
 
 
 
 
# adds username entry widget and defines its properties
username_box = Entry(login_window)
username_box.insert(0, 'Enter Username')
username_box.bind("<FocusIn>", clear_widget)
username_box.bind('<FocusOut>', repopulate_defaults)
username_box.grid(row=1, column=5, sticky='NS')
 
 
# adds password entry widget and defines its properties
password_box = Entry(login_window, show='*')
password_box.insert(0, '              ')
password_box.bind("<FocusIn>", clear_widget)
password_box.bind('<FocusOut>', repopulate_defaults)
password_box.bind('<Return>', login)
password_box.grid(row=2, column=5, sticky='NS')
 
 
# adds login button and defines its properties
login_btn = Button(login_window, text='Login', command=login)
login_btn.bind('<Return>', login)
login_btn.grid(row=5, column=5, sticky='NESW')
 
 
login_window.mainloop()
