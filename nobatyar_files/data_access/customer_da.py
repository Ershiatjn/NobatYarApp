import os
import pickle

# ذخیره و خواندن اطلاعات مشتریان از فایل
class CustomerDa:
    def __init__(self):
        self.filename = "data_access/data/customers.dat"
        self.customer_list = self.find_all()

    def save(self, customer):
        self.customer_list = self.find_all()
        self.customer_list.append(customer)
        self.write_file()

    def edit(self, customer):
        self.customer_list = self.find_all()
        for index in range(len(self.customer_list)):
            if self.customer_list[index].customer_id == customer.customer_id:
                self.customer_list[index] = customer
        self.write_file()

    def remove(self, customer_id):
        self.customer_list = self.find_all()
        new_list = []
        for customer in self.customer_list:
            if customer.customer_id != customer_id:
                new_list.append(customer)
        self.customer_list = new_list
        self.write_file()

    def find_by_id(self, customer_id):
        for customer in self.find_all():
            if customer.customer_id == customer_id:
                return customer
        return None

    def find_all(self):
         if not os.path.exists(self.filename):
            return []
         else:
            file = open(self.filename, "rb")
            customer_list = pickle.load(file)
            file.close()
            return customer_list

    def write_file(self):
        os.makedirs("data_access/data", exist_ok=True)
        file = open(self.filename, "wb")
        pickle.dump(self.customer_list, file)
        file.close()
