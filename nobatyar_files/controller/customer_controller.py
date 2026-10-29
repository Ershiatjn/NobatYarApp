from business_logic.customer_bl import CustomerBL
from model.customer import Customer
from tools.converter import Converter

# کنترلر مشتریان
class CustomerController:
    def __init__(self):
        self.customer_bl = CustomerBL()


    def save(self, customer_id, name, family, phone):
        try:
            customer = Customer(Converter.to_int(customer_id), name, family, Converter.to_english(phone))
            self.customer_bl.save(customer)
            return True, "مشتری ذخیره شد"
        except Exception as e:
            return False, f"ذخیره ناموفق بود : {e}"

    def edit(self, customer_id, name, family, phone):
        try:
            customer = Customer(Converter.to_int(customer_id), name, family, Converter.to_english(phone))
            self.customer_bl.edit(customer)
            return True, "مشتری ویرایش شد"
        except Exception as e:
            return False, f"ویرایش ناموفق بود : {e}"

    def remove(self, customer_id):
        try:
            self.customer_bl.remove(Converter.to_int(customer_id))
            return True, "مشتری حذف شد"
        except Exception as e:
            return False, f"حذف ناموفق بود : {e}"

    def find_by_id(self, customer_id):
        try:
            return True, self.customer_bl.find_by_id(Converter.to_int(customer_id))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_by_phone(self, phone):
        try:
            return True, self.customer_bl.find_by_phone(Converter.to_english(phone))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_all(self):
        try:
            customer_list = self.customer_bl.find_all()
            return True, customer_list
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def next_id(self):
        return True, self.customer_bl.next_id()
