from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
class Login_System:
    def __init__(self,root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp=''
        # ====== images ======
        self.phone_image = ImageTk.PhotoImage(file="Images/phone.png")
        self.lbl_Phone_image = Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        # ======== Login Frame 1 =======
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame= Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee Id",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_password=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login = Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",font=("times new roman",15,"bold"),bg="white",fg="lightgray").place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E",command=self.forget).place(x=100,y=390)

        # ===== Frame 2 =====
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        # ====== Animation Images =======
        self.im1=ImageTk.PhotoImage(file="Images/im1.png")
        self.im2=ImageTk.PhotoImage(file="Images/im2.png")
        self.im3=ImageTk.PhotoImage(file="Images/im3.png")

        self.lbl_change_image = Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()
# ============================== All Function ========================
    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? and pass=?",(self.employee_id.get(),self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error","Invalid Username/Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def forget(self):
        con = sqlite3.connect(database=r"ims.db")
        cur = con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                else:
                    # ===== Forget Window =====
                    self.var_otp = StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    # ====== call send email function
                    chk=self.send_email(email[0])
                    if chk=="failed":
                        messagebox.showerror(("Error","Connection Error,try again"),parent=self.root)
                    else:
                        self.forget_window = Toplevel(self.root)
                        self.forget_window.title('RESET PASSWORD')
                        self.forget_window.geometry('400x350+500+100')
                        self.forget_window.focus_force()

                        title=Label(self.forget_window,text='Reset Password',font=('goudy old style',15,'bold'),bg="#3f51b5",fg='white').pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_window,text="Enter OTP Sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_window,textvariable=self.var_otp,font=("times new roman",15),bg='lightyellow').place(x=20,y=100,width=250,height=30)

                        self.btn_reset = Button(self.forget_window,text="Submit",font=("times new roman",15),bg='lightblue',command=self.validate_otp)
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass = Label(self.forget_window, text="New Password",font=("times new roman", 15)).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_window, textvariable=self.var_new_pass, font=("times new roman", 15),bg='lightyellow').place(x=20, y=190, width=250, height=30)

                        lbl_conf_pass = Label(self.forget_window, text="Confirm Password",font=("times new roman", 15)).place(x=20, y=225)
                        txt_conf_pass = Entry(self.forget_window, textvariable=self.var_conf_pass, font=("times new roman", 15),bg='lightyellow').place(x=20, y=255, width=250, height=30)

                        self.btn_update = Button(self.forget_window, text="Update",state=DISABLED, font=("times new roman", 15), bg='lightblue',command=self.update_password)
                        self.btn_update.place(x=20, y=300, width=100, height=30)

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_window)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","Confirm Password must be same",parent=self.forget_window)
        else:
            con = sqlite3.connect(database=r"ims.db")
            cur = con.cursor()
            try:
                cur.execute("Update employee set pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password Update Successfully", parent=self.forget_window)
                self.forget_window.destroy()
            except EXCEPTION as ex:
                messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, try again",parent=self.forget_window)


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587) # 587 port no. for email
        s.starttls()  # use for encription
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_,pass_)

        self.otp = int(time.strftime("%H%S%M"))+int(time.strftime("%d%m%Y"))
        subject = 'IMS-Reset Password OTP'
        message = f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
        message = "Subject:{}\n\n{}".format(subject,message)
        s.sendmail(email_,to_,message)
        chk=s.ehlo()
        if chk[0]==250:
            return 'successfull submitted'
        else:
            return 'failed'




root = Tk()
obj = Login_System(root)
root.mainloop()
