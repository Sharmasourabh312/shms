import tkinter as tk
import traceback
from tkcalendar import DateEntry
from tkinter import font, messagebox, simpledialog, ttk
from datetime import datetime
from mysql.connector import IntegrityError,InterfaceError
import shmsdbcontroller


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.valid =False
        self.Invalid = None
        self.Invalid1 = None
        self.font = font.Font(
            weight="bold",
            slant="italic",
            size=15
        )
        self.alphabets = [
            ['`', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y',
                'u', 'i', 'o', 'p', '[', ']', "\\"],
            ['CapsLK', 'a', 's', 'd', 'f', 'g',
                'h', 'j', 'k', 'l', ';', "'", 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Space']
        ]
        self.window=None
        self.caplock = False
        self.w = None

        self.photo = tk.PhotoImage(file="./icons/logo.png")
        self.root.iconphoto(self.root, self.photo)
        
        self.root.title("Smart Health Monitoring System")  
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.root.geometry(
            f"{self.sw // 2}x{self.sh - 200}+{self.sw // 4}+{100}")
        self.root.minsize(height=f"{self.sh - 200}", width=f"{self.sw // 2}")
        self.controller = shmsdbcontroller.controller()
        self.name = tk.StringVar()
        self.temp = tk.DoubleVar()
        self.bp = tk.DoubleVar()
        self.bs = tk.DoubleVar()
        self.pr = tk.DoubleVar()
        self.adh = tk.StringVar()
        self.addres = tk.StringVar()
        self.contact = tk.StringVar()
        self.dob = tk.StringVar()

        self.root.protocol('WM_DELETE_WINDOW',self.destroyroot)
        self.create_hompepage()

    def create_hompepage(self):
        self.destroy_VirtualKey()
        self.homepage = tk.Frame(self.root, height=(self.sh - 200), width=(self.sw // 2), border=5)
        self.bg = tk.Label(self.homepage, bg="Cyan")

        self.l1 = tk.Label(self.homepage, text="Welcome To Smart Health Monitoring System",font="Futura 22 bold", fg="White", bg="Black", borderwidth=4, width=36)
        self.login = tk.Button(self.homepage, text="Login ", fg="Cyan", bg="Black",
                               width=10, relief=tk.RAISED, borderwidth=2, font="Arial 10 bold",command=self.createloginpage)
        self.signup = tk.Button(self.homepage, text=" Sign up ", fg="Cyan", bg="Black",
                               width=10, relief=tk.RAISED, borderwidth=2, font="Arial 10 bold",command=self.createsignup)

        self.Exit = tk.Button(self.homepage, text="Exit", fg="Cyan", bg="Black",
                              width=10, relief=tk.RAISED, borderwidth=2, font="Arial 10 bold", command=self.destroyroot)

        self.view = tk.Button(self.homepage, text="View Reports", bg="Black", fg="Cyan", width=10, relief=tk.RAISED,
                              command=self.createviewpage, borderwidth=2, font="Arial 10 bold")
        self.pack_homepage()
        ########################## SIGN UP PAGE  ###########################

    def createsignup(self):
        self.destroyhomepage()
        self.sign_frame = tk.Frame(self.root)
        self.sign_label = tk.Label(self.sign_frame,bg="Skyblue",font = self.font)
        self.sign_sign =tk.Label(self.sign_label,bg="Skyblue",font=("Arial",30,"bold"),text="Sign up")
        self.BackButton = tk.Button(
            self.sign_label, text="\U0001F3E0", fg="Black", bg="Skyblue", font="Arial 20 bold", relief=tk.SOLID,activebackground="Skyblue",command=self.destroy_signup)
        self.sign_labelframe = tk.Label(self.sign_label,bg="Skyblue")
            ####ADhaar LABEL#######

        self.sign_adh = tk.Label(self.sign_labelframe,text="Adhaar No. :",bg="Skyblue",font = self.font)
        self.sign_adh_input = ttk.Entry(self.sign_labelframe,textvariable=self.adh,width=25,justify=tk.CENTER)
        self.sign_adh_input.bind("<Button-1>",lambda e=0:self.VirtualKey(self.alphabets, self.sign_adh_input))
        self.sign_adh_input.delete(0,tk.END)
        ######NAME LABEL ############

        self.sign_name = tk.Label(self.sign_labelframe,text="Name :",bg="Skyblue",font = self.font)
        self.sign_name_input = ttk.Entry(self.sign_labelframe,textvariable=self.name,width=25,justify=tk.CENTER)
        self.sign_name_input.bind("<Button-1>",lambda e=0:self.VirtualKey(self.alphabets, self.sign_name_input))
        self.sign_name_input.delete(0,tk.END)
        ######CONTACT LABEL ##########

        self.sign_cont = tk.Label(self.sign_labelframe,text="Contact NO. :",bg="Skyblue",font = self.font)
        self.sign_cont_input = ttk.Entry(self.sign_labelframe,textvariable=self.contact,width=25,justify=tk.CENTER)
        self.sign_cont_input.bind("<Button-1>",lambda e=0:self.VirtualKey(self.alphabets, self.sign_cont_input))
        self.sign_cont_input.delete(0,tk.END)

        ##### ADDRESS LABEL ###########

        self.sign_add = tk.Label(self.sign_labelframe,text="Address :",bg="Skyblue",font = self.font)
        self.sign_add_input = ttk.Entry(self.sign_labelframe,textvariable=self.addres,width=25,justify=tk.CENTER)
        self.sign_add_input.bind("<Button-1>",lambda e=0: self.VirtualKey(self.alphabets, self.sign_add_input))
        self.sign_add_input.delete(0,tk.END)
        
        ####### Date Of Birth ############
        self.dob.set("DD/MM/YYYY")
        self.sign_date = tk.Label(self.sign_labelframe,text="Date of Birth :",font=self.font,bg="skyblue")
        today = datetime.now()
        self.sign_date_input = DateEntry(self.sign_labelframe,state="readonly",font=("Aril",12,"bold"),textvariable=self.dob,date_pattern="DD/MM/YYYY",maxdate=today.date())
        self.sign_date_input.bind("<FocusIn>",self.cal_down)
        # self.sign_date_input.bind("<<DateEntrySelected>>",))

        self.sign_submit = tk.Button(self.sign_labelframe,text="Sign up",fg="White",bg="Blue",font=("Helvatica",10,"bold"),command=self.valid_sign_adh)

        self.sign_status = tk.Label(self.sign_label,bg="White",fg="Red",font=("Arial",15,"italic"))

        self.pack_signup()

    def valid_sign_adh(self):
        self.sign_status.config(text="")
        adh = self.adh.get()
        if not adh.isnumeric() or len(adh) != 12:
            if  not adh.isnumeric():
                if len(adh) ==0:
                    self.sign_status.config(text="Adhaar Number required")
                else:
                    self.sign_status.config(text="Adhaar should be Number!")
            elif len(adh) != 12:
                self.sign_status.config(text="Adhaar should be of 12 digit!")
        else:
            self.valid_sign_name()

    def valid_sign_name(self):
        name = self.name.get()
        if not name.isalpha() :
            if len(name.strip())<=0:
                self.sign_status.config(text="*Name is required")
            else:
                self.sign_status.config(text="Name should be in Alphabet!")
        else:
            self.valid_sign_cont()

    def valid_sign_cont(self):
        cont = self.contact.get()
        if not cont.isnumeric() or len(cont.strip()) != 10:
            if  not cont.isnumeric():
                self.sign_status.config(text="Contact Number should be Numeric!")
            else:
                self.sign_status.config(text="Contact Number should be of 10 digit!")
            self.sign_cont_input.setfocus()
        else:
            self.valid_sign_adress()

    def valid_sign_adress(self):
        address = self.addres.get()
        if len(address) <=0:
            self.sign_status.config(text="Invalid Address!")
            self.sign_add_input.focus()
        else:
            self.sign_up_func()


    def destroy_signup(self):
        self.destroy_VirtualKey()
        self.create_hompepage()
        self.sign_frame.destroy()

    def sign_up_func(self):
        self.destroy_VirtualKey()
        try:
            self.controller.sign_up(adh=self.adh,name=self.name,addres=self.addres,cont=self.contact,dob=self.dob)
        except IntegrityError:
            if messagebox.askyesno("Already user","Please login"):
                self.destroy_signup()
                self.create_input_page()
        except InterfaceError:
            messagebox.showerror("Database Error","Not able to connect to database")
        except Exception:
            messagebox.showerror("Database Error","Some Unkown Error!!")
        else:
            messagebox.showinfo("Sign up","Successfuly Signed up")
            self.destroy_signup()
            self.create_input_page()

        finally:
            self.controller.close_db()
    
    def cal_down(self,e=0):
        self.sign_labelframe.focus()
        self.sign_date_input.drop_down()


    def pack_signup(self):
        self.sign_frame.place(x=0,y=0,relheight=1,relwidth=1)
        self.sign_label.place(x=0,y=0,relheight=1,relwidth=1)
        self.sign_sign.place(x=200,y=20)
        self.BackButton.place(x=10,y=10)
        self.sign_labelframe.place(x=20,y=100)

        self.sign_adh.grid(row=0,column=0,sticky="E")
        self.sign_adh_input.grid(row=0,column=1,padx=20)

        self.sign_name.grid(row=1,column=0,sticky="E")
        self.sign_name_input.grid(row=1,column=1)

        self.sign_cont.grid(row=2,column=0,sticky="E")
        self.sign_cont_input.grid(row=2,column=1)

        self.sign_add.grid(row=3,column=0,sticky="E")
        self.sign_add_input.grid(row=3,column=1)

        self.sign_date.grid(row=4,column=0,sticky="E")
        self.sign_date_input.grid(row=4,column=1)

        self.sign_submit.grid(row=5,column=0,pady=20)
        self.sign_status.pack(side=tk.BOTTOM,fill=tk.X)

    def destroyroot(self):
        if messagebox.askyesno("Quit!","Do you want to quit?"):
            self.root.destroy()

    def createloginpage(self):
        self.destroyhomepage()
        self.loginpage = tk.Frame(
            self.root, width=self.sw // 2, height=self.sh - 200, borderwidth=5, relief=tk.GROOVE)
        self.ph = tk.Label(self.loginpage, bg="Cyan")

        self.BackButton = tk.Button(
            self.loginpage, text="\U0001F3E0", fg="Black", bg="Cyan", font="Arial 20 bold", relief=tk.SOLID, command=self.destroyloginpage,activebackground="Cyan")

        self.ll = tk.Label(self.loginpage, text="Login Form", fg="Black",
                           bg="Cyan", font="Arial 25 bold", borderwidth=2)  
                           
        self.lad = tk.Label(self.loginpage, text="Aadhare No. :",
                            fg="Black", font="Arial 10 bold", bg="Cyan")

        self.Ead = tk.Entry(self.loginpage, border=0,
                            borderwidth=2, textvariable=self.adh)

        self.Ead.bind("<Button-1>",lambda e: self.VirtualKey(self.alphabets,self.Ead ))

        self.Ead.delete(first=0,last=tk.END)

        self.submit = tk.Button(self.loginpage, text="Submit", font="Arial 10 bold",
                                bg="Blue", fg="white", relief=tk.GROOVE,command=self.validation) 
        self.submit.bind("<FocusIn>",self.validation)
        self.pack_loginpage()  # tempratue Entry

    def destroy_VirtualKey(self):
        if self.window is None:
            return None
        self.window.destroy()
        self.window =None

    def  VirtualKey(self, alphabets,w):
        self.w=w
        if self.window is not None:
            return None

        self.window = tk.Toplevel(self.root)
        self.window.protocol('WM_DELETE_WINDOW',
                             lambda : self.destroy_VirtualKey())
        self.window.config(background="black")
        self.vkdict=dict()
        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text in ('Enter', 'Shift'):
                    width = 20
                    columnspan = 2
                elif text == 'Space':
                    width = 100
                    columnspan = 16
                else:
                    width = 5
                    columnspan = 1
                self.vkdict[text]=tk.Button(self.window, text=text, width=width,
                          command=lambda value=text: self.insert(value),
                          padx=1, pady=1, bd=3, bg="black", fg="white"
                          )
                self.vkdict[text].grid(row=y, column=x, columnspan=columnspan,sticky="WE")
                
                x += columnspan
    def insert(self, value):
        try:
            if value.upper()== "BACKSPACE":
                self.w.delete(len(self.w.get())-1,last=tk.END)

            elif value.upper() == "SPACE":
                self.w.insert(tk.END, " ")

            elif value.upper() == "TAB":
                self.w.insert(tk.END, "\t")
         
            elif value.upper() == "ENTER":
                self.w.tk_focusNext().focus()
                self.w
                self.w =self.root.focus_get()

            elif value.upper() =="CAPSLK": 
                self.caplock= not self.caplock
                if self.caplock:
                    self.vkdict[value].config(text=value+"  \U000021E7")
                    for k,v in self.vkdict.items():
                        if len(k) == 1:
                            v.config(text=k.upper())
                else:
                    self.vkdict[value].config(text=value+"  \U000021E9")
                    for k,v in self.vkdict.items():
                        if len(k) == 1:
                            v.config(text=k.lower())    
            elif len(value)==1:
                if self.caplock:
                    self.w.insert(tk.END, value.upper())
                else:
                    self.w.insert(tk.END, value)
        except AttributeError:
            self.destroy_VirtualKey()


  
    def validation(self, e=None):
        self.controller.dict['adh'] = self.adh
        self.valid_adh()
        
    def valid_adh(self):
        if self.Invalid != None:
            self.Invalid.destroy()

        adh = self.adh.get()
        if not adh.isnumeric() or len(adh) != 12:
            if  not adh.isnumeric():
                self.Invalid = tk.Label(
                    self.loginpage, text="! Aadhaar must be Numerber", font="Arial 10 bold", bg="Cyan", fg="Red")
                self.Invalid.place(x=450, y=130)

            elif len(adh) != 12:
                self.Invalid = tk.Label(
                    self.loginpage, text="! Aadhaar must be of 12 digit", font="Arial 10 bold", bg="Cyan",fg="Red")
                self.Invalid.place(x=450, y=130)
            return None
        else:
            msg = self.controller.login_by_adh(self.adh.get())
        if msg==True:
            self.destroyloginpage()
            self.create_input_page()
        elif msg==False:
            messagebox.showerror("Login Error","You don't have account in SHMS!")
        else:
            messagebox.showerror("Unkown Error","Some unkow Error!")

        

    def create_input_page(self):
    
        self.inputframe = tk.Frame(self.root)
        self.inputcolor = tk.Label(self.inputframe,bg="Cyan")
        self.inputBack = tk.Button(self.inputframe, text="\U0001F3E0", fg="Black", bg="Cyan",font="Arial 20 bold", relief=tk.FLAT, command=self.destroyinputpage)

        self.inputstatus = tk.Label(self.inputframe, bg="White", fg="Red", font=("Helvetica 10 italic"))

        self.ll2 = tk.Label(self.inputframe, text="Temprature :",
                            fg="Black", font="Arial 10 bold", bg="Cyan")  # Temprature
        self.ll3 = tk.Label(self.inputframe, text="Blood Pressure :",
                            fg="Black", font="Arial 10 bold", bg="Cyan")  # Blood pressure
        self.ll4 = tk.Label(self.inputframe, text="Blood Sugar :",
                            fg="Black", font="Arial 10 bold", bg="Cyan")  # Blood pressure
        self.ll5 = tk.Label(self.inputframe, text="Pulse Rate :",
                            fg="Black", font="Arial 10 bold", bg="Cyan")  # Blood pressure

        self.Bl1 = tk.Button(self.inputframe, text=" ECG ", fg="White",
                            font="Arial 10 bold", relief=tk.GROOVE, bg="Blue")  # Blood pressure
        self.window =None
        self.El2 = tk.Entry(self.inputframe, textvariable=self.temp)
        self.El2.bind("<Button-1>", lambda e: self.VirtualKey(
            self.alphabets, self.El2))

        self.El3 = tk.Entry(self.inputframe, textvariable=self.bp)
        self.El3.bind("<Button-1>", lambda e: self.VirtualKey(
            self.alphabets, self.El3))

        self.El4 = tk.Entry(self.inputframe, textvariable=self.bs)
        self.El4.bind("<Button-1>", lambda e: self.VirtualKey(
            self.alphabets, self.El4))

        self.El5 = tk.Entry(self.inputframe,textvariable=self.pr)
        self.El5.bind("<Button-1>", lambda e: self.VirtualKey(
            self.alphabets, self.El5))

        self.El2.delete(first=0,last=tk.END)
        self.El3.delete(first=0,last=tk.END)
        self.El4.delete(first=0,last=tk.END)
        self.El5.delete(first=0,last=tk.END)
        self.inputsubmit = tk.Button(
            self.inputcolor, text="Submit", command=self.valid_temp, fg="White", bg="Blue")
        self.inputview = tk.Button(
            self.inputcolor, text="View Reports", command=self.viewdata,fg="White",bg="Blue")
        self.inputlable = tk.LabelFrame(self.inputframe,text="Reports",bd=0,font=self.font)
        
        self.my_tree = ttk.Treeview(self.inputlable)
        self.scroll_bar = ttk.Scrollbar(self.inputlable)
        self.my_tree.config(
            yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.my_tree.yview)

        self.my_tree["column"] = (
            "ID", "TEMPERATURE", "BP", "BS", "PR", "DATE", "TIME")
        self.my_tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.my_tree.column("ID", width=100, minwidth=100,
                            anchor=tk.CENTER, stretch=tk.NO)
        self.my_tree.column("TEMPERATURE", width=50,
                            minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("BP", width=40, minwidth=40, anchor=tk.CENTER)
        self.my_tree.column("BS", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("PR", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("DATE", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("TIME", width=50, minwidth=50, anchor=tk.CENTER)

        self.my_tree.heading("#0", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading(
            "TEMPERATURE", text="Temperature", anchor=tk.CENTER)
        self.my_tree.heading("BP", text="B.P", anchor=tk.CENTER)
        self.my_tree.heading("BS", text="B.S", anchor=tk.CENTER)
        self.my_tree.heading("PR", text="P.R", anchor=tk.CENTER)
        self.my_tree.heading("DATE", text="Date", anchor=tk.CENTER)
        self.my_tree.heading("TIME", text="Time", anchor=tk.CENTER)

        self.my_tree.tag_configure("oddrow", background="Red")
        self.my_tree.tag_configure("evenrow", background="crimson")

        self.my_tree.bind('<Button-1>', self.handle_click)
        
        self.pack_inputpage()

    def printf(self):
        print(self.temp.get())

    def pack_inputpage(self):
        self.inputframe.place(x=0,y=0,relheight=1,relwidth=1)
        self.inputcolor.place(x=0,y=0,relheight=1,relwidth=1)
        self.inputBack.place(x=0,y=0)
        self.inputstatus.pack(side=tk.BOTTOM,fill=tk.X)

        self.ll2.place(x=200, y=100)
        self.El2.place(x=320, y=100)

        self.ll3.place(x=200, y=130)
        self.El3.place(x=320, y=130)

        self.ll4.place(x=200, y=160)
        self.El4.place(x=320, y=160)

        self.ll5.place(x=200, y=190)
        self.El5.place(x=320, y=190)


        self.inputsubmit.place(x=320, y=220)
        self.Bl1.place(x=200, y=220)
        self.inputview.place(x=420,y=220)

        self.inputlable.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.scroll_bar.pack(fill=tk.Y,side=tk.RIGHT)
        self.my_tree.pack(fill=tk.BOTH,side=tk.BOTTOM)

    def destroyinputpage(self):
        self.create_hompepage()
        self.inputcolor.destroy()
        self.inputframe.destroy()
        self.inputBack.destroy()
        self.inputsubmit.destroy()
        self.ll2.destroy()
        self.El2.destroy()
        self.ll3.destroy()
        self.El3.destroy()
        self.ll4.destroy()
        self.El4.destroy()
        self.ll5.destroy()
        self.El5.destroy()
        self.Bl1.destroy()
        self.destroy_VirtualKey()

    def valid_temp(self):
        try:
            temp = self.temp.get()
        except Exception:
            self.inputstatus.config(text="Invalid Temperature!")
        else:
            self.valid_bp()

    def valid_bp(self):
        try:
            bp = self.bp.get()
        except Exception:
            self.inputstatus.config(text="Invalid Blood Pressure")
            return None
        else:
            self.valid_bs()

    def valid_bs(self):
        try:
            bs = self.bs.get()
        except Exception:
            self.inputstatus.config(text="Invalid Blood Sugar")
            return None
        else:
            self.valid_pr()

    def valid_pr(self):
        try:
            pr = self.pr.get()
        except Exception:
            self.inputstatus.config(text="Invalid Pulse Rate!")
            return None
        else:
            self.db_msg()


    def db_msg(self):   
        self.controller.dict["adh"]=self.adh
        self.controller.dict["temp"]=self.temp
        self.controller.dict["bp"]=self.bp
        self.controller.dict["bs"]=self.bs
        self.controller.dict["pr"]=self.pr
        msg = self.controller.save_data_to_db()
        print(msg)
        if msg == 1:
            messagebox.showinfo("Data Saved", "Data Saved Successfuly!")
            self.destroyinputpage()


    def destroyloginpage(self):
        self.create_hompepage()
        self.ll.destroy()
        self.BackButton.destroy()
        self.lad.destroy() 
        self.Ead.destroy()
        self.ph.destroy()
        self.submit.destroy()
        self.loginpage.destroy()
        if self.window is not None:
            self.window.destroy()
        self.window= None

    def pack_loginpage(self):
        self.loginpage.place(x=0, y=0, relheight=1, relwidth=1)
        self.ph.place(x=0, y=0, relheight=1, relwidth=1)
        self.ll.place(x=200, y=0)
        self.BackButton.place(x=1, y=1)

        self.lad.place(x=200, y=130)
        self.Ead.place(x=320, y=130)

        self.submit.place(x=200, y=180)

##############################    CREATING VIEW PAGE      ################################

    def createviewpage(self):
        self.destroyhomepage()
        self.Invalid=None
        self.mainframe = tk.Frame(self.root,)
        self.mainlabel1 = tk.Label(self.mainframe,bg="Yellow")
        self.mainframe1 = tk.Frame(self.mainframe)
        self.BackButton1 = tk.Button(
        self.mainframe, text="\U0001F3E0", fg="Black", bg="Yellow", font="Arial 20 bold", relief=tk.FLAT, command=self.destroyviewpage)

        self.identry = tk.Entry(self.mainframe,text="",textvariable=self.adh,font=self.font)
        self.identry.delete(first=0,last=tk.END)
        self.identry.bind("<Button-1>",lambda e: self.VirtualKey(self.alphabets, self.identry))
        self.lv1 = tk.Label(self.mainframe,text="Aadhaar No. :")

        self.idcheck = tk.Button(self.mainframe, text=" View ", borderwidth=3,fg="White", bg="Navyblue", relief=tk.RAISED,font=self.font, command=self.viewdata)
        self.idcheck.bind("<FocusIn>",self.viewdata)

       
        self.my_tree = ttk.Treeview(self.mainframe1)
        self.scroll_bar = ttk.Scrollbar(self.mainframe1)
        self.my_tree.config(
            yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.my_tree.yview)
        
        self.my_tree["column"] = ("ID","TEMPERATURE","BP","BS","PR","DATE","TIME")
        self.my_tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.my_tree.column("ID", width=100, minwidth=100, anchor=tk.CENTER,stretch=tk.NO)
        self.my_tree.column("TEMPERATURE", width=50, minwidth=50,anchor=tk.CENTER)
        self.my_tree.column("BP", width=40, minwidth=40, anchor=tk.CENTER)
        self.my_tree.column("BS", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("PR", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("DATE", width=50, minwidth=50, anchor=tk.CENTER)
        self.my_tree.column("TIME", width=50, minwidth=50, anchor=tk.CENTER)

        self.my_tree.heading("#0", anchor=tk.W)
        self.my_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.my_tree.heading("TEMPERATURE", text="Temperature", anchor = tk.CENTER)
        self.my_tree.heading("BP", text="B.P", anchor=tk.CENTER)
        self.my_tree.heading("BS", text="B.S", anchor=tk.CENTER)
        self.my_tree.heading("PR", text="P.R", anchor=tk.CENTER)
        self.my_tree.heading("DATE", text="Date", anchor=tk.CENTER)
        self.my_tree.heading("TIME", text="Time", anchor=tk.CENTER)

        self.my_tree.tag_configure("oddrow",background="Red")
        self.my_tree.tag_configure("evenrow",background="crimson")

        self.my_tree.bind('<Button-1>',self.handle_click)
        self.pack_viewpage()
    def handle_click(self,event):
        if self.my_tree.identify_region(event.x,event.y) == 'separator':
            return "break"

    def viewdata(self, e=0):
        adh = self.adh.get()
        if self.Invalid != None:
            self.Invalid.destroy()
        if not adh.isnumeric() or len(adh) != 12:
            if not adh.isnumeric():
                self.Invalid = tk.Label(
                    self.mainframe, text="! Invalid Aadhaar card Number", font="Arial 10 bold", bg="White", fg="Red")
                self.Invalid.place(x=100, y=0,relwidth=1)
            if len(adh) != 12:
                self.Invalid = tk.Label(
                    self.mainframe , text="! Aadhaar must be of 12 digit", font="Arial 10 bold", bg="Cyan", fg="Red")
                self.Invalid.place(x=100, y=0)
            for a in self.my_tree.get_children():
                self.my_tree.delete(a)
        else:
            data = self.controller.get_data_from_db(adh)
            if not data:
                messagebox.showerror("Invalid Aadhaar","Data Not present")
            else:
                for a in self.my_tree.get_children():
                    self.my_tree.delete(a)
                self.destroy_VirtualKey()
                for i,a in enumerate(data):
                    if i%2 ==0: 
                        self.my_tree.insert(parent='', index='end',
                                    iid=i, text="", values=a,tags=('evenrow',))
                    else:
                        self.my_tree.insert(parent='', index='end',
                                    iid=i, text="", values=a,tags=('oddrow',))
                
    # def showmessage(self,data)
    def destroyviewpage(self):
        self.create_hompepage()
        self.mainlabel1.destroy()
        self.BackButton1.destroy()
        self.mainframe.destroy()
        self.lv1.destroy()
        self.identry.destroy()
        self.idcheck.destroy()

        self.my_tree.destroy()
        self.scroll_bar.destroy()
        self.destroy_VirtualKey()


    def pack_viewpage(self):
        self.BackButton1.place(x=0, y=0)
        self.mainlabel1.place(x=0, y=0, relheight=1, relwidth=1)
        self.mainframe.place(x=0, y=0,relheight=1,relwidth=1)
        self.lv1.place(x=100, y=130)
        self.identry.place(x=200, y=130)
        self.idcheck.place(x=200, y=160)
        self.mainframe1.place(x=0,y=300,relwidth=1)
        # self.mainlabel.place(x=0, y=300, relwidth=1, relheight=1)
        # self.mainframelabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_tree.pack(fill=tk.BOTH,side=tk.BOTTOM)



    def pack_homepage(self):
        self.homepage.place(x=0, y=0, relheight=1, relwidth=1)
        self.bg.place(x=0, y=0, relheight=1, relwidth=1)
        self.l1.pack(side=tk.TOP,fill=tk.X)
        self.login.place(x=200, y=100)
        self.signup.place(x=300,y=100)
        self.view.place(x=400, y=100)
        self.Exit.place(x=550, y=500)

    def destroyhomepage(self):
        self.l1.destroy()
        self.homepage.destroy()

    def mainloop(self):
        self.root.mainloop()



App = Gui()
App.mainloop()
