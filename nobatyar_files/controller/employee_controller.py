from business_logic.employee_bl import EmployeeBL
from model.employee import Employee
from tools.converter import Converter

# کنترلر کارمندان
class EmployeeController:
    def __init__(self):
        self.employee_bl = EmployeeBL()


    def save(self, employee_id, name, family, service_ids):
        try:
            employee = Employee(Converter.to_int(employee_id), name, family, Converter.to_int_list(service_ids))
            self.employee_bl.save(employee)
            return True, "کارمند ذخیره شد"
        except Exception as e:
            return False, f"ذخیره ناموفق بود : {e}"

    def edit(self, employee_id, name, family, service_ids):
        try:
            employee = Employee(Converter.to_int(employee_id), name, family, Converter.to_int_list(service_ids))
            self.employee_bl.edit(employee)
            return True, "کارمند ویرایش شد"
        except Exception as e:
            return False, f"ویرایش ناموفق بود : {e}"

    def remove(self, employee_id):
        try:
            self.employee_bl.remove(Converter.to_int(employee_id))
            return True, "کارمند حذف شد"
        except Exception as e:
            return False, f"حذف ناموفق بود : {e}"

    def find_by_id(self, employee_id):
        try:
            return True, self.employee_bl.find_by_id(Converter.to_int(employee_id))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_all(self):
        try:
            employee_list = self.employee_bl.find_all()
            return True, employee_list
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def find_all_rows(self):
        try:
            return True, self.employee_bl.find_all_rows()
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def next_id(self):
        return True, self.employee_bl.next_id()
