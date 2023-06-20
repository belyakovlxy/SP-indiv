import hashlib
import sqlite3
from flask_restful import reqparse


my_args = reqparse.RequestParser()
my_args.add_argument("login", type=str, help="login is not defined or has wrong type!")
my_args.add_argument("password", type=str, help="password is not defined or has wrong type!")
my_args.add_argument("avarage_mark", type=float, help="avarage_mark is not defined or has wrong type!")


def getAllStudents(name):
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''SELECT student.login, student.avarage_mark
    FROM student
    WHERE student.id IN (SELECT stud_to_teacher.student_id
                        FROM stud_to_teacher
                        WHERE stud_to_teacher.teacher_id = (SELECT teacher.id 
                                                            FROM teacher
                                                            WHERE teacher.login = \"{name}\"))'''.format(name = name)
    
    result = {"students" : []}
    
    res = dbcursour.execute(query)
    names = list(map(lambda x: x[0], dbcursour.description))
    for row in res:
        student = {}
        for i in range(len(names)):
            student[names[i]] = row[i]
        result["students"].append(student)

    con.close()
    return result


def addStudent(args, teacher_name):
    if args['login'] == None or args["password"] == None:
            return {"INFO" : "login or password was not entered"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    h = hashlib.new('sha256')
    h.update(bytes(args["password"], 'UTF-8'))


    query = '''INSERT INTO student (login, password, avarage_mark)
    VALUES (\"{name}\", \"{password}\", {mark})'''.format(name = args["login"], password = h.hexdigest(), mark = args["avarage_mark"])

    dbcursour.execute(query)

    query = '''INSERT INTO stud_to_teacher (student_id, teacher_id)
    VALUES ((SELECT student.id
            FROM student
            WHERE student.login = \"{name}\"), (SELECT teacher.id
                                        FROM teacher
                                        WHERE teacher.login = \"{teacher_name}\"));'''.format(name = args["login"], teacher_name = teacher_name)
    
    dbcursour.execute(query)


    con.commit()
    con.close()
    return {"INFO" : "Student {name} was added".format(name = args["login"])}



def updateStudentsMark(args, teacher_name):
    if args['login'] == None or args["avarage_mark"] == None:
            return {"INFO" : "login or avarage_mark was not entered"}
     
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()
    
    query = '''UPDATE student
    SET avarage_mark = {mark}
    WHERE student.login = \"{name}\" AND student.id IN (SELECT stud_to_teacher.student_id
                                                FROM stud_to_teacher
                                                WHERE stud_to_teacher.teacher_id = (SELECT teacher.id
                                                                                    FROM teacher
                                                                                    WHERE teacher.login = \"{teacher_name}\"))'''.format(name = args["login"], teacher_name = teacher_name, mark = args["avarage_mark"])

    dbcursour.execute(query)

    con.commit()
    con.close()
    return {"INFO" : "Student {name}'s mark was updated".format(name = args["login"])}


def deleteStudent(args, teacher_name):
    if args['login'] == None:
        return {"INFO" : "login was not entered"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''DELETE FROM stud_to_teacher
    WHERE stud_to_teacher.student_id = (SELECT student.id
                                        FROM student
                                        WHERE student.login = \"{name}\") AND stud_to_teacher.teacher_id = (SELECT teacher.id
                                                                                                    FROM teacher
                                                                                                    WHERE teacher.login = \"{teacher_name}\");'''.format(name = args["login"], teacher_name = teacher_name)
    dbcursour.execute(query)                          

    query = '''DELETE FROM student
    WHERE student.login = \"{name}\";'''.format(name = args["login"])

    dbcursour.execute(query) 

    con.commit()
    con.close()
    return {"INFO" : "Student {name} was deleted".format(name = args["login"])}



def getMarks(name):
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''SELECT student.avarage_mark
    FROM student
    WHERE student.login = \"{name}\"'''.format(name = name)

    res = dbcursour.execute(query)
    row = dbcursour.fetchone()

    con.close()
    return {"mark" : row[0]}

    


def loginQuery(args):
    if args['login'] == None or args["password"] == None:
            return {"INFO" : "login or password was not entered"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    h = hashlib.new('sha256')
    h.update(bytes(args["password"], 'UTF-8'))
    hashedPasswower = h.hexdigest()

    query = '''SELECT *
    FROM teacher
    WHERE teacher.login = \"{login}\" AND teacher.password = \"{password}\"'''.format(login = args["login"], password = hashedPasswower)

    res = dbcursour.execute(query)
    row = dbcursour.fetchone()
    print(row)
    if (row != None):
        return {"name" : args['login'], "role" : "teacher"}
    

    query = '''SELECT *
    FROM student
    WHERE student.login = \"{login}\" AND student.password = \"{password}\"'''.format(login = args["login"], password = hashedPasswower)

    res = dbcursour.execute(query)
    row = dbcursour.fetchone()

    con.close()
    if (row != None):
        return {"name" : args['login'], "role" : "student"}
    else:
        return {"INFO": "These's no user with this login and password"}



