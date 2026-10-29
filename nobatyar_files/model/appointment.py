from tools.validation import Validator


class Appointment:
    # ساعت پایان و مبلغ را منطق برنامه (business_logic) از روی خدمت محاسبه می کند
    def __init__(self, appointment_id, customer_id, shift_id, date, start_time, end_time="00:00", price=0, canceled=False):
        self.appointment_id = appointment_id
        self.customer_id = customer_id
        self.shift_id = shift_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.canceled = canceled

    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id):
        Validator.id_validator(appointment_id)
        self.__appointment_id = appointment_id

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        Validator.id_validator(customer_id)
        self.__customer_id = customer_id

    @property
    def shift_id(self):
        return self.__shift_id

    @shift_id.setter
    def shift_id(self, shift_id):
        Validator.id_validator(shift_id)
        self.__shift_id = shift_id

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        Validator.date_validator(date)
        self.__date = date

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        Validator.time_validator(start_time)
        self.__start_time = start_time

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        Validator.time_validator(end_time)
        self.__end_time = end_time

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        Validator.price_validator(price)
        self.__price = price


    def __repr__(self):
        return f"Appointment({self.appointment_id}, {self.customer_id}, {self.shift_id}, {self.date}, {self.start_time}, {self.end_time}, {self.price}, {self.canceled})"

    def to_tuple(self):
        return (self.appointment_id, self.customer_id, self.shift_id, self.date, self.start_time, self.end_time, self.price, self.canceled)
