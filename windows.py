from tkinter import *
from tkinter import ttk
from save import *
from view import *
from database import *
from plot_current import *
from plot_predict import *
import operations_data
import operations_economy

def Capital(name):
    return name[0].upper()+name[1:]

class Window:
    def __init__(self, account=None, width=1300, high=600):
        self.account = account
        
        self.root = Tk()
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (width, high, (screenwidth-width)/2, (screenheight-high)/2))
        self.root.title('Covid-19 Information System '+("(Administrator Mode)" if account else "(Tourist Mode)"))

        self.columns = self.get_columns()
        self.attr_dict = {}
        for attr in self.columns:
            self.attr_dict[attr] = StringVar()

        Label(self.root, text=Capital(self.__class__.__name__), font=('宋体', 15)).pack(side=TOP, fill='x') # , bg='white', fg='red', 

        self.add_Menu()
        self.add_Tree()

    def add_Tree(self):
        self.tree_view = ttk.Treeview(self.root, show='headings', column=self.columns)
        self.tree_view.place(relx=0.01, rely=0.35, relwidth=0.96, relheight=0.6)
        self.tree_view.bind('<ButtonRelease-1>', self.treeview_click)
        
        for col in self.columns:
            self.tree_view.column(col, width=50, anchor="center")
        for col in self.columns:
            self.tree_view.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(_col, True))

        self.scrollbar = Scrollbar(self.root, orient='vertical', command=self.tree_view.yview)
        self.scrollbar.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        self.tree_view.configure(yscrollcommand=self.scrollbar.set)

    def add_Menu(self):
        self.menubar = Menu(self.root)
        # 显示菜单
        self.root.config(menu=self.menubar)
        
        filemenu = Menu(self.menubar, tearoff=False);self.menubar.add_cascade(label="File", menu=filemenu)
        if filemenu:
            openmenu = Menu(filemenu, tearoff=False);filemenu.add_cascade(label="Open", menu=openmenu)
            if openmenu:
                openmenu.add_command(label='Data', command=lambda: self.open_data())
                openmenu.add_command(label='Economy', command=lambda: self.open_economy())
                openmenu.add_command(label='Supply', command=lambda: self.open_supply())
            savemenu = Menu(filemenu, tearoff=False);filemenu.add_cascade(label="Save", menu=savemenu)
            if savemenu:
                savemenu.add_command(label='csv', command=lambda: savecsv(self.tree_view, self.columns))
                savemenu.add_command(label='json', command=lambda: savejson(self.tree_view, self.columns))
                savemenu.add_command(label='xlsx', command=lambda: savexlsx(self.tree_view, self.columns))
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=lambda: self.callback())
        viewmenu = Menu(self.menubar, tearoff=False);self.menubar.add_cascade(label="View", menu=viewmenu)
        if viewmenu:
            viewmenu.add_command(label="Accounts", command=lambda: account())
            viewmenu.add_command(label="SystemLog", command=lambda: systemlog())

    def treeview_click(self, event):
        for item in self.tree_view.selection():
            tup = self.tree_view.item(item, "values")
            for i in range(len(tup)):
                self.attr_dict[self.columns[i]].set(tup[i])

    def treeview_sort_column(self, k, reverse):
        table = []
        for item in self.tree_view.get_children():
            tup = tree_view.item(item, "values")
            table.append(tup)

        table.sort(key=lambda tup: tup[k], reverse=reverse)
        for tup in table:
            self.tree_view.insert("", values=tup)

        self.treeview_sort_column(self, k, reverse=not reverse)

    def callback(self):
        if askokcancel("Query", "Confirm to close the window?"):
            self.root.destroy()

    def clear(self):
        for col in self.columns:
            self.attr_dict[col].set("")

    def get_columns(self):
        world_v2 = Database()
        world_v2.prepare("describe "+self.__class__.__name__)
        columns = [attr[0] for attr in world_v2.fetchall()]
        world_v2.close()
        return tuple(columns)

    def open_data(self):
        self.root.destroy()
        data(self.account)

    def open_economy(self):
        self.root.destroy()
        economy(self.account)
    
    def open_supply(self):
        self.root.destroy()
        supply(self.account)
 
