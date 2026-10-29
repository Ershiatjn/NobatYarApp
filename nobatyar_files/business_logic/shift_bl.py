from data_access.appointment_da import AppointmentDa
from data_access.employee_da import EmployeeDa
from data_access.service_da import ServiceDa
from data_access.shift_da import ShiftDa
from tools.date_tool import DateTool


# قوانین مربوط به شیفت ها
class ShiftBL:
    def __init__(self):
        self.shift_da = ShiftDa()
        self.employee_da = EmployeeDa()
        self.service_da = ServiceDa()
        self.appointment_da = AppointmentDa()

    def check_rules(self, shift):
        employee = self.employee_da.find_by_id(shift.employee_id)
        if not employee:
            raise ValueError("کارمندی با این شناسه وجود ندارد")
        service = self.service_da.find_by_id(shift.service_id)
        if not service:
            raise ValueError("خدمتی با این شناسه وجود ندارد")
        if shift.service_id not in employee.service_ids:
            raise ValueError("این خدمت جزو خدمات این کارمند نیست")

        length = DateTool.to_time(shift.end_time) - DateTool.to_time(shift.start_time)
        if length.total_seconds() <= 0:
            raise ValueError("ساعت پایان باید بعد از ساعت شروع باشد")
        if length.total_seconds() / 60 < service.duration:
            raise ValueError(f"طول شیفت از مدت خدمت ({service.duration} دقیقه) کمتر است")

        # یک کارمند در یک زمان فقط یک شیفت می تواند داشته باشد
        for other in self.shift_da.find_all():
            if other.shift_id != shift.shift_id and other.employee_id == shift.employee_id and other.weekday == shift.weekday:
                if DateTool.is_overlap(shift.start_time, shift.end_time, other.start_time, other.end_time):
                    raise ValueError(f"این شیفت با شیفت شماره {other.shift_id} همپوشانی دارد")

    def save(self, shift):
        if self.shift_da.find_by_id(shift.shift_id):
            raise ValueError("این شناسه قبلاً ثبت شده است")
        self.check_rules(shift)
        self.shift_da.save(shift)

    def edit(self, shift):
        if not self.shift_da.find_by_id(shift.shift_id):
            raise ValueError("شیفتی با این شناسه وجود ندارد")
        for appointment in self.appointment_da.find_all():
            if appointment.shift_id == shift.shift_id and not appointment.canceled:
                raise ValueError("برای این شیفت نوبت فعال ثبت شده و ویرایش نمی شود")
        self.check_rules(shift)
        self.shift_da.edit(shift)

    def remove(self, shift_id):
        for appointment in self.appointment_da.find_all():
            if appointment.shift_id == shift_id:
                raise ValueError("برای این شیفت نوبت ثبت شده و حذف نمی شود (ابتدا نوبت ها را حذف کنید)")
        self.shift_da.remove(shift_id)

    def find_by_id(self, shift_id):
        shift = self.shift_da.find_by_id(shift_id)
        if not shift:
            raise ValueError("شیفتی با این شناسه وجود ندارد")
        return shift

    def find_all(self):
        return self.shift_da.find_all()

    # ردیف جدول: شناسه، کارمند، خدمت، مبلغ، مدت، روز، از ساعت، تا ساعت، نزدیک ترین تاریخ
    def to_row(self, shift):
        employee = self.employee_da.find_by_id(shift.employee_id)
        service = self.service_da.find_by_id(shift.service_id)
        return (
            shift.shift_id,
            f"{employee.name} {employee.family}",
            service.title,
            service.price,
            service.duration,
            DateTool.weekday_name(shift.weekday),
            shift.start_time,
            shift.end_time,
            DateTool.next_date(shift.weekday)
        )

    def find_all_rows(self):
        return [self.to_row(shift) for shift in self.shift_da.find_all()]

    def find_rows_by_employee(self, employee_id):
        return [self.to_row(shift) for shift in self.shift_da.find_all() if shift.employee_id == employee_id]

    def next_id(self):
        id_list = [shift.shift_id for shift in self.shift_da.find_all()]
        if id_list:
            return max(id_list) + 1
        return 1
