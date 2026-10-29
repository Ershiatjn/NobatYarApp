from business_logic.customer_bl import CustomerBL
from controller.customer_controller import CustomerController
from data_access.customer_da import CustomerDa
from model.customer import Customer


customer1 = Customer(1, "سارا", "محمدی", "09121234567")
customer2 = Customer(2, "نیما", "رضایی", "09123456789")
# print(customer1)
# print(customer2)


# Test
# customer_da = CustomerDa()
# print(customer_da.find_all())
# customer_da.save(customer1)
# print(customer_da.find_all())

# Test
# bl = CustomerBL()
# bl.save(customer2)
# print("Done")
# bl.save(customer2)


# controller = CustomerController()
# success, message = controller.save(3, "مریم", "کریمی", "0912")
# print(success)
# print(message)
