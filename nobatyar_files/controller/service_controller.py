from business_logic.service_bl import ServiceBL
from model.service import Service
from tools.converter import Converter

# کنترلر خدمات: ورودی های متنی فرم را به نوع درست تبدیل می کند و نتیجه را به صورت (موفق یا ناموفق، پیام) برمی گرداند
class ServiceController:
    def __init__(self):
        self.service_bl = ServiceBL()


    def save(self, service_id, title, price, duration):
        try:
            service = Service(Converter.to_int(service_id), title, Converter.to_int(price), Converter.to_int(duration))
            self.service_bl.save(service)
            return True, "خدمت ذخیره شد"
        except Exception as e:
            return False, f"ذخیره ناموفق بود : {e}"

    def edit(self, service_id, title, price, duration):
        try:
            service = Service(Converter.to_int(service_id), title, Converter.to_int(price), Converter.to_int(duration))
            self.service_bl.edit(service)
            return True, "خدمت ویرایش شد (قیمت جدید فقط برای نوبت های جدید اعمال می شود)"
        except Exception as e:
            return False, f"ویرایش ناموفق بود : {e}"

    def remove(self, service_id):
        try:
            self.service_bl.remove(Converter.to_int(service_id))
            return True, "خدمت حذف شد"
        except Exception as e:
            return False, f"حذف ناموفق بود : {e}"

    def find_by_id(self, service_id):
        try:
            return True, self.service_bl.find_by_id(Converter.to_int(service_id))
        except Exception as e:
            return False, f"جستجو ناموفق بود : {e}"

    def find_all(self):
        try:
            service_list = self.service_bl.find_all()
            return True, service_list
        except Exception as e:
            return False, f"خواندن اطلاعات ناموفق بود : {e}"

    def next_id(self):
        return True, self.service_bl.next_id()
