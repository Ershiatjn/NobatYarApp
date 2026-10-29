from tools.validation import Validator


class Employee:
    def __init__(self, employee_id, name, family, service_ids):
        self.employee_id = employee_id
        self.name = name
        self.family = family
        self.service_ids = service_ids

    @property
    def employee_id(self):
        return self.__employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        Validator.id_validator(employee_id)
        self.__employee_id = employee_id

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
    def service_ids(self):
        return self.__service_ids

    @service_ids.setter
    def service_ids(self, service_ids):
        Validator.service_ids_validator(service_ids)
        self.__service_ids = service_ids


    def __repr__(self):
        return f"Employee({self.employee_id}, {self.name}, {self.family}, {self.service_ids})"

    def to_tuple(self):
        return (self.employee_id, self.name, self.family, ",".join(str(service_id) for service_id in self.service_ids))
