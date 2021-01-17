from tkinter import *
from database import *

import datetime

def systemlog(width=1300, high=600):
    top = Toplevel()
    
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    
    top.geometry('%dx%d+%d+%d'%(width, high, (screenwidth-width)/2, (screenheight-high)/2))
    top.title('Covid-19 Information System '+ 'SystemLog')

    tree_view = ttk.Treeview(top, show='headings', column=('datetime', 'account', 'command'))
    tree_view.column('datetime', width=100, anchor="center");tree_view.heading('datetime', text='datatime')
    tree_view.column('account', width=100, anchor="center"); tree_view.heading('account', text='account')
    tree_view.column('command', width=800, anchor="center"); tree_view.heading('command', text='command')

    tree_view.place(relx=0.01, rely=0.1, relwidth=0.96, relheight=0.8)
    scrollbar = Scrollbar(top, orient='vertical', command=tree_view.yview)
    scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
    tree_view.configure(yscrollcommand=scrollbar.set)

    db = Database()
    db.prepare("select * from systemlog")
    data = db.fetchall()
    db.close
    for row in data:
        tree_view.insert("", 'end', values=row)

def account(width=1300, high=600):
    top = Toplevel()
    
    screenwidth = top.winfo_screenwidth()
    screenheight = top.winfo_screenheight()
    
    top.geometry('%dx%d+%d+%d'%(width, high, (screenwidth-width)/2, (screenheight-high)/2))
    top.title('Covid-19 Information System '+ 'Account')

    tree_view = ttk.Treeview(top, show='headings', column=('account', 'first seen', 'last seen', 'operation number'))
    tree_view.column('account', width=100, anchor="center");tree_view.heading('account', text='account')
    tree_view.column('first seen', width=100, anchor="center");tree_view.heading('first seen', text='first seen')
    tree_view.column('last seen', width=100, anchor="center");tree_view.heading('last seen', text='last seen')
    tree_view.column('operation number', width=100, anchor="center");tree_view.heading('operation number', text='operation number')

    tree_view.place(relx=0.01, rely=0.1, relwidth=0.96, relheight=0.8)
    scrollbar = Scrollbar(top, orient='vertical', command=tree_view.yview)
    scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
    tree_view.configure(yscrollcommand=scrollbar.set)

    db = Database()
    db.prepare("select * from systemlog")
    data = db.fetchall()
    db.close

    number = {}
    first = {}
    last = {}

    for row in data:
        admin = row[1]
        if admin not in number: number[admin] = 0
        number[admin] += 1
        time = row[0]
        if admin not in first: first[admin] = time
        if time<first[admin]: first[admin] = time

        if admin not in last: last[admin] = time
        if time>last[admin]: last[admin] = time

    data = []
    for admin in number:
        data.append([admin, first[admin], last[admin], number[admin]])

    for row in data:
        tree_view.insert("", 'end', values=row)

