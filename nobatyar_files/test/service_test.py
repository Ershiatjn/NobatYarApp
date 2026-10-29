from business_logic.service_bl import ServiceBL
from controller.service_controller import ServiceController
from data_access.service_da import ServiceDa
from model.service import Service


service1 = Service(1, "جراحی", 160000, 60)
service2 = Service(2, "ویزیت", 80000, 30)
service3 = Service(3, "کاشت ناخن", 300000, 45)
# print(service1)
# print(service2)


# Test
# service_da = ServiceDa()
# print(service_da.find_all())
# service_da.save(service1)
# service_da.save(service2)
# print(service_da.find_all())

# Test
# bl = ServiceBL()
# bl.save(service3)
# print("Done")
# bl.save(service3)


# controller = ServiceController()
# success, message = controller.save(4, "ماساژ", 500000, 60)
# print(success)
# print(message)
