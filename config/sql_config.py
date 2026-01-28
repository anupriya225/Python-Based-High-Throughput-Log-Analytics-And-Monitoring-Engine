import mysql.connector
from mysql.connector import Error

def database_connection():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anu@225",
        database="springboard",
        port=3306
    )
        if connection.is_connected():
            print("Connection successful!!")
            return connection
        else:
            print("Unable to connect!!")

    except Error as e:
        return (f"Error: {e}")

database_connection()