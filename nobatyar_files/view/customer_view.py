from tkinter import *
from tkinter import messagebox

from controller.customer_controller import CustomerController
from tools.window_tool import WindowTool


class CustomerView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = CustomerController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "مشتریان", self.back_click)

        # جدول (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 90), ("نام", 250), ("نام خانوادگی", 300), ("شماره موبایل", 310)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=18, command=self.table_click)

        # فرم
        self.customer_id = StringVar(win)
        self.name = StringVar(win)
        self.family = StringVar(win)
        self.phone = StringVar(win)
        WindowTool.field(self.frame, "شناسه", self.customer_id, 80)
        WindowTool.field(self.frame, "نام", self.name, 134)
        WindowTool.field(self.frame, "نام خانوادگی", self.family, 188)
        WindowTool.field(self.frame, "شماره موبایل", self.phone, 242)

        WindowTool.button(self.frame, "ذخیره", 1380, 310, self.save_click, WindowTool.GREEN)
        WindowTool.button(self.frame, "ویرایش", 1180, 310, self.edit_click, WindowTool.BLUE)
        WindowTool.button(self.frame, "حذف", 1380, 360, self.remove_click, WindowTool.RED)
        WindowTool.button(self.frame, "فرم جدید", 1180, 360, self.reset_from, WindowTool.GRAY)
        WindowTool.hint(self.frame, "شماره موبایل مثل 09121234567 نوشته شود", 420, 50)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # فرم را ریست می کند، مجدد تمام مشتریان را از فایل می خواند و در جدول نمایش می دهد
    def reset_from(self):
        self.customer_id.set(self.controller.next_id()[1])
        self.name.set("")
        self.family.set("")
        self.phone.set("")

        WindowTool.fill_table(self.table, [customer.to_tuple() for customer in self.controller.find_all()[1]])

    # دکمه ذخیره فشرده شود
    def save_click(self):
        success, message = self.controller.save(
            self.customer_id.get(),
            self.name.get(),
            self.family.get(),
            self.phone.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه ویرایش فشرده شود
    def edit_click(self):
        success, message = self.controller.edit(
            self.customer_id.get(),
            self.name.get(),
            self.family.get(),
            self.phone.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه حذف فشرده شود
    def remove_click(self):
        success, message = self.controller.remove(self.customer_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # وقتی روی جدول کلیک کنیم اطلاعات را نمایش می دهد
    def table_click(self, event):
        selected_customer = WindowTool.selected(self.table)

        if selected_customer:
            success, customer = self.controller.find_by_id(selected_customer[0])
            if success:
                self.customer_id.set(customer.customer_id)
                self.name.set(customer.name)
                self.family.set(customer.family)
                self.phone.set(customer.phone)
