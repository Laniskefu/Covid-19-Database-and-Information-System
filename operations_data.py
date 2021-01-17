from database import Database
from tkinter.messagebox import *
import easygui
import time

class data_operation:
    def __init__(self, tree_view, attr_dict):
        self.password = "shankudedoushidaiji"
        self.db = Database()
        self.code = attr_dict['code'].get()
        self.date = attr_dict['date'].get()
        self.confirmedCount = attr_dict['confirmedCount'].get()
        self.confirmedIncr = attr_dict['confirmedIncr'].get()
        self.curedCount = attr_dict['curedCount'].get()
        self.curedIncr = attr_dict['curedIncr'].get()
        self.deadCount = attr_dict['deadCount'].get()
        self.deadIncr = attr_dict['deadIncr'].get()
        self.existingCount = attr_dict['existingCount'].get()
        self.existingIncr = attr_dict['existingIncr'].get()
        self.suspectedCount = attr_dict['suspectedCount'].get()
        self.suspectedIncr = attr_dict['suspectedIncr'].get()

    def dataValidityCheck(self):
        self.db.cursor.execute("select * from countrylist")
        countryCodes = [row[0] for row in self.db.cursor.fetchall()]
        if not self.code in countryCodes: return False
        if not self.date.isdigit() or len(self.date)!=8: return False
        return True

    def dataRationalityCheck(self):
        CountRational = self.confirmedCount>=0 and self.curedCount>=0 and self.deadCount>=0 and self.existingCount>=0 and self.suspectedCount>=0
        IncrRational = self.confirmedIncr>=0 and self.curedIncr>=0 and self.deadIncr>=0
        return CountRational and IncrRational

    def addSystemLog(self, account, command):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        command_ = command.replace("'", "")
        sql = f"insert into systemlog values ('{datetime}', '{account}', '{command_}')"
        self.db.prepare(sql)
        self.db.update()

class Insert(data_operation):
    def __init__(self, tree_view, attr_dict, account):
        if not account:
            showinfo("Reminder", "Sorry, tourist mode does not support this function")
            return None
        data_operation.__init__(self, tree_view, attr_dict)

        try:
            if not self.dataValidityCheck(): raise ValueError
            self.confirmedCount = int(self.confirmedCount)
            self.confirmedIncr = int(self.confirmedIncr)
            self.curedCount = int(self.curedCount)
            self.curedIncr = int(self.curedIncr)
            self.deadCount = int(self.deadCount)
            self.deadIncr = int(self.deadIncr)
            self.existingCount = int(self.existingCount)
            self.existingIncr = int(self.existingIncr)
            self.suspectedCount = int(self.suspectedCount)
            self.suspectedIncr = int(self.suspectedIncr)
        except ValueError:
            showerror("Insertion failed", "Information incomplete or invalid")
        else:
            if self.dataRationalityCheck():
                if self.db.prepare(f"select * from data where code='{self.code}' and date='{self.date}'")==0:
                    sql = f"insert into data values('{self.code}', '{self.date}', {self.confirmedCount}, {self.confirmedIncr}, {self.curedCount}, {self.curedIncr}, {self.deadCount}, {self.deadIncr}, {self.existingCount}, {self.existingIncr}, {self.suspectedCount}, {self.suspectedIncr})"
                    result = self.db.prepare(sql)
                    if showwarning("Warning", f"Confirm to insert {self.code} {self.date}?"):
                        password=easygui.enterbox("Please input the database management password")
                        if password:
                            while password!=self.password:
                                if askretrycancel("Error","Wrong password, retry or not?"): 
                                    password=easygui.enterbox("Please input the database management password")
                                else: break
                            else:
                                self.db.update()
                                showinfo("Reminder", f"Successfully inserted {self.code} {self.date}")
                                self.addSystemLog(account, sql)
                else:
                    showerror("Insertion failed", "Entry already exist")
            else:
                showerror("Insertion failed", "Information unreasonable")
        finally:
            self.db.close()

