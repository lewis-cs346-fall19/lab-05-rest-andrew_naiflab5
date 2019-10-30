#!/usr/bin/python3
import cgi
import cgitb
import os
import json
cgitb.enable()
import passwords
import MySQLdb

def jsonFunc():
    print("Content-type: application/json")
    print("Status: 200 OK")
    print()
    x = [1,2,3,4, {"foo": "bar"}]
    x_json = json.dumps(x, indent=2)
    print(x_json)

def course():
    print("Content-type: application/json")
    print("Status: 200 OK")
    print()
    conn = MySQLdb.connect(host   = passwords.SQL_HOST,
	                   user   = passwords.SQL_USER,
	                   passwd = passwords.SQL_PASSWD,
	                   db     = "courses")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM school")
    all = cursor.fetchall()
    cursor.close()
    entries = []
    for entry in all:
        entries.append({
            "id": entry[0],
            "department": entry[1],
            "course": entry[2],
            "units": entry[3]
        })
    all_json = json.dumps(entries, indent=2)
    print(all_json)

def courseFinder(x):
    print("Content-type: application/json")
    print("Status: 200 OK")
    print()
    conn1 = MySQLdb.connect(host   = passwords.SQL_HOST,
                            user   = passwords.SQL_USER,
                            passwd = passwords.SQL_PASSWD,
                            db     = "courses")
    cursor = conn1.cursor()
    cursor.execute("SELECT * FROM school WHERE id={}".format(x))
    all = cursor.fetchall()
    cursor.close()
    entries = []
    for entry in all:
        entries.append({
            "id": entry[0],
            "department": entry[1],
            "course": entry[2],
            "units": entry[3]
        })
    all_json = json.dumps(entries, indent=2)
    print(all_json)
def postCourse(data):
    fields = data.split("&")
    f = [field.split("=")[1] for field in fields]
    conn1 = MySQLdb.connect(host   = passwords.SQL_HOST,
                            user   = passwords.SQL_USER,
                            passwd = passwords.SQL_PASSWD,
                            db     = "courses")
    cursor = conn1.cursor()
    cursor.execute('INSERT INTO school(dept, course, units) VALUES("{}","{}","{}")'.format(f[0], f[1], f[2]))
    new_id = cursor.lastrowid
    cursor.close()
    conn1.commit()
    conn1.close()
    print("Status: 302 Redirect")
    print("Location: /cgi-bin/rest.cgi/courses/{}".format(new_id))
    print()
try:
	path = os.environ['PATH_INFO']
except:
	path = "error"

if path == "error":
	print("Status: 302 Redirect")
	print("Location: rest.cgi/")
	print()
elif path == "/course-form" or path == "/course-form/":
    print("Content-type: text/html")
    print("Status: 200 OK")
    print()

    print("""<html><body>
    <form action="courses/" method=POST>
    <p>Department:
    <br><input type=text   name="dept">
    <p>Course:
    <br><input type=text   name="course">
    <p>Units:
    <br><input type=number name="credits">
    <input type=submit>
    </form></body></html>""")

else:
    if(path == "/json"):
        jsonFunc()
    if(path == "/courses" or path == "/courses/"):
	    if os.environ['REQUEST_METHOD'] == "POST":
	        postCourse(input())
	    else:
	        course()

    if path.startswith("/courses/"):
        try:
	        num = int(path[9:])
	        courseFinder(num)
        except:
            if os.environ['REQUEST_METHOD'] == "POST":
                postCourse(input())
            