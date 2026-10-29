from data_access.appointment_da import AppointmentDa
from data_access.customer_da import CustomerDa


# قوانین مربوط به مشتریان
class CustomerBL:
    def __init__(self):
        self.customer_da = CustomerDa()
        self.appointment_da = AppointmentDa()

    def check_phone(self, customer):
        for other in self.customer_da.find_all():
            if other.phone == customer.phone and other.customer_id != customer.customer_id:
                raise ValueError("این شماره موبایل قبلاً ثبت شده است")

    def save(self, customer):
        if self.customer_da.find_by_id(customer.customer_id):
            raise ValueError("این شناسه قبلاً ثبت شده است")
        self.check_phone(customer)
        self.customer_da.save(customer)

    def edit(self, customer):
        if not self.customer_da.find_by_id(customer.customer_id):
            raise ValueError("مشتری با این شناسه وجود ندارد")
        self.check_phone(customer)
        self.customer_da.edit(customer)

    def remove(self, customer_id):
        for appointment in self.appointment_da.find_all():
            if appointment.customer_id == customer_id:
                raise ValueError("این مشتری نوبت ثبت شده دارد و حذف نمی شود")
        self.customer_da.remove(customer_id)

    def find_by_id(self, customer_id):
        customer = self.customer_da.find_by_id(customer_id)
        if not customer:
            raise ValueError("مشتری با این شناسه وجود ندارد")
        return customer

    def find_by_phone(self, phone):
        for customer in self.customer_da.find_all():
            if customer.phone == phone:
                return customer
        raise ValueError("مشتری با این شماره موبایل پیدا نشد")

    def find_all(self):
        return self.customer_da.find_all()

    def next_id(self):
        id_list = [customer.customer_id for customer in self.customer_da.find_all()]
        if id_list:
            return max(id_list) + 1
        return 1
