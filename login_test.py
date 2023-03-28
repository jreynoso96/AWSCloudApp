import mysql.connector
import random

user = "user_test"
password = "ahhhhh"
new_id = 1234

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="S*0pW!JR",
    database = "tester",
    autocommit = True
)

mycursor = mydb.cursor()
mycursor.execute("SELECT id FROM accounts")
myresult = mycursor.fetchall()

#new_id = random.randint(1000,10000)

while new_id in myresult[:][0]:
    new_id = random.randint(1000, 10000)

mycursor.execute("SELECT password FROM accounts WHERE username = '" + str(user) + "'")
myresult = mycursor.fetchall()

if password == myresult[0][0]:
    print(True)
else: False

#sql = "INSERT INTO accounts (id,username,password) VALUES (%s, %s, %s)"
#val = (new_id, "dummy2", "helloWorld2")

#mycursor.execute(sql, val)
#mydb.commit()

#print(mycursor.rowcount, "record inserted")
mycursor.close()