from tools.validation import Validator


class Customer:
    def __init__(self, customer_id, name, family, phone):
        self.customer_id = customer_id
        self.name = name
        self.family = family
        self.phone = phone

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        Validator.id_validator(customer_id)
        self.__customer_id = customer_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        Validator.name_validator(name)
        self.__name = name

    @property
    def family(self):
        return self.__family

    @family.setter
    def family(self, family):
        Validator.family_validator(family)
        self.__family = family

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        Validator.phone_validator(phone)
        self.__phone = phone


    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name}, {self.family}, {self.phone})"

    def to_tuple(self):
        return (self.customer_id, self.name, self.family, self.phone)
