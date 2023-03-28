import mysql.connector
import random

new_user = "user_test2"
new_pass = "ahhhhhhhh2"
new_id = random.randint(10000000, 100000000)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="S*0pW!JR",
    database = "tester",
    autocommit = True
)

mycursor = mydb.cursor()
mycursor.execute("SELECT username FROM accounts")
myresult = mycursor.fetchall()
print(myresult)

for x in myresult[:]:
    print(x[0])
    if new_id == x[0]:
        new_id = random.randint(10000000, 100000000)
        break

sql = "INSERT INTO accounts (id,username,password) VALUES (%s, %s, %s)"
val = (new_id, new_user, new_pass)

mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted")
mycursor.close()