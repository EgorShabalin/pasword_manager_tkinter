import tkinter
from tkinter import IntVar
from tkinter import ttk
import random
import string
import sqlite3


def generator(length, numbersFlag, symbolsFlag): #password generator function
    if length.isdigit() and int(length) < 1000:    
        length = int(length)
        upperLetters = string.ascii_uppercase
        lowerLetters = string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation

        chars = upperLetters + lowerLetters        
        
        password = []
        password.append(random.choice(upperLetters))
        password.append(random.choice(lowerLetters))        

        if numbersFlag == 1:
            chars = chars + numbers
            password.append(random.choice(numbers))
        
        if symbolsFlag == 1:
            chars = chars + symbols
            password.append(random.choice(symbols))
        
        if len(password) <= length:
            saltlen = length - len(password)
        else:
            saltlen = 0

        password.extend(random.choices(chars, k=saltlen))
        random.shuffle(password)
        password = ''.join(password)
        out.delete(0, tkinter.END)
        out.insert(0, password)
    
    elif len(length) == 0:
        userInput.delete(0, tkinter.END)
        userInput.insert(0, 'ENTER DIGIT ONLY!')

    elif int(length) > 1000:
        userInput.delete(0, tkinter.END)
        userInput.insert(0, 'TOO LONG!')

    else:
        userInput.delete(0, tkinter.END)
        userInput.insert(0, 'ENTER DIGIT ONLY!')


class Database: #sqlite3 handling
    def __init__(self):
        self.conn = sqlite3.connect('data.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Passwords (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, password TEXT)')
        self.conn.commit()

    def view(self):
        self.cur.execute('SELECT * FROM Passwords')
        rows = self.cur.fetchall()
        return rows
    
    def save(self, name, psw):
        self.cur.execute('INSERT INTO Passwords(name, password) VALUES (?,?)', (str(name), str(psw)))
        self.conn.commit()    

    def delete(self, index):
        self.cur.execute('DELETE FROM Passwords WHERE id=?', (str(index),))
        self.conn.commit()

    def copy(self, index):
        self.cur.execute('SELECT password FROM Passwords WHERE id=?', (str(index),))
        c = self.cur.fetchall()
        return str(c[0][0])

    def __del__(self): #closes sql connection
        self.conn.close()


data = Database()

switch = False

def view_in_tree(tree): #refreshes tree view
    tree.delete(*tree.get_children())
    rows = data.view()
    hidden = '******************************'
    global switch
    for row in rows:
        if switch == True:
            tree.insert('', tkinter.END, values = row)
        else:
            tree.insert('', tkinter.END, values = (row[0], row[1], hidden))

def not_common(): #validates existing names and passwords in database
    mark = []
    rows = data.view()
    for row in rows:
        if str(out.get()) in row[2]:
            out.delete(0, tkinter.END)
            out.insert(0, '!!!PASSWORD EXISTS!!!')
            mark.append(False)
        elif str(inputPassName.get()) in row[1]:
            inputPassName.delete(0, tkinter.END)
            inputPassName.insert(0, '!!!NAME EXISTS!!!')
            mark.append(False)
        else:
            mark.append(True)
    if False in mark:
        return False
    else:
        return True

def save_password():
    def saveit():
        data.save(inputPassName.get(), out.get())
        inputPassName.delete(0, tkinter.END)
        inputPassName.insert(0, 'PASSWORD SAVED!')

    if len(out.get()) == 0:
        userInput.delete(0, tkinter.END)
        userInput.insert(0, 'GENERATE PASSWORD!')
    elif len(inputPassName.get()) == 0:
        inputPassName.delete(0, tkinter.END)
        inputPassName.insert(0, 'ENTER NAME!')
    else:
        if not_common():
            saveit()
            view_in_tree(tree)
        else:
            pass

def delete_row(tree):
    try:
        selected = tree.selection()[0]
        index = tree.item(selected)['values']
        index = index[0]    
        tree.delete(selected)
        data.delete(index)
    except IndexError:
        pass


def on_off():
    global switch
    if switch == True:
        btnSwitch.config(text = 'Show')
        switch = False
        view_in_tree(tree)
    else:
        btnSwitch.config(text = 'Hide ')
        switch = True
        view_in_tree(tree)    
    return switch

def copy(event):
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    values = item['values']
    index = values[0]
    p = data.copy(index)
    cp = tkinter.Tk()
    cp.withdraw()
    cp.clipboard_clear()
    cp.clipboard_append(p)
    cp.update()
    cp.destroy()
    out.delete(0, tkinter.END)
    out.insert(0, 'COPIED TO CLIPBOARD!')


def clear(event):
    item_id = event.widget.focus()
    item = event.widget.delete(0, tkinter.END)
    


#all the gui code

window = tkinter.Tk()

numbersFlag = IntVar()
symbolsFlag = IntVar()

window['bg'] = '#000000'
window.title('BruqwaPassMan')
window.geometry('770x490')

window.resizable(width=True, 
                 height = True)

canvas = tkinter.Canvas(window, 
                        height = 300, 
                        width = 300)
