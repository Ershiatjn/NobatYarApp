import os
import pickle

# ذخیره و خواندن اطلاعات کارمندان از فایل
class EmployeeDa:
    def __init__(self):
        self.filename = "data_access/data/employees.dat"
        self.employee_list = self.find_all()

    def save(self, employee):
        self.employee_list = self.find_all()
        self.employee_list.append(employee)
        self.write_file()

    def edit(self, employee):
        self.employee_list = self.find_all()
        for index in range(len(self.employee_list)):
            if self.employee_list[index].employee_id == employee.employee_id:
                self.employee_list[index] = employee
        self.write_file()

    def remove(self, employee_id):
        self.employee_list = self.find_all()
        new_list = []
        for employee in self.employee_list:
            if employee.employee_id != employee_id:
                new_list.append(employee)
        self.employee_list = new_list
        self.write_file()

    def find_by_id(self, employee_id):
        for employee in self.find_all():
            if employee.employee_id == employee_id:
                return employee
        return None

    def find_all(self):
         if not os.path.exists(self.filename):
            return []
         else:
            file = open(self.filename, "rb")
            employee_list = pickle.load(file)
            file.close()
            return employee_list

    def write_file(self):
        os.makedirs("data_access/data", exist_ok=True)
        file = open(self.filename, "wb")
        pickle.dump(self.employee_list, file)
        file.close()
