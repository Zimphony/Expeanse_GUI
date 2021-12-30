from tkinter import * # import * --> import only file main(_init_)
from tkinter import ttk, messagebox
import csv
from datetime import datetime
# ttk is a theme of Tk

GUI = Tk()
GUI.title('Program for record spending by Tanaphat')
GUI.geometry('600x500+500+100') 

# B1 = Button(GUI,text = 'Hello')
# B1.pack(ipadx = 50,ipady = 5)  #.pack()--> use to set something into GUI

# --------------menu---------------------
menu_bar = Menu(GUI)
GUI.config(menu=menu_bar)

# file menu
filemenu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import csv')
filemenu.add_command(label='Export to Googlesheet')
# Help
def about():
    messagebox.showinfo('About','Hello, This program was developed for store a data')

helpmenu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=about)

# Donate
donatemenu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='donate', menu=donatemenu)
#----------------------------------------





# ---------Adding Frame---------------
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab) # Can add width,height 
T2 = Frame(Tab)
F1 = Frame(T1)
F1.pack()
Tab.pack(fill=BOTH, expand=1)
# -----------------------------------

# ------Insert-Image--------------
icon_t1 = PhotoImage(file='wallet-icon.png') # .subsample(2)--> minimize picture
icon_t2 = PhotoImage(file='Cash-register-icon.png')
icon_b2 = PhotoImage(file='Save-icon.png').subsample(2)
icon_main = PhotoImage(file='tasks-icon.png')
Tab.pack(fill=BOTH, expand=1)
# --------------------------------

# ---------Adhere tab menu------------
Tab.add(T1, text=f'{"Add expense" : >{20}}', image=icon_t1, compound='right')
Tab.add(T2, text=f'{"Total expense" : >{20}}', image=icon_t2, compound='right')
# ------------------------------------

# ---------Adhere main icon-----------
mainicon = Label(F1, image=icon_main)
mainicon.pack()
# ------------------------------------

days = {'Mon': 'จันทร์',
        'Tue': 'อังคาร',
        'Wed': 'พุธ',
        'Thur': 'พฤหัส',
        'Fri': 'ศุกร์',
        'Sat': 'เสาร์',
        'Sun': 'อาทิตย์'}


def save(event=None):
    expense = v_expense.get() # .get() --> get value from ......
    price = v_price.get()
    no = v_no.get()
    if expense == '' :
        print('No data')
        messagebox.showwarning('Error','Please enter Object')
        return()
    elif price == '' :
        messagebox.showwarning('Error','Please enter price')
        return()
    elif no == '' :
        quantity = 1

    try:
        total = float(no)*float(price)
        day = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt = days[day]+'-'+dt
        print(f"Object : {expense} Price/piece : {price}$")
        print(f"No : {no}   Total : {total}$")
        text = f"Object : {expense} Price : {price}$ \n No : {no}   Total : {total}$"
        v_result.set(text)
        # clear data
        v_expense.set('')
        v_price.set('')
        v_no.set('')
        # Save data into CSV *import csv first*
        with open('savedata.csv','a',encoding='utf-8', newline='') as f:
            # with--> is command to automatic open and close
            # 'a'--> continuous saving from last one
            # newline = '' --> no blank line
            fw = csv.writer(f) # create function for write data
            data = [dt,expense,price,no,total]
            fw.writerow(data)
        # make cursor back to original E1
        E1.focus()
        update_table()
    except Exception as e:
        print('Error :',e)
        #messagebox.showerror('Error','Please enter a correct value')
        messagebox.showwarning('Error','Please enter a correct value')
        #messagebox.showinfo('Error','Please enter a correct value')
        v_expense.set('')
        v_price.set('')
        v_no.set('')
        E1.focus()
        
#Able to use enter
GUI.bind('<Return>',save) #must write def Save(event=None)
#.bind()--> to check that Did the user use<Return> (Enter),If use it will save

FONT1 = (None,13)
# ------Text1------
L1 = ttk.Label(F1, text='Object of spending', font = FONT1).pack()
v_expense = StringVar()  #StringVar --> to store data in GUI
E1 = ttk.Entry(F1, textvariable=v_expense,font=FONT1)
E1.pack()
# ------------------

# ------Text2------
L2 = ttk.Label(F1, text='Price (Dollar $)', font = FONT1).pack()
v_price = StringVar()  #StringVar --> to store data in GUI
E2 = ttk.Entry(F1, textvariable=v_price,font=FONT1)
E2.pack()
# ------------------

# ------Text3------
L3 = ttk.Label(F1, text='Number (Piece)', font = FONT1).pack()
v_no = StringVar()  #StringVar --> to store data in GUI
E3 = ttk.Entry(F1, textvariable=v_no,font=FONT1)
E3.pack()
# ------------------

# -----Bottom1------
B2 = ttk.Button(F1, text=f'{"save": ^{10}}', command=save, image=icon_b2, compound='right')
B2.pack(ipadx=5, ipady=5)
# ------------------

# -----Result-------
v_result = StringVar()
v_result.set('------result------')
result = ttk.Label(F1, textvariable=v_result, font=FONT1, foreground='green')
result.pack(pady=20)
# ------------------

###################################################Tab2################################################

def read_csv():
    with open('savedata.csv', newline='', encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
        #print(data)
        #print(data[0][0])
        #for a,b,c,d,e in data:
        #    print(a)
    return data

def update_table():
    result_table.delete(*result_table.get_children())
    data = read_csv()
    for d in data:
        result_table.insert('', 0, value=d)

# -------------table----------------
L = ttk.Label(T2,text='Result Table',font=FONT1).pack(pady=20)
Header = ['Date-Time', 'Object', 'Price', 'Number', 'Total']
result_table = ttk.Treeview(T2, columns=Header, show='headings', height=10)
result_table.pack()
#type1
    #for i in range(len(Header)):
    #    result_table.heading(Header[i], text=Header[i])
#type2
for h in Header:
    result_table.heading(h ,text=h)

headerwidth =[150,120,80,80,80] 
for i,w in zip(Header,headerwidth):
    result_table.column(i, width=w)

#---adding list-------

# ----------------------------------

















update_table()
read_csv()
GUI.mainloop()
