from dependancies import *
from login import *
from mysql_connection import *
import pandas as pd


def create_table(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            column1 VARCHAR(255),
            column2 VARCHAR(255),
            column3 VARCHAR(255)
        )
    """)
    conn.commit()


# Function to insert data into MySQL table
#def insert_data(conn, data):
 #   cur.execute("""
  #      INSERT INTO my_table (column1, column2, column3) 
   #     VALUES (%s, %s, %s)
    #""", data)
   # conn.commit()

def upload_data(file):
    # Check file size
    if file.size > 10*1024*1024:  # 10MB limit
        st.error("File size exceeds the limit (10MB). Please upload a smaller file.")
        return
    
    # Read uploaded file
    df = pd.read_csv(file)
    
    
    df.to_sql('users_data', con=mysql.connector.connect(**config), if_exists='append', index=False)
    
    st.success("Data uploaded successfully!")

def home():
    st.markdown("""Welcome to the **Cloud Based Storage App**. This App will help you to store your files in cloud. But you have limit of 10MB. When your limit is reached you will not be able to upload file.""")
    
    