class data(Window):
    def __init__(self, account=None):
        Window.__init__(self, account=account)
        
        Label(self.root, text=self.columns[0]).place(relx=0, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[1]).place(relx=0, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[2]).place(relx=0, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[3]).place(relx=0, rely=0.20, relwidth=0.15)
        Label(self.root, text=self.columns[4]).place(relx=0.3, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[5]).place(relx=0.3, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[6]).place(relx=0.3, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[7]).place(relx=0.3, rely=0.20, relwidth=0.15)
        Label(self.root, text=self.columns[8]).place(relx=0.6, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[9]).place(relx=0.6, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[10]).place(relx=0.6, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[11]).place(relx=0.6, rely=0.20, relwidth=0.15)
        
        Entry(self.root, textvariable=self.attr_dict[self.columns[0]])\
        .place(relx=0.15, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[1]])\
        .place(relx=0.15, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[2]])\
        .place(relx=0.15, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[3]])\
        .place(relx=0.15, rely=0.20, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[4]])\
        .place(relx=0.45, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[5]])\
        .place(relx=0.45, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[6]])\
        .place(relx=0.45, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[7]])\
        .place(relx=0.45, rely=0.20, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[8]])\
        .place(relx=0.75, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[9]])\
        .place(relx=0.75, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[10]])\
        .place(relx=0.75, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[11]])\
        .place(relx=0.75, rely=0.20, relwidth=0.15, height=25)
        
        Button(self.root, text="SEARCH", command=lambda: operations_data.Search(self.tree_view, self.attr_dict))\
        .place(relx=0.15, rely=0.27, relwidth=0.1)
        Button(self.root, text="INSERT", command=lambda: operations_data.Insert(self.tree_view, self.attr_dict, account))\
        .place(relx=0.30, rely=0.27, relwidth=0.1)
        Button(self.root, text="DELETE", command=lambda: operations_data.Delete(self.tree_view, self.attr_dict, account))\
        .place(relx=0.45, rely=0.27, relwidth=0.1)
        Button(self.root, text="MODIFY", command=lambda: operations_data.Modify(self.tree_view, self.attr_dict, account))\
        .place(relx=0.60, rely=0.27, relwidth=0.1)
        Button(self.root, text="CLEAR", command=lambda: self.clear())\
        .place(relx=0.75, rely=0.27, relwidth=0.1)
        
        
        plotmenu = Menu(self.menubar, tearoff=False);self.menubar.add_cascade(label="Plot", menu=plotmenu)
        if plotmenu:
            currentmenu = Menu(plotmenu, tearoff=False);plotmenu.add_cascade(label="Current", menu=currentmenu)
            if currentmenu:
                currentmenu.add_command(label="confirmedCount", command=lambda: currentone(self.tree_view, self.columns, 2))
                currentmenu.add_command(label="confirmedIncr", command=lambda: currentone(self.tree_view, self.columns, 3))
                currentmenu.add_command(label="curedCount", command=lambda: currentone(self.tree_view, self.columns, 4))
                currentmenu.add_command(label="curedIncr", command=lambda: currentone(self.tree_view, self.columns, 5))
                currentmenu.add_command(label="deadCount", command=lambda: currentone(self.tree_view, self.columns, 6))
                currentmenu.add_command(label="deadIncr", command=lambda: currentone(self.tree_view, self.columns, 7))
                currentmenu.add_command(label="existingCount", command=lambda: currentone(self.tree_view, self.columns, 8))
                currentmenu.add_command(label="existingIncr", command=lambda: currentone(self.tree_view, self.columns, 9))
                currentmenu.add_command(label="suspectedCount", command=lambda: currentone(self.tree_view, self.columns, 10))
                currentmenu.add_command(label="suspectedIncr", command=lambda: currentone(self.tree_view, self.columns, 11))
                currentmenu.add_separator()
                currentmenu.add_command(label="All attributes", command=lambda: currentall(self.tree_view, self.columns))
            predictmenu = Menu(plotmenu, tearoff=False);plotmenu.add_cascade(label="Predict", menu=predictmenu)
            if predictmenu:
                predictmenu.add_command(label="confirmedCount", command=lambda: predictone(self.tree_view, self.columns, 2))
                predictmenu.add_command(label="confirmedIncr", command=lambda: predictone(self.tree_view, self.columns, 3))
                predictmenu.add_command(label="curedCount", command=lambda: predictone(self.tree_view, self.columns, 4))
                predictmenu.add_command(label="curedIncr", command=lambda: predictone(self.tree_view, self.columns, 5))
                predictmenu.add_command(label="deadCount", command=lambda: predictone(self.tree_view, self.columns, 6))
                predictmenu.add_command(label="deadIncr", command=lambda: predictone(self.tree_view, self.columns, 7))
                predictmenu.add_command(label="existingCount", command=lambda: predictone(self.tree_view, self.columns, 8))
                predictmenu.add_command(label="existingIncr", command=lambda: predictone(self.tree_view, self.columns, 9))
                predictmenu.add_command(label="suspectedCount", command=lambda: predictone(self.tree_view, self.columns, 10))
                predictmenu.add_command(label="suspectedIncr", command=lambda: predictone(self.tree_view, self.columns, 11))
                predictmenu.add_separator()
                predictmenu.add_command(label="All attributes", command=lambda: predictall(self.tree_view, self.columns))

        # 事件循环
        self.root.mainloop()

    def treeview_sort_column(self, col, reverse):
        if col=='code' or col=='date':
            l = [(self.tree_view.set(k, col), k) for k in self.tree_view.get_children('')]
        else:
            l = [(int(self.tree_view.set(k, col)), k) for k in self.tree_view.get_children('')]
        l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree_view.move(k, '', index)
        # reverse sort next time
        self.tree_view.heading(col, command=lambda _col=col: self.treeview_sort_column(_col, not reverse))

