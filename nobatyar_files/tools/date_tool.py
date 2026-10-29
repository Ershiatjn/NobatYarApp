import re
from datetime import datetime, timedelta

from persiantools.jdatetime import JalaliDate

from tools.converter import Converter


# تمام کارهای مربوط به تاریخ شمسی و ساعت در این کلاس انجام می شود
class DateTool:
    WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

    @staticmethod
    def today():
        return JalaliDate.today()

    @staticmethod
    def parse_date(text):
        text = Converter.to_english(text)
        if not re.match(r"^\d{4}/\d{1,2}/\d{1,2}$", text):
            raise ValueError("تاریخ نامعتبر است (نمونه درست: 1405/08/10)")
        year, month, day = text.split("/")
        try:
            return JalaliDate(int(year), int(month), int(day))
        except ValueError:
            raise ValueError("تاریخ نامعتبر است (نمونه درست: 1405/08/10)")

    @staticmethod
    def format_date(jalali_date):
        return jalali_date.strftime("%Y/%m/%d")

    @staticmethod
    def weekday_name(weekday):
        return DateTool.WEEKDAYS[weekday]

    @staticmethod
    def weekday_from_name(text):
        text = Converter.to_english(text)
        text = text.replace("\u200c", "").replace(" ", "").replace("ي", "ی")
        for weekday in range(7):
            name = DateTool.WEEKDAYS[weekday].replace("\u200c", "")
            if name == text:
                return weekday
        raise ValueError("روز هفته نامعتبر است")

    # نزدیک ترین تاریخ شمسی (از امروز) که در آن روز هفته قرار دارد
    @staticmethod
    def next_date(weekday):
        today = DateTool.today()
        days = (weekday - today.weekday()) % 7
        return DateTool.format_date(today + timedelta(days=days))

    @staticmethod
    def normalize_date(text):
        return DateTool.format_date(DateTool.parse_date(text))

    @staticmethod
    def normalize_time(text):
        try:
            return DateTool.to_time(text).strftime("%H:%M")
        except ValueError:
            raise ValueError("ساعت نامعتبر است (نمونه درست: 08:00)")

    @staticmethod
    def to_time(text):
        return datetime.strptime(Converter.to_english(text), "%H:%M")

    @staticmethod
    def add_minutes(text, minutes):
        start = DateTool.to_time(text)
        time = start + timedelta(minutes=minutes)
        if time.day != start.day:
            raise ValueError("نوبت نمی تواند از ساعت 24 عبور کند")
        return time.strftime("%H:%M")

    @staticmethod
    def now_time():
        return datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")

    @staticmethod
    def is_overlap(start1, end1, start2, end2):
        return DateTool.to_time(start1) < DateTool.to_time(end2) and DateTool.to_time(start2) < DateTool.to_time(end1)
