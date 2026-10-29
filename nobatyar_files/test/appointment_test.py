from business_logic.appointment_bl import AppointmentBL
from controller.appointment_controller import AppointmentController
from data_access.appointment_da import AppointmentDa
from model.appointment import Appointment


appointment1 = Appointment(1, 1, 1, "1405/08/16", "08:00")
appointment2 = Appointment(2, 2, 1, "1405/08/16", "09:00")
# print(appointment1)
# print(appointment2)


# Test
# appointment_da = AppointmentDa()
# print(appointment_da.find_all())
# appointment_da.save(appointment1)
# print(appointment_da.find_all())

# Test
# bl = AppointmentBL()
# bl.save(appointment2)
# print("Done")
# print(bl.free_slots(1, "1405/08/16"))


# controller = AppointmentController()
# success, message = controller.save(3, 1, 1, "1405/08/16", "08:00")
# print(success)
# print(message)
# print(controller.cancel(1))
