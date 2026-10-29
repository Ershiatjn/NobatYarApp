from data_access.employee_da import EmployeeDa
from data_access.service_da import ServiceDa
from data_access.shift_da import ShiftDa


# قوانین مربوط به کارمندان
class EmployeeBL:
    def __init__(self):
        self.employee_da = EmployeeDa()
        self.service_da = ServiceDa()
        self.shift_da = ShiftDa()

    def check_services(self, employee):
        for service_id in employee.service_ids:
            if not self.service_da.find_by_id(service_id):
                raise ValueError(f"خدمتی با شناسه {service_id} وجود ندارد")

    def save(self, employee):
        if self.employee_da.find_by_id(employee.employee_id):
            raise ValueError("این شناسه قبلاً ثبت شده است")
        self.check_services(employee)
        self.employee_da.save(employee)

    def edit(self, employee):
        if not self.employee_da.find_by_id(employee.employee_id):
            raise ValueError("کارمندی با این شناسه وجود ندارد")
        self.check_services(employee)
        # خدمتی که در شیفت این کارمند استفاده شده نباید از فهرست خدماتش حذف شود
        for shift in self.shift_da.find_all():
            if shift.employee_id == employee.employee_id and shift.service_id not in employee.service_ids:
                raise ValueError(f"خدمت شماره {shift.service_id} در شیفت شماره {shift.shift_id} استفاده شده است")
        self.employee_da.edit(employee)

    def remove(self, employee_id):
        for shift in self.shift_da.find_all():
            if shift.employee_id == employee_id:
                raise ValueError("این کارمند شیفت دارد و حذف نمی شود")
        self.employee_da.remove(employee_id)

    def find_by_id(self, employee_id):
        employee = self.employee_da.find_by_id(employee_id)
        if not employee:
            raise ValueError("کارمندی با این شناسه وجود ندارد")
        return employee

    def find_all(self):
        return self.employee_da.find_all()

    # عنوان خدمات کارمند را به صورت یک متن برمی گرداند
    def service_titles(self, employee):
        title_list = []
        for service_id in employee.service_ids:
            service = self.service_da.find_by_id(service_id)
            if service:
                title_list.append(service.title)
        return "، ".join(title_list)

    # ردیف های جدول: شناسه، نام، نام خانوادگی، شناسه خدمات، عنوان خدمات
    def find_all_rows(self):
        row_list = []
        for employee in self.employee_da.find_all():
            row_list.append(employee.to_tuple() + (self.service_titles(employee),))
        return row_list

    def next_id(self):
        id_list = [employee.employee_id for employee in self.employee_da.find_all()]
        if id_list:
            return max(id_list) + 1
        return 1
