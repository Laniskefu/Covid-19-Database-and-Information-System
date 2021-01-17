from database import *
from windows import *


class Login:
    def __init__(self, width=500, high=300):
        self.db = Database()
        
        self.root = Tk()
        self.root.title("Welcome to Covid-19 Information System")
        
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (width, high, (screenwidth-width)/2, (screenheight-high)/2))
        
        Label(self.root, text='Username').place(relx=0.15, rely=0.3, relwidth=0.2)
        Label(self.root, text='Password').place(relx=0.15, rely=0.4, relwidth=0.2)

        username = StringVar()
        password = StringVar()

        Entry(self.root, width=30, textvariable=username).place(relx=0.35, rely=0.3, relwidth=0.4)
        Entry(self.root, width=30, textvariable=password, show='*').place(relx=0.35, rely=0.4, relwidth=0.4)

        Button(self.root, command=lambda: self.tourist_mode(), text="Tourist").place(relx=0.2, rely=0.5, relwidth=0.15)
        Button(self.root, command=lambda: self.login(username, password), text="Login").place(relx=0.4, rely=0.5, relwidth=0.15)
        Button(self.root, command=lambda: self.register(username, password), text="Register").place(relx=0.6, rely=0.5, relwidth=0.15)
        

        mainloop()

    def login(self, username, password):
        username = username.get()
        password = password.get()
        if username.strip() and password.strip():
            if self.db.prepare(f"select * from account where username='{username}' and password='{password}'"):
                showinfo("Reminder", "Login succeed")
                self.root.destroy()
                data(account=username)
            else:
                showerror("Error", "Wrong account or password, please try again")
        else:
            showerror("Error", "Invalid account or password")
        
    def register(self, username, password):
        username = username.get()
        password = password.get()
        if username.strip() and password.strip():
            if self.db.prepare(f"select * from account where username='{username}'")==0:
                self.db.prepare(f"insert into account values ('{username}', '{password}')")
                self.db.update()
                showinfo("Remainder", "Register succeed")
            else:
                showerror("Error", "This account has alrealy been registeded")
        else:
            showerror("Error", "Invalid account or password")

    def tourist_mode(self):
        self.root.destroy()
        data()
        

