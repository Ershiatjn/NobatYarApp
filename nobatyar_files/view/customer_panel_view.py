from tkinter import *
from tkinter import messagebox

from controller.appointment_controller import AppointmentController
from controller.customer_controller import CustomerController
from controller.shift_controller import ShiftController
from tools.window_tool import WindowTool


# بخش مشتری: مشتری با شماره موبایلش وارد می شود، از ساعت های آزاد نوبت می گیرد و نوبت های خودش را می بیند
class CustomerPanelView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = AppointmentController()
        self.customer_controller = CustomerController()
        self.shift_controller = ShiftController()
        self.customer = None

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "بخش مشتری", self.back_click)

        # جدول شیفت ها (ستون ها از راست به چپ چیده می شوند)
        WindowTool.section(self.frame, "شیفت ها و خدمات (برای انتخاب کلیک کنید)", 20, 65, 880)
        columns = [("شناسه", 60), ("کارمند", 160), ("خدمت", 140), ("مبلغ", 90), ("مدت", 70), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("تاریخ بعدی", 110)]
        self.table = WindowTool.table(self.frame, 20, 100, columns, rows=7, command=self.table_click)

        # جدول نوبت های من
        WindowTool.section(self.frame, "نوبت های من (برای لغو، نوبت را انتخاب کنید)", 20, 335, 940)
        appointment_columns = [("شناسه", 60), ("مشتری", 160), ("کارمند", 150), ("خدمت", 130), ("تاریخ", 100), ("روز هفته", 90), ("از ساعت", 80), ("تا ساعت", 80), ("مبلغ", 90)]
        self.appointment_table = WindowTool.table(self.frame, 20, 370, appointment_columns, rows=6, command=self.appointment_table_click)
        self.appointment_id = StringVar(win)
        WindowTool.button(self.frame, "لغو نوبت انتخاب شده", 960, 575, self.cancel_click, WindowTool.RED, width=220)

        # ورود و ثبت نوبت
        self.phone = StringVar(win)
        self.shift_id = StringVar(win)
        self.date = StringVar(win)
        self.start_time = StringVar(win)
        self.customer_text = StringVar(win)
        self.customer_text.set("مشتری وارد نشده است")
        WindowTool.field(self.frame, "شماره موبایل", self.phone, 80)
        WindowTool.button(self.frame, "ورود", 1380, 130, self.login_click, WindowTool.BLUE)
        WindowTool.label(self.frame, None, 1380, 180, width=380, textvariable=self.customer_text, bg=WindowTool.BG)
        WindowTool.field(self.frame, "شناسه شیفت", self.shift_id, 230)
        WindowTool.field(self.frame, "تاریخ (شمسی)", self.date, 284)
        WindowTool.field(self.frame, "ساعت شروع", self.start_time, 338)
        WindowTool.button(self.frame, "ثبت نوبت", 1380, 392, self.save_click, WindowTool.GREEN)
        WindowTool.button(self.frame, "ساعت های آزاد", 1190, 392, self.free_slots_click, WindowTool.BLUE, width=190)
        WindowTool.hint(self.frame, "تاریخ را مثل 1405/08/10 بنویسید", 442)

        # جدول ساعت های آزاد
        WindowTool.section(self.frame, "ساعت های آزاد (برای انتخاب کلیک کنید)", 1000, 490, 380)
        slot_columns = [("از ساعت", 120), ("تا ساعت", 120)]
        self.slot_table = WindowTool.table(self.frame, 1140, 525, slot_columns, rows=6, command=self.slot_table_click)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # جدول ها را خالی می کند، مجدد شیفت ها و نوبت های مشتری را از فایل می خواند و نمایش می دهد
    def reset_from(self):
        self.shift_id.set("")
        self.date.set("")
        self.start_time.set("")
        self.appointment_id.set("")

        WindowTool.fill_table(self.table, self.shift_controller.find_all_rows()[1])
        WindowTool.fill_table(self.slot_table, [])
        if self.customer:
            WindowTool.fill_table(self.appointment_table, self.controller.find_rows_by_customer(self.customer.customer_id)[1])
        else:
            WindowTool.fill_table(self.appointment_table, [])

    # دکمه ورود فشرده شود
    def login_click(self):
        success, result = self.customer_controller.find_by_phone(self.phone.get())

        if success:
            self.customer = result
            self.customer_text.set(f"مشتری: {result.name} {result.family}")
            self.reset_from()
        else:
            self.customer = None
            self.customer_text.set("مشتری وارد نشده است")
            self.reset_from()
            messagebox.showerror("خطا", result)

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

    # دکمه ثبت نوبت فشرده شود
    def save_click(self):
        if not self.customer:
            messagebox.showerror("خطا", "ابتدا با شماره موبایل وارد شوید")
            return

        success, message = self.controller.save(
            self.controller.next_id()[1],
            self.customer.customer_id,
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
        if self.appointment_id.get() == "":
            messagebox.showerror("خطا", "ابتدا یک نوبت را از جدول انتخاب کنید")
        else:
            success, message = self.controller.cancel(self.appointment_id.get())

            if success:
                messagebox.showinfo("موفق", message)
                self.reset_from()
            else:
                messagebox.showerror("خطا", message)

    # وقتی روی جدول شیفت ها کلیک کنیم شناسه شیفت انتخاب می شود
    def table_click(self, event):
        selected_shift = WindowTool.selected(self.table)

        if selected_shift:
            self.shift_id.set(selected_shift[0])

    # انتخاب ساعت آزاد از جدول
    def slot_table_click(self, event):
        selected_slot = WindowTool.selected(self.slot_table)

        if selected_slot:
            self.start_time.set(selected_slot[0])

    # انتخاب نوبت از جدول نوبت های من
    def appointment_table_click(self, event):
        selected_appointment = WindowTool.selected(self.appointment_table)

        if selected_appointment:
            self.appointment_id.set(selected_appointment[0])
