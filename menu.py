import re
import MySQLdb
import os


string = r'[a-zA-Z\s]+$'
emailReg = r'^[a-zA-z0-9]+@[a-z]+.[a-z]{2,4}$'


def mysqlconnect():
    # Trying to connect to the database
    try:
        con = MySQLdb.connect(
            "localhost", "root", "0000", "python")
    # If connection is not successful
    except:
        print("Unable to connect to database.")
        return 0
    # Making Cursor Object For Query Execution
    cursor = con.cursor()
    return con


# Function Call For Connecting To Our Database
mysqlconnect()


class Person:
    healthRate = 0

    def __init__(self, full_name, money, sleepmood, healthRate):
        self.full_name = full_name
        self.money = money
        self.sleepmood = sleepmood
        self.healthRate = healthRate

    # sleep method
    def sleep(self, hours):
        if hours == 7:
            self.sleepmood = 'happy'
            print('your sleepmood changed to happy')
        elif hours > 7:
            self.sleepmood = 'lazy'
            print('your sleepmood changed to lazy')
        elif hours < 7:
            self.sleepmood = 'tired'
            print('your sleepmood changed to tired')
            return self.sleepmood
        else:
            return 'please enter values in range'

    def sethealthRate(self, healthRate):
        if healthRate >= 0 and healthRate <= 100:
            self.healthRate = healthRate
        else:
            print('out of range')

    # eat method
    def eat(self, meals):
        if meals <= 3 and meals >= 1:
            if meals == 3:
                self.healthRate = '100'
                print('your healthRate changed to 100')
            elif meals == 2:
                self.healthRate = '75'
                print('your healthRate changed to 75')
            elif meals == 1:
                self.healthRate = '50'
                print('your healthRate changed to 50')
            return self.healthRate
        else:
            print('out of range')

    def buy(self, items):
        if items == 1:
            self.money -= 10
            print('Your money decreased by 10')


# employee class
class Employee(Person):

    def __init__(self, email, workmood, salary, is_manager, office_id):
        self.office_id = office_id
        self.email = email

        self.workmood = workmood
        if(salary < 1000):
            print('salary is too low, it must be 1000 or more')
        else:
            self.salary = salary
        self.is_manager = is_manager

    def sendEmail(self, to, subject, body, receiver_name):
        f = open('email.txt', 'w')
        f.write(f'email is sent to : {to} \n')
        f.write(f'email subject is :{subject} \n')
        f.write(f'email body is :{body} \n')
        f.write(f'email sender is : {receiver_name} \n')
        f.close()

    def work(self, hours):
        if hours == 8:
            self.workmood = 'happy'
            print('your workmood changed to happy')
        elif hours < 8:
            self.workmood = 'lazy'
            print('your workmood changed to lazy')
        elif hours > 8:
            self.workmood = 'tired'
            print('your workmood changed to tired')
        return self.workmood

    def fire_employee(cls, id):
        # fire employee by id
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "DELETE FROM employee WHERE id = " + str(id))
        cont.commit()
        return 'employee fired'


class Office():

    def __init__(self, name):
        self.name = name

    def get_all_employees(cls, id):
        # return all employees
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM employee WHERE office_id = " + str(id))
        myresult = mycursor.fetchall()
        return myresult

    def get_employee(cls, id):
        # get employee by id
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM employee WHERE id = " + str(id))
        myresult = mycursor.fetchall()
        return myresult

    def hire(self, employee, office_id):
        print(employee.email)

        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "INSERT INTO employee(email, workmood, salary, is_manager, office_id) VALUES ('" + employee.email + "','" + employee.workmood + "','" + str(employee.salary) + "','" + str(employee.is_manager) + "','" + str(office_id) + "')")
        cont.commit()
        cont.close()
        return 'employee hired'

    def add_office(self):
        # add office
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "INSERT INTO office(name) VALUES('" + self.name + "')")
        cont.commit
        return 'office added'
# ##############################################################################


def check_office_name(name):
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM office WHERE name = '" + name + "'")
    myresult = mycursor.fetchall()
    if(myresult):
        return False
    else:
        return True


def check_office_id(id):
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM office WHERE id = '" + id + "'")
    myresult = mycursor.fetchall()
    if(myresult):
        return False
    else:
        return True


def check_employee():
    emp_id = input("Enter Employee Id : ")
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True


def check_employeeWithoutID(emp_id):
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True


###############################################################################

def add_employee():

    email = input("Enter your Email : ")
    if not (re.match(emailReg, email)):
        print('invalid email')
        return

    workmood = input("Enter your Workmood : ")

    salary = input("Enter your Salary : ")
    if(int(salary) < 1000):
        print('salary is too low, it must be 1000 or more')
        return
    is_manager = input("If Manager press 1, if not press 0 : ")
    office_id = input("Enter your Office Id : ")
    if(check_office_id(office_id) == True):
        print('Office Id is not valid')
        return
    employee = Employee(email, workmood, int(
        salary), is_manager, office_id)
    office = Office(office_id)
    office.hire(employee, office_id)
    print('Employee added')


def add_office():
    name = input("Enter Office Name : ")
    if(check_office_name(name) == False):
        print('Office Name was already taken')
        return
    if(re.match(string, name) == False):
        print('Office Name is not valid')
        return
    office = Office(name)
    office.add_office()
    print('Office added')


def delete_employee():
    emp_id = input("Enter Employee Id : ")
    if(check_employeeWithoutID(emp_id)):
        Employee.fire_employee(emp_id)
        print('Employee deleted')
    else:
        print('Employee does not exist')


def get_all_employees():
    office_id = input("Enter Office Id : ")
    employees = Office.get_all_employees(office_id)
    for i in employees:
        print("Employee Id : ", i[0])
        print("Employee Email : ", i[1])
        print("Employee WorkMood : ", i[2])
        if(i[4] == 1):
            print("Employee Salary : Employee is Manager, You can't view his/her salary")
        else:
            print("Employee Salary : ", i[3])

        print("Employee Status(Manager) : ", bool(i[4]))
        print("Employee Office ID : ", i[5])
        print("Employee Reg Date: ", i[6])


def get_employee():
    emp_id = input("Enter Employee Id : ")
    if(check_employeeWithoutID(emp_id)):
        employees = Office.get_employee(emp_id)
        print("Employee Id : ", employees[0][0])
        print("Employee Email : ", employees[0][1])
        print("Employee WorkMood : ", employees[0][2])
        if(employees[0][4] == 1):
            print("Employee Salary : Employee is Manager, You can't view his/her salary")
        else:
            print("Employee Salary : ", employees[0][3])

        print("Employee Status(Manager) : ", bool(employees[0][4]))
        print("Employee Office ID : ", employees[0][5])
        print("Employee Reg Date: ", employees[0][6])
    else:
        print('Employee does not exist')


def print_menu():
    print("to hire employee press 1")
    print("to add office press 2")
    print("to fire employee press 3")
    print("to display all employees press 4")
    print("to display employee by id press 5")
    print("to exit press Q")


def menu():
    print_menu()
    ch = input("Enter your Choice: ")
    while(ch != 'Q'):
        os.system('cls')
        if(ch == '1'):
            add_employee()
        elif(ch == '2'):
            add_office()
        elif(ch == '3'):
            delete_employee()
        elif(ch == '4'):
            get_all_employees()
        elif(ch == '5'):
            get_employee()
        else:
            print("Invalid Choice")
        print_menu()
        ch = input("Enter your Choice: ")


menu()
