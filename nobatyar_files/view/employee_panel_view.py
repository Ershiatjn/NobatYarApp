from tkinter import *

from controller.appointment_controller import AppointmentController
from controller.employee_controller import EmployeeController
from controller.shift_controller import ShiftController
from tools.window_tool import WindowTool


# بخش کارمند: کارمند خودش را انتخاب می کند و شیفت ها و نوبت های خودش را می بیند
class EmployeePanelView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = EmployeeController()
        self.shift_controller = ShiftController()
        self.appointment_controller = AppointmentController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "بخش کارمند", self.back_click)

        # جدول کارمندان
        WindowTool.section(self.frame, "کارمند خود را انتخاب کنید", 1030, 65, 350)
        columns = [("شناسه", 60), ("نام", 130), ("نام خانوادگی", 160)]
        self.table = WindowTool.table(self.frame, 1030, 100, columns, rows=6, command=self.table_click)

        # جدول شیفت های کارمند
        WindowTool.section(self.frame, "شیفت های من", 20, 65, 880)
        shift_columns = [("شناسه", 60), ("کارمند", 160), ("خدمت", 140), ("مبلغ", 90), ("مدت", 70), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("تاریخ بعدی", 110)]
        self.shift_table = WindowTool.table(self.frame, 20, 100, shift_columns, rows=6)

        # جدول نوبت های کارمند
        WindowTool.section(self.frame, "نوبت های فعال من", 20, 335, 940)
        appointment_columns = [("شناسه", 60), ("مشتری", 160), ("کارمند", 150), ("خدمت", 130), ("تاریخ", 100), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("مبلغ", 90)]
        self.appointment_table = WindowTool.table(self.frame, 20, 370, appointment_columns, rows=10)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # جدول ها را خالی می کند و مجدد کارمندان را از فایل می خواند و نمایش می دهد
    def reset_from(self):
        WindowTool.fill_table(self.table, [employee.to_tuple()[:3] for employee in self.controller.find_all()[1]])
        WindowTool.fill_table(self.shift_table, [])
        WindowTool.fill_table(self.appointment_table, [])

    # وقتی روی جدول کلیک کنیم شیفت ها و نوبت های آن کارمند نمایش داده می شود
    def table_click(self, event):
        selected_employee = WindowTool.selected(self.table)

        if selected_employee:
            WindowTool.fill_table(self.shift_table, self.shift_controller.find_rows_by_employee(selected_employee[0])[1])
            WindowTool.fill_table(self.appointment_table, self.appointment_controller.find_rows_by_employee(selected_employee[0])[1])
