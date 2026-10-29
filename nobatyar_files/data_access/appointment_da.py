import os
import pickle

# ذخیره و خواندن اطلاعات نوبت‌ها از فایل
class AppointmentDa:
    def __init__(self):
        self.filename = "data_access/data/appointments.dat"
        self.appointment_list = self.find_all()

    def save(self, appointment):
        self.appointment_list = self.find_all()
        self.appointment_list.append(appointment)
        self.write_file()

    def edit(self, appointment):
        self.appointment_list = self.find_all()
        for index in range(len(self.appointment_list)):
            if self.appointment_list[index].appointment_id == appointment.appointment_id:
                self.appointment_list[index] = appointment
        self.write_file()

    def remove(self, appointment_id):
        self.appointment_list = self.find_all()
        new_list = []
        for appointment in self.appointment_list:
            if appointment.appointment_id != appointment_id:
                new_list.append(appointment)
        self.appointment_list = new_list
        self.write_file()

    def find_by_id(self, appointment_id):
        for appointment in self.find_all():
            if appointment.appointment_id == appointment_id:
                return appointment
        return None

    def find_all(self):
         if not os.path.exists(self.filename):
            return []
         else:
            file = open(self.filename, "rb")
            appointment_list = pickle.load(file)
            file.close()
            return appointment_list

    def write_file(self):
        os.makedirs("data_access/data", exist_ok=True)
        file = open(self.filename, "wb")
        pickle.dump(self.appointment_list, file)
        file.close()
