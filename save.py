from tkinter.messagebox import *
import easygui

def savecsv(tree_view, columns):
    filename = easygui.enterbox("please input the filename", default="data.csv")

    with open(filename, "w") as f:
        f.write(','.join(columns))
        f.write('\n')
        for item in tree_view.get_children():
            tup = tree_view.item(item, "values")
            f.write(','.join(tup))
            f.write('\n')

    showinfo("Reminder", f"Successfully exported selected data to {filename}")

def savejson(tree_view, columns):
    pass

def savexlsx(tree_view, columns):
    pass
