import mysql.connector

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Omm@ir510219900',
    'database': 'cloud_assignment'
}

# Establish a connection
connection = mysql.connector.connect(**config)
cur = connection.cursor()