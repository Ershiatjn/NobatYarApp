from data_access.employee_da import EmployeeDa
from data_access.service_da import ServiceDa
from data_access.shift_da import ShiftDa
from tools.date_tool import DateTool


# قوانین مربوط به خدمات
class ServiceBL:
    def __init__(self):
        self.service_da = ServiceDa()
        self.employee_da = EmployeeDa()
        self.shift_da = ShiftDa()

    def save(self, service):
        if self.service_da.find_by_id(service.service_id):
            raise ValueError("این شناسه قبلاً ثبت شده است")
        self.service_da.save(service)

    def edit(self, service):
        if not self.service_da.find_by_id(service.service_id):
            raise ValueError("خدمتی با این شناسه وجود ندارد")
        # مدت جدید خدمت باید در شیفت هایی که این خدمت را دارند جا شود
        for shift in self.shift_da.find_all():
            if shift.service_id == service.service_id:
                length = DateTool.to_time(shift.end_time) - DateTool.to_time(shift.start_time)
                if length.total_seconds() / 60 < service.duration:
                    raise ValueError(f"مدت جدید از طول شیفت شماره {shift.shift_id} بیشتر است")
        self.service_da.edit(service)

    def remove(self, service_id):
        for employee in self.employee_da.find_all():
            if service_id in employee.service_ids:
                raise ValueError("این خدمت برای یک کارمند ثبت شده و حذف نمی شود")
        for shift in self.shift_da.find_all():
            if shift.service_id == service_id:
                raise ValueError("این خدمت در یک شیفت استفاده شده و حذف نمی شود")
        self.service_da.remove(service_id)

    def find_by_id(self, service_id):
        service = self.service_da.find_by_id(service_id)
        if not service:
            raise ValueError("خدمتی با این شناسه وجود ندارد")
        return service

    def find_all(self):
        return self.service_da.find_all()

    def next_id(self):
        id_list = [service.service_id for service in self.service_da.find_all()]
        if id_list:
            return max(id_list) + 1
        return 1
