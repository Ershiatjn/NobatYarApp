from tkinter import *
from tkinter import messagebox

from controller.appointment_controller import AppointmentController
from tools.window_tool import WindowTool


class CancelView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = AppointmentController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "نوبت های لغو شده", self.back_click)

        # جدول نوبت های لغو شده (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 60), ("مشتری", 160), ("کارمند", 150), ("خدمت", 130), ("تاریخ", 100), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("مبلغ", 90)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=18, command=self.table_click)

        # حذف دائمی نوبت انتخاب شده
        self.appointment_id = StringVar(win)
        WindowTool.field(self.frame, "شناسه نوبت", self.appointment_id, 80, readonly=True)
        WindowTool.button(self.frame, "حذف دائمی", 1380, 134, self.remove_click, WindowTool.RED, width=380)
        WindowTool.hint(self.frame, "برای حذف دائمی، یک نوبت را از جدول انتخاب کنید", 190, 50)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # مجدد تمام نوبت های لغو شده را از فایل می خواند و در جدول نمایش می دهد
    def reset_from(self):
        self.appointment_id.set("")

        WindowTool.fill_table(self.table, self.controller.find_canceled_rows()[1])

    # دکمه حذف دائمی فشرده شود
    def remove_click(self):
        if self.appointment_id.get() == "":
            messagebox.showerror("خطا", "ابتدا یک نوبت را از جدول انتخاب کنید")
        else:
            success, message = self.controller.remove(self.appointment_id.get())

            if success:
                messagebox.showinfo("موفق", message)
                self.reset_from()
            else:
                messagebox.showerror("خطا", message)

    # وقتی روی جدول کلیک کنیم شناسه نوبت انتخاب می شود
    def table_click(self, event):
        selected_appointment = WindowTool.selected(self.table)

        if selected_appointment:
            self.appointment_id.set(selected_appointment[0])
