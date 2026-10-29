from tkinter import *
from tkinter import ttk


# ساخت پنجره ی اصلی (یک پنجره ی ثابت برای کل برنامه) و ویجت های رنگی (نوشته، کادر ورودی، دکمه، جدول)
class WindowTool:
    WIDTH = 1400
    HEIGHT = 800

    BG = "#E9EEF5"
    BAR = "#B8CCEA"
    LABEL = "#C9D9F2"
    ENTRY = "#FFF8D6"
    GREEN = "#9FE2B4"
    BLUE = "#A9C7F5"
    RED = "#F4A9A9"
    GRAY = "#D0D4DA"

    ROW = 25
    HEAD = 28

    # پنجره ی اصلی فقط یک بار ساخته می شود و اندازه و جایش عوض نمی شود
    @staticmethod
    def create_window(title):
        win = Tk()
        win.title(title)
        win.configure(bg=WindowTool.BG)
        win.geometry(f"{WindowTool.WIDTH}x{WindowTool.HEIGHT}+60+30")
        return win

    # هر صفحه یک قاب تمام پنجره است؛ با بستن قاب، صفحه ی بعدی جایش را می گیرد
    @staticmethod
    def frame(win):
        frame = Frame(win, bg=WindowTool.BG)
        frame.place(x=0, y=0, width=WindowTool.WIDTH, height=WindowTool.HEIGHT)
        return frame

    # نوار عنوان صفحه و دکمه ی بازگشت
    @staticmethod
    def header(frame, title, back_click=None):
        Label(frame, text=title, bg=WindowTool.BAR, fg="black").place(x=0, y=0, width=WindowTool.WIDTH, height=50)
        if back_click:
            WindowTool.button(frame, "بازگشت", 1380, 7, back_click, WindowTool.GRAY, width=110, height=36)

    # نوشته ی رنگی که متن آن دقیقا وسط کادر قرار می گیرد (right لبه ی راست کادر است)
    @staticmethod
    def label(frame, text, right, y, width=150, height=34, textvariable=None, bg=None):
        Label(frame, text=text, textvariable=textvariable, bg=bg or WindowTool.LABEL, fg="black").place(x=right - width, y=y, width=width, height=height)

    # توضیح کوچک زیر فرم
    @staticmethod
    def hint(frame, text, y, height=30):
        Label(frame, text=text, bg=WindowTool.BG, fg="black", wraplength=370).place(x=1000, y=y, width=380, height=height)

    # عنوان بالای جدول (left لبه ی چپ کادر است)
    @staticmethod
    def section(frame, text, left, y, width):
        Label(frame, text=text, bg=WindowTool.LABEL, fg="black").place(x=left, y=y, width=width, height=30)

    # کادر ورودی (right لبه ی راست کادر است)
    @staticmethod
    def entry(frame, variable, right, y, width=220, height=34, readonly=False):
        entry = Entry(frame, textvariable=variable, justify=RIGHT, bg=WindowTool.ENTRY, fg="black")
        if readonly:
            entry.configure(state="readonly", readonlybackground=WindowTool.ENTRY)
        entry.place(x=right - width, y=y, width=width, height=height)

    # یک ردیف فرم: نوشته در سمت راست و کادر ورودی کنار آن
    @staticmethod
    def field(frame, text, variable, y, readonly=False):
        WindowTool.label(frame, text, 1380, y)
        WindowTool.entry(frame, variable, 1220, y, readonly=readonly)

    # دکمه ی رنگی (right لبه ی راست دکمه است)
    @staticmethod
    def button(frame, text, right, y, command, color=None, width=180, height=40):
        Button(frame, text=text, bg=color or WindowTool.BLUE, fg="black", command=command).place(x=right - width, y=y, width=width, height=height)

    # جدول راست چین (ستون اول سمت راست است)  columns: فهرست (عنوان، عرض)
    @staticmethod
    def table(frame, x, y, columns, rows=10, command=None):
        columns = columns[::-1]
        table = ttk.Treeview(frame, show="headings", columns=list(range(len(columns))), height=rows)
        for number in range(len(columns)):
            table.heading(number, text=columns[number][0], anchor=CENTER)
            table.column(number, width=columns[number][1], anchor=CENTER)
        table.place(x=x, y=y)
        if command:
            table.bind("<ButtonRelease>", command)
        return table

    # جدول را خالی می کند و ردیف ها را در آن می ریزد (برای راست چین شدن ترتیب مقدارها برعکس می شود)
    @staticmethod
    def fill_table(table, rows):
        for item in table.get_children():
            table.delete(item)
        for row in rows:
            table.insert("", END, values=tuple(row)[::-1])

    # ردیف انتخاب شده ی جدول را با ترتیب اصلی مقدارها برمی گرداند
    @staticmethod
    def selected(table):
        values = table.item(table.focus())["values"]
        return list(values)[::-1]
