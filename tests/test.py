from clinic.controller import Controller

controller = Controller()
controller.login("user", "123456")
print(controller.list_patients())