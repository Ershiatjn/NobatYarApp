from business_logic.shift_bl import ShiftBL
from controller.shift_controller import ShiftController
from data_access.shift_da import ShiftDa
from model.shift import Shift


# روز هفته: 0 = شنبه ... 6 = جمعه
shift1 = Shift(1, 1, 1, 0, "08:00", "10:00")
shift2 = Shift(2, 1, 2, 1, "08:00", "10:00")
# print(shift1)
# print(shift2)


# Test
# shift_da = ShiftDa()
# print(shift_da.find_all())
# shift_da.save(shift1)
# print(shift_da.find_all())

# Test
# bl = ShiftBL()
# bl.save(shift2)
# print("Done")


# controller = ShiftController()
# success, message = controller.save(3, 1, 1, "شنبه", "09:00", "11:00")
# print(success)
# print(message)
