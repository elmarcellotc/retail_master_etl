import mysql.connector
import os


def initialize_conn():

    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = os.getenv("MYSQL_PORT")
    mysql_port = int(mysql_port)
    mysql_user = os.getenv("MYSQL_ETL_USER")
    mysql_password = os.getenv("MYSQL_ETL_PASSWORD")
    mysql_database = os.getenv("MYSQL_DATABASE")

    # Connect to MySQL
    conn = mysql.connector.connect(
        host=mysql_host,            
        port=mysql_port,
        user=mysql_user,            
        password=mysql_password,    
        database=mysql_database
    )

    return conn