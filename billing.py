from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class billClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        self.cart_list=[]
        self.chk_print = 0

        #========= Variables =========
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        #======title======
        self.icon_title=PhotoImage(file="images/logo1.png")
        title = Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white" , anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #======btn_logout======
        btn_logout = Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2",command=self.logout).place(x=1150,y=10,height=50,width=150)

        #======clock======
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #============================== Product Frame ===============================
        productFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        productFrame1.place(x=6,y=110,width=410,height=550)

        productTitle=Label(productFrame1,text="All Product",font=("goudy old style",20,"bold"),bg="#c299d0",fg='white').pack(side=TOP,fill=X)

        # ====== Product Search Frame ======
        productFrame2 = Frame(productFrame1, bd=4, relief=RIDGE, bg="white")
        productFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search=Label(productFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(productFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(productFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btn_search=Button(productFrame2,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2",command=self.search).place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(productFrame2,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2",command=self.show).place(x=285,y=10,width=100,height=25)

        # ====== Product Details Frame ======
        productFrame3=Frame(productFrame1,bd=3,relief=RIDGE)
        productFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(productFrame3,orient=VERTICAL)
        scrollx=Scrollbar(productFrame3,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(productFrame3,column=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid" , text="PID")
        self.productTable.heading("name" , text="Name")
        self.productTable.heading("price" , text="Price")
        self.productTable.heading("qty" , text="Quantity")
        self.productTable.heading("status" , text="Status")
        self.productTable["show"]="headings"

        self.productTable.column("pid", width=40)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=80)
        self.productTable.column("qty", width=80)
        self.productTable.column("status", width=70)
        self.productTable.pack(fill=BOTH,expand=1)

        self.productTable.bind("<ButtonRelease-1>",self.get_data)

        lbl_note = Label(productFrame1,text="NOTE: 'Enter 0 QTY to Remove the Product from Cart'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

        # ========================== Customer Frame ==========================
        customerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customerFrame.place(x=420, y=110, width=530, height=70)

        customerTitle=Label(customerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name = Label(customerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(customerFrame, textvariable=self.var_cname, font=("times new roman", 13),bg="lightyellow").place(x=70, y=35, width=180)
        lbl_contact = Label(customerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=260, y=35)
        txt_contact = Entry(customerFrame, textvariable=self.var_contact, font=("times new roman", 13),bg="lightyellow").place(x=360, y=35, width=160)

        # ========== Calculator Cart Frame ==========
        cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_Frame.place(x=420, y=190, width=530, height=360)

        # ========== Calculator Frame ==========
        self.var_cal_input = StringVar()

        cal_Frame = Frame(cal_cart_Frame, bd=7, relief=RIDGE, bg="gray")
        cal_Frame.place(x=5, y=10, width=270, height=340)

        txt_cal_input = Entry(cal_Frame,textvariable=self.var_cal_input,font=("arial",15,"bold"),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)


        btn_7 = Button(cal_Frame,text='7',font=("arial",15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8 = Button(cal_Frame,text='8',font=("arial",15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9 = Button(cal_Frame,text='9',font=("arial",15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum = Button(cal_Frame,text="+",font=("arial",15,"bold"),command=lambda:self.get_input("+"),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4 = Button(cal_Frame, text='4', font=("arial", 15, "bold"),command=lambda:self.get_input(4), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(cal_Frame, text='5', font=("arial", 15, "bold"),command=lambda:self.get_input(5), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=1)
        btn_5 = Button(cal_Frame, text='6', font=("arial", 15, "bold"),command=lambda:self.get_input(6), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(cal_Frame, text="-", font=("arial", 15, "bold"),command=lambda:self.get_input('-'), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(cal_Frame, text='1', font=("arial", 15, "bold"),command=lambda:self.get_input(1), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(cal_Frame, text='2', font=("arial", 15, "bold"),command=lambda:self.get_input(2), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(cal_Frame, text='3', font=("arial", 15, "bold"),command=lambda:self.get_input(3), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(cal_Frame, text="*", font=("arial", 15, "bold"),command=lambda:self.get_input('*'), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(cal_Frame, text='0', font=("arial", 15, "bold"),command=lambda:self.get_input(0), bd=5, width=4, pady=17, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(cal_Frame, text='C', font=("arial", 15, "bold"),command=self.clear_cal, bd=5, width=4, pady=17, cursor="hand2").grid(row=4, column=1)
        btn_div = Button(cal_Frame, text="/", font=("arial", 15, "bold"),command=lambda:self.get_input('/'), bd=5, width=4, pady=17, cursor="hand2").grid(row=4, column=2)
        btn_eq = Button(cal_Frame, text='=', font=("arial", 15, "bold"),command=self.equal_cal,bg="lightgreen", bd=5, width=4, pady=17, cursor="hand2").grid(row=4, column=3)



        # ========== Cart Frame ==========
        cart_Frame = Frame(cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)

        self.cartTitle = Label(cart_Frame,text="Cart: \t Total Product [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.cartTable = ttk.Treeview(cart_Frame, column=("pid", "name", "price", "qty"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
        self.cartTable.heading("pid", text="PID")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Quantity")
        self.cartTable["show"] = "headings"

        self.cartTable.column("pid", width=40)
        self.cartTable.column("name", width=100)
        self.cartTable.column("price", width=80)
        self.cartTable.column("qty", width=80)
        self.cartTable.pack(fill=BOTH, expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        # ========== Add Cart Buttons ==========
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()


        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(x=210,y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),bg="lightyellow", state="readonly").place(x=210, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=375, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),bg="lightyellow").place(x=375, y=35, width=144, height=22)

        self.lbl_instock = Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame,text="Clear",font=("times new roman",15,"bold"),bg="#3CC3A5",cursor="hand2",command=self.clear_cart).place(x=180,y=70,width=150,height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame,text="Add | Update Cart",font=("times new roman",15,"bold"),bg="orange",cursor="hand2",command=self.add_update_cart).place(x=340,y=70,width=180,height=30)

        # ==================== billing area ===================
        billFrame = Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=410,height=410)

        billTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="red",fg='white').pack(side=TOP,fill=X)
        scrolly = Scrollbar(billFrame , orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area = Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ==== Billing Buttons ====
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amnt = Label(billMenuFrame,text="Bill Amount\n0",font=("goudy old style",14,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[5%]", font=("goudy old style", 15, "bold"),bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Amount\n0", font=("goudy old style", 15, "bold"),bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text="Print", font=("goudy old style", 15, "bold"),bg="#ffb8b1", fg="white",cursor="hand2",command = self.print_bill)
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Clear All", font=("goudy old style", 15, "bold"),bg="gray", fg="white",cursor="hand2",command=self.clear_all)
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Generate/Save Bill", font=("goudy old style", 13, "bold"), bg="#009688",fg="white",cursor="hand2",command=self.generate_bill)
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ======footer======
        lbl_footer = Label(self.root,text="IMS:- Inventory Management System || Developed By Vaibhav Jain \nFor any Technical Issue Contact: xxxxxxxxxx ",font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        self.show()
        self.update_date_time()

    # ============================ ALL FUNCTION ===============================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set("")

    def equal_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):              # product ttk show
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())  # delete from ttk
            for row in rows:
                self.productTable.insert('',END,values=row)
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}" , parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Input should be required ", parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error","No record found !!!",parent=self.root)
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self,event):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        #self.var_search.set(row[1])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,event):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
        elif self.var_qty.get()=="":
            messagebox.showerror("Error","Quantity Is Required",parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error",f"Invalid Quantity \nWe have only {self.var_stock.get()} Products",parent=self.root)
        else:
            # price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))
            price_cal = self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            # ====== Update Cart ====
            present = "no"
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_+=1
            if present == "yes":
                op = messagebox.askyesno("Confirm","Product already present\nDo you want to want to Update | Remove from the Cart List",parent=self.root)
                if op == True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2])*int(row[3]))
        self.discount = (self.bill_amnt*5)/100
        self.net_pay = self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amount\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Amount\n[{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart:\tTotal Product [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())  # delete from ttk
            for row in self.cart_list:
                self.cartTable.insert('',END,values=row)
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}" , parent=self.root)

    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error", f"Customer Details are required" , parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please Add Product to the Cart !!!" , parent=self.root)
        else:
            # ====== Bill Top =======
            self.bill_top()
            # ====== Bill Middle =======
            self.bill_middle()
            # ====== Bill Bottom =======
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill ha been generated",parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%y"))
        bill_top_temp =f'''
\t\t  XYZ-Inventory
\t Phone No 98725***** , Delhi-125001
{str("="*47)}
 customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()}\t\t\tTime: {str(time.strftime("%I:%M:%S"))}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%y"))}
{str("="*47)}
 Product Name\t\t\tQty\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name = row[1]
                qty = int(row[4])-int(row[3]) # row[4] is a stock, we assign the stock also in to the cart table but we don't show the user
                if int(row[3])==int(row[4]):
                    status = 'Inactive'
                if int(row[3])!=int(row[4]):
                    status = 'Active'
                price = float(row[2])*int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                # ====== Update Quantity In Product Table ======
                cur.execute('Update product set qty=?,status=? where pid=?', (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}" , parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Amount\t\t\t\tRs.{self.net_pay}
{str("="*47)}
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart:\tTotal Product [0]")
        self.var_search.set('')
        self.chk_print = 0
        self.clear_cart()
        self.show()
        self.show_cart()

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror('Print',"Please generatre bill, to print the receipt",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')


    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def logout(self):
        self.root.destroy()
        os.system(("python login.py"))


if __name__=="__main__":
    root = Tk()
    object=billClass(root)
    root.mainloop()