class Delete(data_operation):
    def __init__(self, tree_view, attr_dict, account):
        if not account:
            showinfo("Reminder", "Sorry, tourist mode does not support this function")
            return None
        data_operation.__init__(self, tree_view, attr_dict)

        sql = "delete from data"
        if self.code:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" code='{self.code}'"
        if self.date:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" date='{self.date}'"
        if self.confirmedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" confirmedCount='{self.confirmedCount}'"
        if self.confirmedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" confirmedIncr='{self.confirmedIncr}'"
        if self.curedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" curedCount='{self.curedCount}'"
        if self.curedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" curedIncr='{self.curedIncr}'"
        if self.deadCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" deadCount='{self.deadCount}'"
        if self.deadIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" deadIncr='{self.deadIncr}'"
        if self.existingCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" existingCount='{self.existingCount}'"
        if self.existingIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" existingIncr='{self.existingIncr}'"
        if self.suspectedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" suspectedCount='{self.suspectedCount}'"
        if self.suspectedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" suspectedIncr='{self.suspectedIncr}'"

        result = self.db.cursor.execute(sql)
        if showwarning("Warning", f"Confirm to delete {result} entries?"):
            password=easygui.enterbox("Please input the database management password")
            if password:
                while password!=self.password:
                    if askretrycancel("Error","Wrong password, retry or not?"): 
                        password=easygui.enterbox("Please input the database management password")
                    else: break
                else:
                    self.db.update()
                    showinfo("Reminder", f"Successfully deleted {result} entries")
                    self.addSystemLog(account, sql)
        self.db.close()

class Modify(data_operation):
    def __init__(self, tree_view, attr_dict, account):
        if not account:
            showinfo("Reminder", "Sorry, tourist mode does not support this function")
            return None
        data_operation.__init__(self, tree_view, attr_dict)

        try:
            if not self.dataValidityCheck(): raise ValueError
            self.confirmedCount = int(self.confirmedCount)
            self.confirmedIncr = int(self.confirmedIncr)
            self.curedCount = int(self.curedCount)
            self.curedIncr = int(self.curedIncr)
            self.deadCount = int(self.deadCount)
            self.deadIncr = int(self.deadIncr)
            self.existingCount = int(self.existingCount)
            self.existingIncr = int(self.existingIncr)
            self.suspectedCount = int(self.suspectedCount)
            self.suspectedIncr = int(self.suspectedIncr)
        except ValueError:
            showerror("Insertion failed", "Information incomplete or invalid")
        else:
            if self.dataRationalityCheck():
                if self.db.prepare(f"select * from data where code='{self.code}' and date='{self.date}'")!=0:
                    sql = f"update data set confirmedCount={self.confirmedCount}, confirmedIncr={self.confirmedIncr}, curedCount={self.curedCount}, curedIncr={self.curedIncr}, deadCount={self.deadCount}, deadIncr={self.deadIncr}, existingCount={self.existingCount}, existingIncr={self.existingIncr}, suspectedCount={self.suspectedCount}, suspectedIncr={self.suspectedIncr} where code='{self.code}' and date='{self.date}'"
                    result = self.db.prepare(sql)
                    if showwarning("Warning", f"Confirm to modify {self.code} {self.date}?"):
                        password=easygui.enterbox("Please input the database management password")
                        if password:
                            while password!=self.password:
                                if askretrycancel("Error","Wrong password, retry or not?"): 
                                    password=easygui.enterbox("Please input the database management password")
                                else: break
                            else:
                                self.db.update()
                                showinfo("Reminder", f"Successfully modified {self.code} {self.date}")
                                self.addSystemLog(account, sql)
                else:
                    showerror("Modification failed", "Entry does not exist")
            else:
                showerror("Modification failed", "Information unreasonable")
        finally:
            self.db.close()

class Search(data_operation):
    def __init__(self, tree_view, attr_dict):
        data_operation.__init__(self, tree_view, attr_dict)

        sql = "select * from data"
        if self.code:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" code='{self.code}'"
        if self.date:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" date='{self.date}'"
        if self.confirmedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" confirmedCount='{self.confirmedCount}'"
        if self.confirmedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" confirmedIncr='{self.confirmedIncr}'"
        if self.curedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" curedCount='{self.curedCount}'"
        if self.curedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" curedIncr='{self.curedIncr}'"
        if self.deadCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" deadCount='{self.deadCount}'"
        if self.deadIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" deadIncr='{self.deadIncr}'"
        if self.existingCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" existingCount='{self.existingCount}'"
        if self.existingIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" existingIncr='{self.existingIncr}'"
        if self.suspectedCount:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" suspectedCount='{self.suspectedCount}'"
        if self.suspectedIncr:
            sql += ' where' if len(sql)<20 else ' and'
            sql += f" suspectedIncr='{self.suspectedIncr}'"

        print(sql)
        result = self.db.cursor.execute(sql)
        rows = self.db.cursor.fetchall()

        x = tree_view.get_children()
        for item in x:
            tree_view.delete(item)
        for row in rows:
            tree_view.insert("", 'end', values=row)
        showinfo("Reminder", f"Found {result} results")

        self.db.close()
