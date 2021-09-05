from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk,messagebox
import sqlite3
class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        #self.root.focus_force()
        #=====================================
        #========== variables ==========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.cat_list = []
        self.fetch_cat()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()



        product_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        # ====== title ======
        title = Label(product_Frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP , fill=X)

        # ====== Column 1
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30,y=60)
        lbl_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30,y=110)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30,y=160)
        lbl_quantity = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30,y=210)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30,y=260)

        # ====== Column 2
        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,values=self.cat_list, state='readonly', justify=CENTER,font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=110, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=160, width=200)
        txt_quantity = Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=210, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active" , "Inactive"), state='readonly' , justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=260, width=200)
        cmb_status.current(0)

        # ===buttons===
        btn_add = Button(product_Frame , text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2" , command=self.add).place(x=10, y=350, width=100, height=40)
        btn_update = Button(product_Frame , text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white",cursor="hand2" , command=self.update).place(x=120, y=350, width=100, height=40)
        btn_delete = Button(product_Frame , text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white",cursor="hand2" , command=self.delete).place(x=230, y=350, width=100, height=40)
        btn_clear = Button(product_Frame , text="Clear", font=("goudy old style", 15), bg="#607d8b", fg="white",cursor="hand2" , command=self.clear).place(x=340, y=350, width=100, height=40)

        #======SearchFrame======
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        # ======option======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2",command=self.search).place(x=410,y=9,width=150,height=30)

        # ====== Product Details ======
        prod_frame = Frame(self.root, bd=3, relief=RIDGE)
        prod_frame.place(x=480, y=100,width=600, height=390)

        scrolly = Scrollbar(prod_frame, orient=VERTICAL)
        scrollx = Scrollbar(prod_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(prod_frame, column=("pid", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid", text="P Id")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Quantity")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=90)
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
# ========================= ========== =========================
    def fetch_cat(self):
        self.cat_list.append("Empty")
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()

            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This product already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into product (Category, name, price, qty, status) values(?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.show()
        except EXCEPTION as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}" , parent=self.root)

    def get_data(self,event):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.var_status.set(row[5])

    def update(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error","Please select product from list " , parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product " , parent=self.root)
                else:
                    cur.execute("Update product set Category=?, name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.show()
        except EXCEPTION as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}" ,parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select product from the list ",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product" , parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do yoy want to delete?",parent=self.root)
                    if op == True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error","Select By option",parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Input should be required ", parent=self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error","No record found !!!",parent=self.root)
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    object=productClass(root)
    root.mainloop()