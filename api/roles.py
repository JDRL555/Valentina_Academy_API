from rolepermissions.roles import AbstractUserRole

class Student(AbstractUserRole):
    available_permissions = {
        'get_courses': True,
    }

class Teacher(AbstractUserRole):
    available_permissions = {
        'GET': True,
        'CURSE':True,
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'GET': True,
        'CURSE': True,
        'RECIPES': True,
        'SURVEY':True,
        'USERS':True,
       
    }