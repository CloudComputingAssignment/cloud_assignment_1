import mysql.connector

config = {
    'host':'cloud-assignment-1.database.windows.net',
    'port':'1433'
    'user':'ommair-01',
    'password':'Omm@ir510219900',
    'database':'cloud-assignment'
}

# Establish a connection
connection = mysql.connector.connect(**config)
cur = connection.cursor()
