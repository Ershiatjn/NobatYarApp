import re

from tools.date_tool import DateTool


class Validator:
    @staticmethod
    def id_validator(id):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("شناسه نامعتبر است")

    @staticmethod
    def name_validator(name):
        if not re.match(r"^[\u0600-\u06FFa-zA-Z\u200c ]{2,30}$", name):
            raise ValueError("نام نامعتبر است")

    @staticmethod
    def family_validator(family):
        if not re.match(r"^[\u0600-\u06FFa-zA-Z\u200c ]{2,40}$", family):
            raise ValueError("نام خانوادگی نامعتبر است")

    @staticmethod
    def title_validator(title):
        if not re.match(r"^[\u0600-\u06FFa-zA-Z0-9\u200c ]{2,40}$", title):
            raise ValueError("عنوان خدمت نامعتبر است")

    @staticmethod
    def phone_validator(phone):
        if not re.match(r"^09\d{9}$", phone):
            raise ValueError("شماره موبایل نامعتبر است (نمونه درست: 09121234567)")

    @staticmethod
    def price_validator(price):
        if not isinstance(price, int) or not 0 <= price <= 1000000000:
            raise ValueError("مبلغ نامعتبر است")

    @staticmethod
    def duration_validator(duration):
        if not isinstance(duration, int) or not 5 <= duration <= 600:
            raise ValueError("مدت خدمت باید بین 5 تا 600 دقیقه باشد")

    @staticmethod
    def service_ids_validator(service_ids):
        if not isinstance(service_ids, list):
            raise ValueError("فهرست خدمات نامعتبر است")
        for service_id in service_ids:
            Validator.id_validator(service_id)

    @staticmethod
    def weekday_validator(weekday):
        if not isinstance(weekday, int) or not 0 <= weekday <= 6:
            raise ValueError("روز هفته نامعتبر است")

    @staticmethod
    def time_validator(time):
        if not re.match(r"^([01]\d|2[0-3]):[0-5]\d$", time):
            raise ValueError("ساعت نامعتبر است (نمونه درست: 08:00)")

    @staticmethod
    def date_validator(date):
        DateTool.parse_date(date)
