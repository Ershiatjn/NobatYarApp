from tools.validation import Validator


class Shift:
    def __init__(self, shift_id, employee_id, service_id, weekday, start_time, end_time):
        self.shift_id = shift_id
        self.employee_id = employee_id
        self.service_id = service_id
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time

    @property
    def shift_id(self):
        return self.__shift_id

    @shift_id.setter
    def shift_id(self, shift_id):
        Validator.id_validator(shift_id)
        self.__shift_id = shift_id

    @property
    def employee_id(self):
        return self.__employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        Validator.id_validator(employee_id)
        self.__employee_id = employee_id

    @property
    def service_id(self):
        return self.__service_id

    @service_id.setter
    def service_id(self, service_id):
        Validator.id_validator(service_id)
        self.__service_id = service_id

    @property
    def weekday(self):
        return self.__weekday

    @weekday.setter
    def weekday(self, weekday):
        Validator.weekday_validator(weekday)
        self.__weekday = weekday

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


    def __repr__(self):
        return f"Shift({self.shift_id}, {self.employee_id}, {self.service_id}, {self.weekday}, {self.start_time}, {self.end_time})"

    def to_tuple(self):
        return (self.shift_id, self.employee_id, self.service_id, self.weekday, self.start_time, self.end_time)
