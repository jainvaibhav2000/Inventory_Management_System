from tkinter import *
from PIL import ImageTk
from employee import employeeClass
from category import categoryClass
from product import productClass
from sales import salesClass
from tkinter import messagebox
import sqlite3
import time
import os
class IMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        #======title======
        self.icon_title=PhotoImage(file="images/logo1.png")
        title = Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white" , anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #======btn_logout======
        btn_logout = Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2",command=self.logout).place(x=1150,y=10,height=50,width=150)

        #======clock======
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #======Left Menu======
        self.MenuLogo = ImageTk.PhotoImage(file="images/menu_im.png")

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=520)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side = PhotoImage(file = "images/side.png")
        lbl_menu = Button(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688",command=self.menu).pack(side=TOP,fill=X)

        btn_employee = Button(LeftMenu,text="Employee",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",command=self.employee).pack(side=TOP,fill=X)
        # btn_suplier = Button(LeftMenu,text="Supplier",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category = Button(LeftMenu,text="Category",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2" , command=self.category).pack(side=TOP,fill=X)
        btn_product = Button(LeftMenu,text="Product",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2" , command=self.product).pack(side=TOP,fill=X)
        btn_sales = Button(LeftMenu,text="Sales",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2" , command=self.sales).pack(side=TOP,fill=X)
        btn_exit = Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor='w',font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        # ======content======
        self.lbl_employee = Button(self.root, text="Total Employee\n [ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9",fg="white", font=("goudy old style", 20, "bold"),command = self.employee)
        self.lbl_employee.place(x=250, y=120, height=150, width=300)

        self.lbl_category = Button(self.root, text="Total Category\n [ 0 ]", bd=5, relief=RIDGE, bg="#009677",fg="white", font=("goudy old style", 20, "bold"), command=self.category)
        self.lbl_category.place(x=600, y=120, height=150, width=300)

        self.lbl_product = Button(self.root, text="Total Product\n [ 0 ]", bd=5, relief=RIDGE, bg="#607d8b",fg="white", font=("goudy old style", 20, "bold"), command=self.product)
        self.lbl_product.place(x=950, y=120, height=150, width=300)

        self.lbl_sales = Button(self.root, text="Total Sales\n [ 0 ]", bd=5, relief=RIDGE, bg="#ffc107",fg="white", font=("goudy old style", 20, "bold"), command=self.sales)
        self.lbl_sales.place(x=250, y=300, height=150, width=300)

        # ======footer======
        lbl_footer = Label(self.root,text="IMS:- Inventory Management System || Developed By Vaibhav Jain \nFor any Technical Issue Contact: xxxxxxxxxx ",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()

    def menu(self):
        self.root.destroy()
        os.system("python dashboard.py")

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n [ {str(len(employee))} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n [ {str(len(category))} ]")

            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n [ {str(len(product))} ]")

            self.lbl_sales.config(text=f"Total Sales\n [ {str(len(os.listdir('bill')))} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200, self.update_content)

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")




if __name__=="__main__":
    root = Tk()
    object=IMS(root)
    root.mainloop()