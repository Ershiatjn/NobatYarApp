from data_access.appointment_da import AppointmentDa
from data_access.customer_da import CustomerDa
from data_access.employee_da import EmployeeDa
from data_access.service_da import ServiceDa
from data_access.shift_da import ShiftDa
from tools.date_tool import DateTool


# قوانین مربوط به نوبت ها (مدیریت زمان)
class AppointmentBL:
    def __init__(self):
        self.appointment_da = AppointmentDa()
        self.customer_da = CustomerDa()
        self.shift_da = ShiftDa()
        self.service_da = ServiceDa()
        self.employee_da = EmployeeDa()

    # بررسی می کند آیا این بازه برای شیفت در آن تاریخ آزاد است یا نه
    def is_free(self, shift_id, date, start_time, end_time, ignore_id=0):
        for other in self.appointment_da.find_all():
            if other.canceled or other.appointment_id == ignore_id:
                continue
            if other.shift_id == shift_id and other.date == date:
                if DateTool.is_overlap(start_time, end_time, other.start_time, other.end_time):
                    return False
        return True

    def check_rules(self, appointment):
        if not self.customer_da.find_by_id(appointment.customer_id):
            raise ValueError("مشتری با این شناسه وجود ندارد")
        shift = self.shift_da.find_by_id(appointment.shift_id)
        if not shift:
            raise ValueError("شیفتی با این شناسه وجود ندارد")
        service = self.service_da.find_by_id(shift.service_id)

        jalali_date = DateTool.parse_date(appointment.date)
        if jalali_date < DateTool.today():
            raise ValueError("تاریخ نوبت نمی تواند گذشته باشد")
        if jalali_date.weekday() != shift.weekday:
            raise ValueError(f"این شیفت مربوط به روز {DateTool.weekday_name(shift.weekday)} است")

        end_time = DateTool.add_minutes(appointment.start_time, service.duration)
        if DateTool.to_time(appointment.start_time) < DateTool.to_time(shift.start_time) or DateTool.to_time(end_time) > DateTool.to_time(shift.end_time):
            raise ValueError(f"نوبت باید داخل ساعت شیفت ({shift.start_time} تا {shift.end_time}) باشد")
        if jalali_date == DateTool.today() and DateTool.to_time(appointment.start_time) <= DateTool.now_time():
            raise ValueError("این ساعت گذشته است")

        if not self.is_free(shift.shift_id, appointment.date, appointment.start_time, end_time, appointment.appointment_id):
            raise ValueError("این بازه زمانی قبلاً رزرو شده است")

        # یک مشتری در یک زمان فقط یک نوبت می تواند داشته باشد
        for other in self.appointment_da.find_all():
            if other.canceled or other.appointment_id == appointment.appointment_id:
                continue
            if other.customer_id == appointment.customer_id and other.date == appointment.date:
                if DateTool.is_overlap(appointment.start_time, end_time, other.start_time, other.end_time):
                    raise ValueError("این مشتری در این بازه زمانی نوبت دیگری دارد")
        return service, end_time

    def save(self, appointment):
        if self.appointment_da.find_by_id(appointment.appointment_id):
            raise ValueError("این شناسه قبلاً ثبت شده است")
        service, end_time = self.check_rules(appointment)
        appointment.end_time = end_time
        # مبلغ همان لحظه ثبت نوبت ذخیره می شود تا تغییر قیمت بعدی روی آن اثر نگذارد
        appointment.price = service.price
        appointment.canceled = False
        self.appointment_da.save(appointment)

    def edit(self, appointment):
        old = self.appointment_da.find_by_id(appointment.appointment_id)
        if not old:
            raise ValueError("نوبتی با این شناسه وجود ندارد")
        if old.canceled:
            raise ValueError("نوبت لغو شده قابل ویرایش نیست")
        service, end_time = self.check_rules(appointment)
        appointment.end_time = end_time
        if old.shift_id == appointment.shift_id:
            appointment.price = old.price
        else:
            appointment.price = service.price
        appointment.canceled = False
        self.appointment_da.edit(appointment)

    def cancel(self, appointment_id):
        appointment = self.appointment_da.find_by_id(appointment_id)
        if not appointment:
            raise ValueError("نوبتی با این شناسه وجود ندارد")
        if appointment.canceled:
            raise ValueError("این نوبت قبلاً لغو شده است")
        appointment.canceled = True
        self.appointment_da.edit(appointment)

    def remove(self, appointment_id):
        if not self.appointment_da.find_by_id(appointment_id):
            raise ValueError("نوبتی با این شناسه وجود ندارد")
        self.appointment_da.remove(appointment_id)

    def find_by_id(self, appointment_id):
        appointment = self.appointment_da.find_by_id(appointment_id)
        if not appointment:
            raise ValueError("نوبتی با این شناسه وجود ندارد")
        return appointment

    def find_all(self):
        return self.appointment_da.find_all()

    # ساعت های آزاد یک شیفت در یک تاریخ را به صورت (شروع، پایان) برمی گرداند
    def free_slots(self, shift_id, date):
        shift = self.shift_da.find_by_id(shift_id)
        if not shift:
            raise ValueError("شیفتی با این شناسه وجود ندارد")
        service = self.service_da.find_by_id(shift.service_id)

        jalali_date = DateTool.parse_date(date)
        if jalali_date < DateTool.today():
            raise ValueError("تاریخ نوبت نمی تواند گذشته باشد")
        if jalali_date.weekday() != shift.weekday:
            raise ValueError(f"این شیفت مربوط به روز {DateTool.weekday_name(shift.weekday)} است")

        date = DateTool.format_date(jalali_date)
        slot_list = []
        start_time = shift.start_time
        while True:
            try:
                end_time = DateTool.add_minutes(start_time, service.duration)
            except ValueError:
                break
            if DateTool.to_time(end_time) > DateTool.to_time(shift.end_time):
                break
            past = jalali_date == DateTool.today() and DateTool.to_time(start_time) <= DateTool.now_time()
            if not past and self.is_free(shift.shift_id, date, start_time, end_time):
                slot_list.append((start_time, end_time))
            start_time = end_time
        return slot_list

    # ردیف جدول: شناسه، مشتری، کارمند، خدمت، تاریخ، روز، از ساعت، تا ساعت، مبلغ
    def to_row(self, appointment):
        customer = self.customer_da.find_by_id(appointment.customer_id)
        shift = self.shift_da.find_by_id(appointment.shift_id)
        employee = self.employee_da.find_by_id(shift.employee_id)
        service = self.service_da.find_by_id(shift.service_id)
        weekday = DateTool.parse_date(appointment.date).weekday()
        return (
            appointment.appointment_id,
            f"{customer.name} {customer.family}",
            f"{employee.name} {employee.family}",
            service.title,
            appointment.date,
            DateTool.weekday_name(weekday),
            appointment.start_time,
            appointment.end_time,
            appointment.price
        )

    def sort_key(self, appointment):
        return (appointment.date, appointment.start_time)

    def find_active_rows(self):
        appointment_list = [a for a in self.appointment_da.find_all() if not a.canceled]
        appointment_list.sort(key=self.sort_key)
        return [self.to_row(appointment) for appointment in appointment_list]

    def find_canceled_rows(self):
        appointment_list = [a for a in self.appointment_da.find_all() if a.canceled]
        appointment_list.sort(key=self.sort_key)
        return [self.to_row(appointment) for appointment in appointment_list]

    def find_rows_by_customer(self, customer_id):
        appointment_list = [a for a in self.appointment_da.find_all() if a.customer_id == customer_id and not a.canceled]
        appointment_list.sort(key=self.sort_key)
        return [self.to_row(appointment) for appointment in appointment_list]

    def find_rows_by_employee(self, employee_id):
        appointment_list = []
        for appointment in self.appointment_da.find_all():
            shift = self.shift_da.find_by_id(appointment.shift_id)
            if shift and shift.employee_id == employee_id and not appointment.canceled:
                appointment_list.append(appointment)
        appointment_list.sort(key=self.sort_key)
        return [self.to_row(appointment) for appointment in appointment_list]

    def next_id(self):
        id_list = [appointment.appointment_id for appointment in self.appointment_da.find_all()]
        if id_list:
            return max(id_list) + 1
        return 1