canvas.pack()


frame = tkinter.Frame(window, bg = 'black')
frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)


tree = ttk.Treeview(frame, 
                    columns = ('id', 'Name', 'Password'), 
                    height = 20, 
                    show = 'headings',)

tree.column('id', width = 30)
tree.column('Name', width = 250)
tree.column('Password', width = 250)

tree.heading('id', text = 'ID', )
tree.heading('Name', text = 'Name')
tree.heading('Password', text = 'Password')


tree.grid(column = 1, 
          row = 1, 
          rowspan = 9, 
          columnspan = 2,)

tree.bind('<Double-Button-1>', copy)


title1 = tkinter.Label(frame, 
                       text = 'Enter password length\n(should be more then 4): ', 
                       bg = 'black', 
                       fg = 'orange', 
                       font =70)

title1.grid(column = 0, 
            row = 0, 
            stick = 'we', 
            padx = 10, 
            pady = 10)


userInput = tkinter.Entry(frame, 
                          bg = 'black', 
                          fg = 'orange', 
                          justify='center', 
                          insertbackground = 'orange')

userInput.grid(column = 0, 
               row = 1, 
               stick = 'we', 
               padx = 10, 
               pady = 10)
userInput.bind('<FocusIn>', clear)


chekboxNumbers = tkinter.Checkbutton(frame, 
                                     text = 'Use numbers', 
                                     fg = 'orange', 
                                     bg = 'black', 
                                     activebackground = 'black', 
                                     activeforeground = 'orange', 
                                     padx = 8, 
                                     variable = numbersFlag, 
                                     onvalue = 1, 
                                     offvalue = 0)

chekboxNumbers.grid(column = 0, 
                    row = 2)
#chekboxNumbers.deselect()


chekboxSymbols = tkinter.Checkbutton(frame, 
                                     text = 'Use symbols', 
                                     fg = 'orange', 
                                     bg = 'black', 
                                     activebackground = 'black', 
                                     activeforeground = 'orange', 
                                     padx = 8, 
                                     variable = symbolsFlag, 
                                     onvalue = 1, 
                                     offvalue = 0)

chekboxSymbols.grid(column = 0, 
                    row = 3)
#chekboxSymbols.deselect()


btnGen = tkinter.Button(frame, 
                        text = 'Generate', 
                        bg = 'orange', 
                        command = lambda: generator(userInput.get(), numbersFlag, symbolsFlag))

btnGen.grid(column = 0, 
            row = 4, 
            stick = 'we', 
            padx = 10, 
            pady = 10)


title2 = tkinter.Label(frame, 
                       text = 'Your password is: ', 
                       bg = 'black', 
                       fg = 'orange', 
                       font =70)

title2.grid(column = 0, 
            row = 5, 
            stick = 'we', 
            padx = 10, 
            pady = 10)


out = tkinter.Entry(frame, 
                    bg = 'black', 
                    fg = 'lime', 
                    justify='center', 
                    insertbackground = 'lime')

out.grid(column = 0, 
         row = 6, 
         stick = 'we', 
         padx = 10, 
         pady = 10)


title3 = tkinter.Label(frame, 
                       text = 'Enter name to save\ngenerated password: ', 
                       bg = 'black', 
                       fg = 'orange', 
                       font =70)

title3.grid(column = 0, 
            row = 7, 
            stick = 'we', 
            padx = 10, 
            pady = 10)


inputPassName = tkinter.Entry(frame, 
                              bg = 'black', 
                              fg = 'orange', 
                              justify='center', 
                              insertbackground = 'orange')

inputPassName.grid(column = 0, 
                   row = 8, 
                   stick = 'we', 
                   padx = 10, 
                   pady = 10)

inputPassName.bind('<FocusIn>', clear)


btnSave = tkinter.Button(frame, 
                         text = 'Save password', 
                         bg = 'orange', 
                         command = lambda: save_password())

btnSave.grid(column = 0, 
             row = 9, 
             stick = 'we', 
             padx = 10, 
             pady = 10)


title4 = tkinter.Label(frame, 
                       text = 'Saved Passwords:\n(double click to copy)', 
                       bg = 'black', 
                       fg = 'orange', 
                       font =70)

title4.grid(column = 1, 
            row = 0, 
            stick = 'ws', 
            padx = 10, 
            pady = 10)


btnSwitch = tkinter.Button(frame, 
                           text = 'Show', 
                           bg = 'orange', 
                           command = lambda: on_off())

btnSwitch.grid(column = 2, 
               stick = 'es', 
               row = 0, 
               padx = 10, 
               pady = 10)


btnDelete = tkinter.Button(frame, 
                           text = 'Delete', 
                           bg = 'orange', 
                           command = lambda: delete_row(tree))

btnDelete.grid(column = 1, 
               stick = 'es', 
               row = 0, 
               padx = 10, 
               pady = 10)


s = ttk.Style()

s.configure('Treeview', 
            color = '#000', 
            background = '#000', 
            foreground = 'lime')


window.mainloop()
