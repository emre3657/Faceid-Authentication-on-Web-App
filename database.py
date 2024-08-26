import mysql.connector

def connectDatabase():
    # MySQL bağlantısı oluşturma
    mydb = mysql.connector.connect(
    host="localhost", 
    port="3306",
    user="root",
    password="********",
    database="********"
    )
    mycursor = mydb.cursor()
    return mycursor, mydb