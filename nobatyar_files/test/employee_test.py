from business_logic.employee_bl import EmployeeBL
from controller.employee_controller import EmployeeController
from data_access.employee_da import EmployeeDa
from model.employee import Employee


employee1 = Employee(1, "علی", "احمدی", [1, 2])
employee2 = Employee(2, "رضا", "کریمی", [3])
# print(employee1)
# print(employee2)


# Test
# employee_da = EmployeeDa()
# print(employee_da.find_all())
# employee_da.save(employee1)
# print(employee_da.find_all())

# Test
# bl = EmployeeBL()
# bl.save(employee2)
# print("Done")


# controller = EmployeeController()
# success, message = controller.save(3, "سارا", "محمدی", "1,2")
# print(success)
# print(message)
