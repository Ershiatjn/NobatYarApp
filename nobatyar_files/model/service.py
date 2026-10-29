from tools.validation import Validator


class Service:
    def __init__(self, service_id, title, price, duration):
        self.service_id = service_id
        self.title = title
        self.price = price
        self.duration = duration

    @property
    def service_id(self):
        return self.__service_id

    @service_id.setter
    def service_id(self, service_id):
        Validator.id_validator(service_id)
        self.__service_id = service_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        Validator.title_validator(title)
        self.__title = title

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        Validator.price_validator(price)
        self.__price = price

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        Validator.duration_validator(duration)
        self.__duration = duration


    def __repr__(self):
        return f"Service({self.service_id}, {self.title}, {self.price}, {self.duration})"

    def to_tuple(self):
        return (self.service_id, self.title, self.price, self.duration)
