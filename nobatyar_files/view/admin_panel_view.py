from tkinter import *

from tools.window_tool import WindowTool
from view import *


# بخش مدیریت: مدیر اصلی سیستم (بدون نام کاربری و رمز عبور)
class AdminPanelView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.show()

    # منوی بخش مدیریت را نمایش می دهد
    def show(self):
        self.frame = WindowTool.frame(self.win)
        WindowTool.header(self.frame, "بخش مدیریت", self.back_click)

        WindowTool.button(self.frame, "خدمات", 910, 120, self.services_click, WindowTool.BLUE, width=420, height=56)
        WindowTool.button(self.frame, "کارمندان", 910, 196, self.employees_click, WindowTool.BLUE, width=420, height=56)
        WindowTool.button(self.frame, "مشتریان", 910, 272, self.customers_click, WindowTool.BLUE, width=420, height=56)
        WindowTool.button(self.frame, "شیفت ها", 910, 348, self.shifts_click, WindowTool.BLUE, width=420, height=56)
        WindowTool.button(self.frame, "نوبت ها", 910, 424, self.appointments_click, WindowTool.GREEN, width=420, height=56)
        WindowTool.button(self.frame, "نوبت های لغو شده", 910, 500, self.cancels_click, WindowTool.RED, width=420, height=56)

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    def services_click(self):
        self.frame.destroy()
        service_ui = ServiceView(self.win, self.show)

    def employees_click(self):
        self.frame.destroy()
        employee_ui = EmployeeView(self.win, self.show)

    def customers_click(self):
        self.frame.destroy()
        customer_ui = CustomerView(self.win, self.show)

    def shifts_click(self):
        self.frame.destroy()
        shift_ui = ShiftView(self.win, self.show)

    def appointments_click(self):
        self.frame.destroy()
        appointment_ui = AppointmentView(self.win, self.show)

    def cancels_click(self):
        self.frame.destroy()
        cancel_ui = CancelView(self.win, self.show)
