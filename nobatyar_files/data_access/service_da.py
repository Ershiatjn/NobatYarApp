import os
import pickle

# ذخیره و خواندن اطلاعات خدمات از فایل
class ServiceDa:
    def __init__(self):
        self.filename = "data_access/data/services.dat"
        self.service_list = self.find_all()

    def save(self, service):
        self.service_list = self.find_all()
        self.service_list.append(service)
        self.write_file()

    def edit(self, service):
        self.service_list = self.find_all()
        for index in range(len(self.service_list)):
            if self.service_list[index].service_id == service.service_id:
                self.service_list[index] = service
        self.write_file()

    def remove(self, service_id):
        self.service_list = self.find_all()
        new_list = []
        for service in self.service_list:
            if service.service_id != service_id:
                new_list.append(service)
        self.service_list = new_list
        self.write_file()

    def find_by_id(self, service_id):
        for service in self.find_all():
            if service.service_id == service_id:
                return service
        return None

    def find_all(self):
         if not os.path.exists(self.filename):
            return []
         else:
            file = open(self.filename, "rb")
            service_list = pickle.load(file)
            file.close()
            return service_list

    def write_file(self):
        os.makedirs("data_access/data", exist_ok=True)
        file = open(self.filename, "wb")
        pickle.dump(self.service_list, file)
        file.close()
