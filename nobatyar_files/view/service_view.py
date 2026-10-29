from tkinter import *
from tkinter import messagebox

from controller.service_controller import ServiceController
from tools.window_tool import WindowTool


class ServiceView:
    def __init__(self, win, back):
        self.win = win
        self.back = back
        self.controller = ServiceController()

        self.frame = WindowTool.frame(win)
        WindowTool.header(self.frame, "خدمات", self.back_click)

        # جدول (ستون ها از راست به چپ چیده می شوند)
        columns = [("شناسه", 90), ("عنوان خدمت", 350), ("مبلغ (تومان)", 260), ("مدت (دقیقه)", 250)]
        self.table = WindowTool.table(self.frame, 20, 80, columns, rows=18, command=self.table_click)

        # فرم
        self.service_id = StringVar(win)
        self.title = StringVar(win)
        self.price = StringVar(win)
        self.duration = StringVar(win)
        WindowTool.field(self.frame, "شناسه", self.service_id, 80)
        WindowTool.field(self.frame, "عنوان خدمت", self.title, 134)
        WindowTool.field(self.frame, "مبلغ (تومان)", self.price, 188)
        WindowTool.field(self.frame, "مدت (دقیقه)", self.duration, 242)

        WindowTool.button(self.frame, "ذخیره", 1380, 310, self.save_click, WindowTool.GREEN)
        WindowTool.button(self.frame, "ویرایش", 1180, 310, self.edit_click, WindowTool.BLUE)
        WindowTool.button(self.frame, "حذف", 1380, 360, self.remove_click, WindowTool.RED)
        WindowTool.button(self.frame, "فرم جدید", 1180, 360, self.reset_from, WindowTool.GRAY)
        WindowTool.hint(self.frame, "تغییر مبلغ فقط روی نوبت های جدید اثر می گذارد", 420, 50)

        self.reset_from()

    # بازگشت به صفحه ی قبل
    def back_click(self):
        self.frame.destroy()
        self.back()

    # فرم را ریست می کند، مجدد تمام خدمات را از فایل می خواند و در جدول نمایش می دهد
    def reset_from(self):
        self.service_id.set(self.controller.next_id()[1])
        self.title.set("")
        self.price.set("")
        self.duration.set("")

        WindowTool.fill_table(self.table, [service.to_tuple() for service in self.controller.find_all()[1]])

    # دکمه ذخیره فشرده شود
    def save_click(self):
        success, message = self.controller.save(
            self.service_id.get(),
            self.title.get(),
            self.price.get(),
            self.duration.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه ویرایش فشرده شود
    def edit_click(self):
        success, message = self.controller.edit(
            self.service_id.get(),
            self.title.get(),
            self.price.get(),
            self.duration.get()
        )

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # دکمه حذف فشرده شود
    def remove_click(self):
        success, message = self.controller.remove(self.service_id.get())

        if success:
            messagebox.showinfo("موفق", message)
            self.reset_from()
        else:
            messagebox.showerror("خطا", message)

    # وقتی روی جدول کلیک کنیم اطلاعات را نمایش می دهد
    def table_click(self, event):
        selected_service = WindowTool.selected(self.table)

        if selected_service:
            success, service = self.controller.find_by_id(selected_service[0])
            if success:
                self.service_id.set(service.service_id)
                self.title.set(service.title)
                self.price.set(service.price)
                self.duration.set(service.duration)
