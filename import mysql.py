import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    username = 'root',
    password = 'root',
    database = 'data_transfer',
    port = 3307
)

cursor = conn.cursor()
#creation

cursor.execute("create table employee1(id INT primary key, emp_name varchar(30), emp_desig varchar(40), salary INT);")
#insertion
cursor.execute("insert into employee1 values(101,'Alice', 'developer', 100000);")
cursor.execute("insert into employee1 values(102,'Bob', 'developer', 100000);")
cursor.execute("insert into employee1 values(103,'charlie', 'developer', 100000);")
#updation
cursor.execute("update employee1 set salary = '2000000' where id = 101;")

cursor.execute("delete from employee1 where id = 103;")

cursor.execute("drop table employee1;")

cursor.execute("select *from employee1;")
col = cursor.fetchall()
print(col)

cursor.close()
conn.close()

