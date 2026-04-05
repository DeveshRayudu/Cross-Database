import mysql.connector
import psycopg2
import cx_Oracle



def connect_database(db_type):
    if db_type == 'mysql':
        conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='root',
            database='data_transfer',
            port=3307
        )

    elif db_type == 'postgresql':
        conn = psycopg2.connect(
            host='localhost',
            database='data_transfer',
            user='postgres',
            password='root',
            port=5432
        )

    elif db_type == 'oracle':
        dsn = cx_Oracle.makedsn("localhost", 1521, sid="XE")
        conn = cx_Oracle.connect(
            user="system",
            password="manager",
            dsn=dsn
        )

    return conn, conn.cursor()