from business_logic.appointment_bl import AppointmentBL
from model.appointment import Appointment
from tools.converter import Converter
from tools.date_tool import DateTool

# کنترلر نوبت ها
class AppointmentController:
    def __init__(self):
        self.appointment_bl = AppointmentBL()


    def save(self, appointment_id, customer_id, shift_id, date, start_time):
        try:
            appointment = Appointment(
                Converter.to_int(appointment_id),
                Converter.to_int(customer_id),
                Converter.to_int(shift_id),
                DateTool.normalize_date(date),
                DateTool.normalize_time(start_time)
            )
            self.appointment_bl.save(appointment)
            return True, "نوبت ثبت شد"
        except Exception as e:
            return False, f"ثبت نوبت ناموفق بود : {e}"

    def edit(self, appointment_id, customer_id, shift_id, date, start_time):
        try:
            appointment = Appointment(
                Converter.to_int(appointment_id),
                Converter.to_int(customer_id),
                Converter.to_int(shift_id),
                DateTool.normalize_date(date),
                DateTool.normalize_time(start_time)
            )
            self.appointment_bl.edit(appointment)
            return True, "نوبت ویرایش شد"
        except Exception as e:
            return False, f"ویرایش ناموفق بود : {e}"

    def cancel(self, appointment_id):
        try:
            self.appointment_bl.cancel(Converter.to_int(appointment_id))
            return True, "نوبت لغو شد"
        except Exception as e:
            return False, f"لغو نوبت ناموفق بود : {e}"

    def remove(self, appointment_id):
        try:
            self.appointment_bl.remove(Converter.to_int(appointment_id))
            return True, "نوبت حذف شد"
        except Exception as e:
            return False, f"حذف ناموفق بود : {e}"

    def find_by_id(self, appointment_id):
        try:
            return True, self.appointment_bl.find_by_id(Converter.to_int(appointment_id))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_all(self):
        try:
            appointment_list = self.appointment_bl.find_all()
            return True, appointment_list
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def free_slots(self, shift_id, date):
        try:
            slot_list = self.appointment_bl.free_slots(Converter.to_int(shift_id), DateTool.normalize_date(date))
            return True, slot_list
        except Exception as e:
            return False, f"نمایش ساعت های آزاد ناموفق بود : {e}"

    def find_active_rows(self):
        try:
            return True, self.appointment_bl.find_active_rows()
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_canceled_rows(self):
        try:
            return True, self.appointment_bl.find_canceled_rows()
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_rows_by_customer(self, customer_id):
        try:
            return True, self.appointment_bl.find_rows_by_customer(Converter.to_int(customer_id))
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_rows_by_employee(self, employee_id):
        try:
            return True, self.appointment_bl.find_rows_by_employee(Converter.to_int(employee_id))
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def next_id(self):
        return True, self.appointment_bl.next_id()
