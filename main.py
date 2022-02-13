import os, time, encoding
from scratch2py import Scratch2Py
import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      connection.commit()
      print("Query successful")
      return "Query successful"
    except Error as err:
      print(f"Error: '{err}'")
      return err
sqlpw = os.environ['sqlpw']
sqlun = os.environ['sqlun']
con = create_db_connection("sql5.freemysqlhosting.net",sqlun,sqlpw,sqlun)
password = os.environ['password']
uname = os.environ['uname']
s2py = Scratch2Py(uname,password)
cloud = s2py.scratchConnect(os.environ['pid'])
while True:
  time.sleep(2)
  login = str(cloud.readCloudVar("cloud_login"))
  if login[:4] == "0001":
    print("Creating Account")
    username = encoding.decode(login[4:])
    print(username)
    query = "INSERT INTO `accounts` (`id`, `username`) VALUES (NULL, '" + username + "')"
    sql = execute_query(con, query)
    encoded = encoding.encode(f"{username}")
    if type(sql) == type(""):
      if sql.find("Duplicate entry") == -1:
        cloud.setCloudVar("cloud_login",f"0003{encoded}")
      elif sql == "Query successful":
        encoded = encoding.encode(f"{username}")
        cloud.setCloudVar("cloud_login",f"0002{encoded}")
    else:
      cloud.setCloudVar("cloud_login",f"0004{encoded}")
