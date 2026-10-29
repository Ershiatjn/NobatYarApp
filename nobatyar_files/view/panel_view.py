from tkinter import *

from tools.window_tool import WindowTool
from view import *


class PanelView:
    def __init__(self):
        self.win = WindowTool.create_window("نوبت یار")
        self.show()
        self.win.mainloop()

    # صفحه ی اصلی برنامه را نمایش می دهد
    def show(self):
        self.frame = WindowTool.frame(self.win)
        WindowTool.header(self.frame, "نوبت یار - سیستم نوبت دهی")

        WindowTool.button(self.frame, "بخش مدیریت", 910, 200, self.admin_click, WindowTool.BLUE, width=420, height=56)
        WindowTool.button(self.frame, "بخش کارمند", 910, 276, self.employee_click, WindowTool.GREEN, width=420, height=56)
        WindowTool.button(self.frame, "بخش مشتری", 910, 352, self.customer_click, WindowTool.GRAY, width=420, height=56)

    def admin_click(self):
        self.frame.destroy()
        admin_ui = AdminPanelView(self.win, self.show)

    def employee_click(self):
        self.frame.destroy()
        employee_ui = EmployeePanelView(self.win, self.show)

    def customer_click(self):
        self.frame.destroy()
        customer_ui = CustomerPanelView(self.win, self.show)
