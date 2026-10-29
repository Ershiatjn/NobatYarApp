import os
import pickle

# ذخیره و خواندن اطلاعات شیفت‌ها از فایل
class ShiftDa:
    def __init__(self):
        self.filename = "data_access/data/shifts.dat"
        self.shift_list = self.find_all()

    def save(self, shift):
        self.shift_list = self.find_all()
        self.shift_list.append(shift)
        self.write_file()

    def edit(self, shift):
        self.shift_list = self.find_all()
        for index in range(len(self.shift_list)):
            if self.shift_list[index].shift_id == shift.shift_id:
                self.shift_list[index] = shift
        self.write_file()

    def remove(self, shift_id):
        self.shift_list = self.find_all()
        new_list = []
        for shift in self.shift_list:
            if shift.shift_id != shift_id:
                new_list.append(shift)
        self.shift_list = new_list
        self.write_file()

    def find_by_id(self, shift_id):
        for shift in self.find_all():
            if shift.shift_id == shift_id:
                return shift
        return None

    def find_all(self):
         if not os.path.exists(self.filename):
            return []
         else:
            file = open(self.filename, "rb")
            shift_list = pickle.load(file)
            file.close()
            return shift_list

    def write_file(self):
        os.makedirs("data_access/data", exist_ok=True)
        file = open(self.filename, "wb")
        pickle.dump(self.shift_list, file)
        file.close()
