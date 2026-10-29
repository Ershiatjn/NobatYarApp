from tkinter import *
from tkinter import messagebox

from controller.appointment_controller import AppointmentController
from controller.customer_controller import CustomerController
from controller.shift_controller import ShiftController
from tools.window_tool import WindowTool


class AppointmentView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = AppointmentController()
        self.customer_controller = CustomerController()
        self.shift_controller = ShiftController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "نوبت ها", self.back_click)

        # جدول نوبت های فعال (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 60), ("مشتری", 160), ("کارمند", 150), ("خدمت", 130), ("تاریخ", 100), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("مبلغ", 90)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=8, command=self.table_click)

        # جدول مشتریان
        WindowTool.section(self.frame, "مشتریان (برای انتخاب کلیک کنید)", 1010, 470, 370)
        customer_columns = [("شناسه", 50), ("نام", 90), ("نام خانوادگی", 110), ("شماره موبایل", 120)]
        self.customer_table = WindowTool.table(self.frame, 1010, 505, customer_columns, rows=7, command=self.customer_table_click)

        # جدول شیفت ها
        WindowTool.section(self.frame, "شیفت ها (برای انتخاب کلیک کنید)", 210, 470, 730)
        shift_columns = [("شناسه", 50), ("کارمند", 130), ("خدمت", 110), ("مبلغ", 70), ("مدت", 60), ("روز هفته", 80), ("از ساعت", 65), ("تا ساعت", 65), ("تاریخ بعدی", 100)]
        self.shift_table = WindowTool.table(self.frame, 210, 505, shift_columns, rows=7, command=self.shift_table_click)

        # جدول ساعت های آزاد
        WindowTool.section(self.frame, "ساعت های آزاد", 20, 470, 170)
        slot_columns = [("از ساعت", 85), ("تا ساعت", 85)]
        self.slot_table = WindowTool.table(self.frame, 20, 505, slot_columns, rows=7, command=self.slot_table_click)

        # فرم
        self.appointment_id = StringVar(win)
        self.customer_id = StringVar(win)
        self.shift_id = StringVar(win)
        self.date = StringVar(win)
        self.start_time = StringVar(win)
        WindowTool.field(self.frame, "شناسه نوبت", self.appointment_id, 80)
        WindowTool.field(self.frame, "شناسه مشتری", self.customer_id, 126)
        WindowTool.field(self.frame, "شناسه شیفت", self.shift_id, 172)
        WindowTool.field(self.frame, "تاریخ (شمسی)", self.date, 218)
        WindowTool.field(self.frame, "ساعت شروع", self.start_time, 264)

        WindowTool.button(self.frame, "ذخیره", 1380, 320, self.save_click, WindowTool.GREEN, width=85)
        WindowTool.button(self.frame, "ویرایش", 1285, 320, self.edit_click, WindowTool.BLUE, width=85)
        WindowTool.button(self.frame, "لغو نوبت", 1190, 320, self.cancel_click, WindowTool.RED, width=85)
        WindowTool.button(self.frame, "حذف", 1095, 320, self.remove_click, WindowTool.GRAY, width=85)
        WindowTool.button(self.frame, "فرم جدید", 1380, 368, self.reset_from, WindowTool.GRAY, width=120)
        WindowTool.button(self.frame, "نمایش ساعت های آزاد", 1240, 368, self.free_slots_click, WindowTool.BLUE, width=240)
        WindowTool.hint(self.frame, "تاریخ مثل 1405/08/10 و ساعت مثل 08:00 نوشته شود", 416)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # فرم را ریست می کند، مجدد تمام اطلاعات را از فایل می خواند و در جدول ها نمایش می دهد
    def reset_from(self):
        self.appointment_id.set(self.controller.next_id()[1])
        self.customer_id.set("")
        self.shift_id.set("")
        self.date.set("")
        self.start_time.set("")

        WindowTool.fill_table(self.table, self.controller.find_active_rows()[1])
        WindowTool.fill_table(self.customer_table, [customer.to_tuple() for customer in self.customer_controller.find_all()[1]])
        WindowTool.fill_table(self.shift_table, self.shift_controller.find_all_rows()[1])
        WindowTool.fill_table(self.slot_table, [])

    # دکمه ذخیره فشرده شود
    def save_click(self):
        success, message = self.controller.save(
            self.appointment_id.get(),
            self.customer_id.get(),
            self.shift_id.get(),
            self.date.get(),
            self.start_time.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه ویرایش فشرده شود
    def edit_click(self):
        success, message = self.controller.edit(
            self.appointment_id.get(),
            self.customer_id.get(),
            self.shift_id.get(),
            self.date.get(),
            self.start_time.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه لغو نوبت فشرده شود
    def cancel_click(self):
        success, message = self.controller.cancel(self.appointment_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه حذف فشرده شود
    def remove_click(self):
        success, message = self.controller.remove(self.appointment_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # ساعت های آزاد شیفت انتخاب شده در تاریخ وارد شده را نمایش می دهد
    def free_slots_click(self):
        success, result = self.controller.free_slots(self.shift_id.get(), self.date.get())

        if success:
            WindowTool.fill_table(self.slot_table, result)
            if not result:
                messagebox.showinfo("اطلاع", "ساعت آزادی وجود ندارد")
        else:
            WindowTool.fill_table(self.slot_table, [])
            messagebox.showerror("خطا", result)

    # وقتی روی جدول نوبت ها کلیک کنیم اطلاعات را نمایش می دهد
    def table_click(self, event):
        selected_appointment = WindowTool.selected(self.table)

        if selected_appointment:
            success, appointment = self.controller.find_by_id(selected_appointment[0])
            if success:
                self.appointment_id.set(appointment.appointment_id)
                self.customer_id.set(appointment.customer_id)
                self.shift_id.set(appointment.shift_id)
                self.date.set(appointment.date)
                self.start_time.set(appointment.start_time)

    # انتخاب مشتری از جدول
    def customer_table_click(self, event):
        selected_customer = WindowTool.selected(self.customer_table)

        if selected_customer:
            self.customer_id.set(selected_customer[0])

    # انتخاب شیفت از جدول
    def shift_table_click(self, event):
        selected_shift = WindowTool.selected(self.shift_table)

        if selected_shift:
            self.shift_id.set(selected_shift[0])

    # انتخاب ساعت آزاد از جدول
    def slot_table_click(self, event):
        selected_slot = WindowTool.selected(self.slot_table)

        if selected_slot:
            self.start_time.set(selected_slot[0])
