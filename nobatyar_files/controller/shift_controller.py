from business_logic.shift_bl import ShiftBL
from model.shift import Shift
from tools.converter import Converter
from tools.date_tool import DateTool

# کنترلر شیفت ها
class ShiftController:
    def __init__(self):
        self.shift_bl = ShiftBL()


    def save(self, shift_id, employee_id, service_id, weekday, start_time, end_time):
        try:
            shift = Shift(
                Converter.to_int(shift_id),
                Converter.to_int(employee_id),
                Converter.to_int(service_id),
                DateTool.weekday_from_name(weekday),
                DateTool.normalize_time(start_time),
                DateTool.normalize_time(end_time)
            )
            self.shift_bl.save(shift)
            return True, "شیفت ذخیره شد"
        except Exception as e:
            return False, f"ذخیره ناموفق بود : {e}"

    def edit(self, shift_id, employee_id, service_id, weekday, start_time, end_time):
        try:
            shift = Shift(
                Converter.to_int(shift_id),
                Converter.to_int(employee_id),
                Converter.to_int(service_id),
                DateTool.weekday_from_name(weekday),
                DateTool.normalize_time(start_time),
                DateTool.normalize_time(end_time)
            )
            self.shift_bl.edit(shift)
            return True, "شیفت ویرایش شد"
        except Exception as e:
            return False, f"ویرایش ناموفق بود : {e}"

    def remove(self, shift_id):
        try:
            self.shift_bl.remove(Converter.to_int(shift_id))
            return True, "شیفت حذف شد"
        except Exception as e:
            return False, f"حذف ناموفق بود : {e}"

    def find_by_id(self, shift_id):
        try:
            return True, self.shift_bl.find_by_id(Converter.to_int(shift_id))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_all(self):
        try:
            shift_list = self.shift_bl.find_all()
            return True, shift_list
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_all_rows(self):
        try:
            return True, self.shift_bl.find_all_rows()
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_rows_by_employee(self, employee_id):
        try:
            return True, self.shift_bl.find_rows_by_employee(Converter.to_int(employee_id))
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def next_id(self):
        return True, self.shift_bl.next_id()
