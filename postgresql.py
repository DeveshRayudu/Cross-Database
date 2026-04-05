import psycopg2

conn = None
cur = None
try:
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'data_transfer',
        user = 'postgres',
        password = 'root',
        port = 5432
        
    )
    if not conn:
        print("not connected")
    else:
        print("connected")
    cur = conn.cursor()
    if cur == True:
        print("cursor connected")
    else:
        print("cursor connected")
except Exception as e:
    print(e)
finally:
    try:
        cur.execute("create table employee(emp_id INT,emp_name varchar(40));")
        cur.execute("insert into employee values(101,'devesh');")
        cur.execute("select *from employee;")
        col=cur.fetchall()
        if col:
            print(col)
        else:
            print("fucked")
    except Exception as e:
        print(e)
    cur.close()
    conn.close()