class economy(Window):
    def __init__(self, account=None):
        Window.__init__(self, account=account)

        Label(self.root, text=self.columns[0]).place(relx=0, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[1]).place(relx=0, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[2]).place(relx=0, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[3]).place(relx=0, rely=0.20, relwidth=0.15)
        Label(self.root, text=self.columns[4]).place(relx=0.3, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[5]).place(relx=0.3, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[6]).place(relx=0.3, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[7]).place(relx=0.3, rely=0.20, relwidth=0.15)
        Label(self.root, text=self.columns[8]).place(relx=0.6, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[9]).place(relx=0.6, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[10]).place(relx=0.6, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[11]).place(relx=0.6, rely=0.20, relwidth=0.15)
        
        Entry(self.root, textvariable=self.attr_dict[self.columns[0]])\
        .place(relx=0.15, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[1]])\
        .place(relx=0.15, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[2]])\
        .place(relx=0.15, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[3]])\
        .place(relx=0.15, rely=0.20, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[4]])\
        .place(relx=0.45, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[5]])\
        .place(relx=0.45, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[6]])\
        .place(relx=0.45, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[7]])\
        .place(relx=0.45, rely=0.20, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[8]])\
        .place(relx=0.75, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[9]])\
        .place(relx=0.75, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[10]])\
        .place(relx=0.75, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[11]])\
        .place(relx=0.75, rely=0.20, relwidth=0.15, height=25)
        
        Button(self.root, text="SEARCH", command=lambda: operations_economy.Search(self.tree_view, self.attr_dict))\
        .place(relx=0.15, rely=0.27, relwidth=0.1)
        Button(self.root, text="INSERT", command=None)\
        .place(relx=0.30, rely=0.27, relwidth=0.1)
        Button(self.root, text="DELETE", command=None)\
        .place(relx=0.45, rely=0.27, relwidth=0.1)
        Button(self.root, text="MODIFY", command=None)\
        .place(relx=0.60, rely=0.27, relwidth=0.1)
        Button(self.root, text="CLEAR", command=lambda: self.clear())\
        .place(relx=0.75, rely=0.27, relwidth=0.1)

    def treeview_sort_column(self, col, reverse):
        if col=='code' or col=='date':
            l = [(self.tree_view.set(k, col), k) for k in self.tree_view.get_children('')]
        else:
            l = [(float(self.tree_view.set(k, col)), k) for k in self.tree_view.get_children('')]
        l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree_view.move(k, '', index)
        # reverse sort next time
        self.tree_view.heading(col, command=lambda _col=col: self.treeview_sort_column(_col, not reverse))

class supply(Window):
    def __init__(self, account=None):
        Window.__init__(self, account=account)

        Label(self.root, text=self.columns[0]).place(relx=0, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[1]).place(relx=0, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[2]).place(relx=0, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[3]).place(relx=0.3, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[4]).place(relx=0.3, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[5]).place(relx=0.3, rely=0.15, relwidth=0.15)
        Label(self.root, text=self.columns[6]).place(relx=0.6, rely=0.05, relwidth=0.15)
        Label(self.root, text=self.columns[7]).place(relx=0.6, rely=0.10, relwidth=0.15)
        Label(self.root, text=self.columns[8]).place(relx=0.6, rely=0.15, relwidth=0.15)
        
        Entry(self.root, textvariable=self.attr_dict[self.columns[0]])\
        .place(relx=0.15, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[1]])\
        .place(relx=0.15, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[2]])\
        .place(relx=0.15, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[3]])\
        .place(relx=0.45, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[4]])\
        .place(relx=0.45, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[5]])\
        .place(relx=0.45, rely=0.15, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[6]])\
        .place(relx=0.75, rely=0.05, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[7]])\
        .place(relx=0.75, rely=0.10, relwidth=0.15, height=25)
        Entry(self.root, textvariable=self.attr_dict[self.columns[8]])\
        .place(relx=0.75, rely=0.15, relwidth=0.15, height=25)
        
        Button(self.root, text="SEARCH", command=None)\
        .place(relx=0.15, rely=0.27, relwidth=0.1)
        Button(self.root, text="INSERT", command=None)\
        .place(relx=0.30, rely=0.27, relwidth=0.1)
        Button(self.root, text="DELETE", command=None)\
        .place(relx=0.45, rely=0.27, relwidth=0.1)
        Button(self.root, text="MODIFY", command=None)\
        .place(relx=0.60, rely=0.27, relwidth=0.1)
        Button(self.root, text="CLEAR", command=lambda: self.clear())\
        .place(relx=0.75, rely=0.27, relwidth=0.1)
        
