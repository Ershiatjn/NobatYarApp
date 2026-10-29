from tkinter import *
from tkinter import messagebox

from controller.employee_controller import EmployeeController
from controller.service_controller import ServiceController
from tools.window_tool import WindowTool


class EmployeeView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = EmployeeController()
        self.service_controller = ServiceController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "کارمندان", self.back_click)

        # جدول کارمندان (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 60), ("نام", 120), ("نام خانوادگی", 150), ("شناسه خدمات", 120), ("خدمات", 500)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=10, command=self.table_click)

        # جدول خدمات (با کلیک روی هر خدمت شناسه آن به خدمات کارمند اضافه می شود)
        WindowTool.section(self.frame, "خدمات موجود (برای افزودن به کارمند روی خدمت کلیک کنید)", 20, 380, 950)
        service_columns = [("شناسه", 90), ("عنوان خدمت", 500), ("مبلغ (تومان)", 360)]
        self.service_table = WindowTool.table(self.frame, 20, 415, service_columns, rows=8, command=self.service_table_click)

        # فرم
        self.employee_id = StringVar(win)
        self.name = StringVar(win)
        self.family = StringVar(win)
        self.service_ids = StringVar(win)
        WindowTool.field(self.frame, "شناسه", self.employee_id, 80)
        WindowTool.field(self.frame, "نام", self.name, 134)
        WindowTool.field(self.frame, "نام خانوادگی", self.family, 188)
        WindowTool.field(self.frame, "شناسه خدمات", self.service_ids, 242)

        WindowTool.button(self.frame, "ذخیره", 1380, 310, self.save_click, WindowTool.GREEN)
        WindowTool.button(self.frame, "ویرایش", 1180, 310, self.edit_click, WindowTool.BLUE)
        WindowTool.button(self.frame, "حذف", 1380, 360, self.remove_click, WindowTool.RED)
        WindowTool.button(self.frame, "فرم جدید", 1180, 360, self.reset_from, WindowTool.GRAY)
        WindowTool.hint(self.frame, "شناسه خدمات را با ویرگول جدا کنید (مثل 1,2) یا از جدول خدمات انتخاب کنید", 420, 60)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # فرم را ریست می کند، مجدد تمام اطلاعات را از فایل می خواند و در جدول ها نمایش می دهد
    def reset_from(self):
        self.employee_id.set(self.controller.next_id()[1])
        self.name.set("")
        self.family.set("")
        self.service_ids.set("")

        WindowTool.fill_table(self.table, self.controller.find_all_rows()[1])
        WindowTool.fill_table(self.service_table, [(service.service_id, service.title, service.price) for service in self.service_controller.find_all()[1]])

    # دکمه ذخیره فشرده شود
    def save_click(self):
        success, message = self.controller.save(
            self.employee_id.get(),
            self.name.get(),
            self.family.get(),
            self.service_ids.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه ویرایش فشرده شود
    def edit_click(self):
        success, message = self.controller.edit(
            self.employee_id.get(),
            self.name.get(),
            self.family.get(),
            self.service_ids.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه حذف فشرده شود
    def remove_click(self):
        success, message = self.controller.remove(self.employee_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # وقتی روی جدول کارمندان کلیک کنیم اطلاعات را نمایش می دهد
    def table_click(self, event):
        selected_employee = WindowTool.selected(self.table)

        if selected_employee:
            success, employee = self.controller.find_by_id(selected_employee[0])
            if success:
                self.employee_id.set(employee.employee_id)
                self.name.set(employee.name)
                self.family.set(employee.family)
                self.service_ids.set(",".join(str(service_id) for service_id in employee.service_ids))

    # وقتی روی جدول خدمات کلیک کنیم شناسه خدمت به فهرست اضافه می شود
    def service_table_click(self, event):
        selected_service = WindowTool.selected(self.service_table)

        if selected_service:
            service_id = str(selected_service[0])
            current_list = [item.strip() for item in self.service_ids.get().replace("،", ",").split(",") if item.strip() != ""]
            if service_id not in current_list:
                current_list.append(service_id)
            self.service_ids.set(",".join(current_list))
