from tkinter import *
from tkinter import messagebox

from controller.employee_controller import EmployeeController
from controller.service_controller import ServiceController
from controller.shift_controller import ShiftController
from tools.date_tool import DateTool
from tools.window_tool import WindowTool


class ShiftView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = ShiftController()
        self.employee_controller = EmployeeController()
        self.service_controller = ServiceController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "شیفت ها", self.back_click)

        # جدول شیفت ها (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 60), ("کارمند", 160), ("خدمت", 140), ("مبلغ", 90), ("مدت", 70), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("تاریخ بعدی", 110)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=9, command=self.table_click)

        # جدول کارمندان
        WindowTool.section(self.frame, "کارمندان (برای انتخاب کلیک کنید)", 570, 470, 500)
        employee_columns = [("شناسه", 60), ("نام", 110), ("نام خانوادگی", 130), ("خدمات", 200)]
        self.employee_table = WindowTool.table(self.frame, 570, 505, employee_columns, rows=6, command=self.employee_table_click)

        # جدول خدمات
        WindowTool.section(self.frame, "خدمات (برای انتخاب کلیک کنید)", 180, 470, 370)
        service_columns = [("شناسه", 60), ("عنوان خدمت", 200), ("مبلغ", 110)]
        self.service_table = WindowTool.table(self.frame, 180, 505, service_columns, rows=6, command=self.service_table_click)

        # جدول روزهای هفته
        WindowTool.section(self.frame, "روزهای هفته", 20, 470, 140)
        weekday_columns = [("روز هفته", 140)]
        self.weekday_table = WindowTool.table(self.frame, 20, 505, weekday_columns, rows=7, command=self.weekday_table_click)

        # فرم
        self.shift_id = StringVar(win)
        self.employee_id = StringVar(win)
        self.service_id = StringVar(win)
        self.weekday = StringVar(win)
        self.start_time = StringVar(win)
        self.end_time = StringVar(win)
        WindowTool.field(self.frame, "شناسه", self.shift_id, 80)
        WindowTool.field(self.frame, "شناسه کارمند", self.employee_id, 126)
        WindowTool.field(self.frame, "شناسه خدمت", self.service_id, 172)
        WindowTool.field(self.frame, "روز هفته", self.weekday, 218)
        WindowTool.field(self.frame, "ساعت شروع", self.start_time, 264)
        WindowTool.field(self.frame, "ساعت پایان", self.end_time, 310)

        WindowTool.button(self.frame, "ذخیره", 1380, 366, self.save_click, WindowTool.GREEN, width=85)
        WindowTool.button(self.frame, "ویرایش", 1285, 366, self.edit_click, WindowTool.BLUE, width=85)
        WindowTool.button(self.frame, "حذف", 1190, 366, self.remove_click, WindowTool.RED, width=85)
        WindowTool.button(self.frame, "جدید", 1095, 366, self.reset_from, WindowTool.GRAY, width=85)
        WindowTool.hint(self.frame, "ساعت را مثل 08:00 بنویسید", 416)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # فرم را ریست می کند، مجدد تمام اطلاعات را از فایل می خواند و در جدول ها نمایش می دهد
    def reset_from(self):
        self.shift_id.set(self.controller.next_id()[1])
        self.employee_id.set("")
        self.service_id.set("")
        self.weekday.set("")
        self.start_time.set("")
        self.end_time.set("")

        WindowTool.fill_table(self.table, self.controller.find_all_rows()[1])
        WindowTool.fill_table(self.employee_table, [row[:3] + (row[4],) for row in self.employee_controller.find_all_rows()[1]])
        WindowTool.fill_table(self.service_table, [(service.service_id, service.title, service.price) for service in self.service_controller.find_all()[1]])
        WindowTool.fill_table(self.weekday_table, [(weekday_name,) for weekday_name in DateTool.WEEKDAYS])

    # دکمه ذخیره فشرده شود
    def save_click(self):
        success, message = self.controller.save(
            self.shift_id.get(),
            self.employee_id.get(),
            self.service_id.get(),
            self.weekday.get(),
            self.start_time.get(),
            self.end_time.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه ویرایش فشرده شود
    def edit_click(self):
        success, message = self.controller.edit(
            self.shift_id.get(),
            self.employee_id.get(),
            self.service_id.get(),
            self.weekday.get(),
            self.start_time.get(),
            self.end_time.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه حذف فشرده شود
    def remove_click(self):
        success, message = self.controller.remove(self.shift_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # وقتی روی جدول شیفت ها کلیک کنیم اطلاعات را نمایش می دهد
    def table_click(self, event):
        selected_shift = WindowTool.selected(self.table)

        if selected_shift:
            success, shift = self.controller.find_by_id(selected_shift[0])
            if success:
                self.shift_id.set(shift.shift_id)
                self.employee_id.set(shift.employee_id)
                self.service_id.set(shift.service_id)
                self.weekday.set(DateTool.weekday_name(shift.weekday))
                self.start_time.set(shift.start_time)
                self.end_time.set(shift.end_time)

    # انتخاب کارمند از جدول
    def employee_table_click(self, event):
        selected_employee = WindowTool.selected(self.employee_table)

        if selected_employee:
            self.employee_id.set(selected_employee[0])

    # انتخاب خدمت از جدول
    def service_table_click(self, event):
        selected_service = WindowTool.selected(self.service_table)

        if selected_service:
            self.service_id.set(selected_service[0])

    # انتخاب روز هفته از جدول
    def weekday_table_click(self, event):
        selected_weekday = WindowTool.selected(self.weekday_table)

        if selected_weekday:
            self.weekday.set(selected_weekday[0])
