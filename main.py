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
def execute_query(connection, query, getRecords=False):
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      if getRecords:
        return cursor.fetchall()
      else:
        connection.commit()
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
process_id = 0
def getIdOfUser(user):
  query = f"SELECT id FROM accounts WHERE username='{uname}';"
  id = execute_query(con, query, True)[0][0]
  return id
while True:
  time.sleep(2)
  login = str(cloud.readCloudVar("cloud_login"))
  code = login[:4]
  
  #Create Account
  if code == "0001":
    process_id+=1
    uname = encoding.decode(login[4:])
    print(f"({process_id}) Create Account: {uname}")
    query = f"INSERT INTO `accounts` (`id`, `username`) VALUES (NULL, '{uname}')"
    sql = execute_query(con, query)
    encoded = encoding.encode(f"{uname}")
    if type(sql) == type(""):
      if sql.find("Duplicate entry") == -1:
        cloud.setCloudVar("cloud_login",f"0003{encoded}")
        print(f"({process_id}) Create Account Error: Already have an account")
      elif sql == "Query successful":
        encoded = encoding.encode(f"{uname}")
        cloud.setCloudVar("cloud_login",f"0002{encoded}")
        print(f"({process_id}) Create Account: Account Created")
    else:
      cloud.setCloudVar("cloud_login",f"0004{encoded}")
      print(f"({process_id}) Create Account Error: Unknown")
    print(f"({process_id}) Interaction Ended: Interaction Ended")
      
  # Login
  if code == "0005":
    process_id+=1
    uname = encoding.decode(login[4:])
    print(f"({process_id}) Login: {uname}")
    query = f"SELECT username FROM accounts WHERE username='{uname}';"
    accExist = execute_query(con, query, True)[0] == (uname,)
    if accExist:
      cloud.setCloudVar("cloud_login",f"0007{login[4:]}")
      print(f"({process_id}) Login: Loged in")
    else:
      cloud.setCloudVar("cloud_login",f"0006{login[4:]}")
      print(f"({process_id}) Login: Account doesnt exist")
    print(f"({process_id}) Interaction Ended: Interaction Ended")

  #Get Notes
  if code == "0008":
    process_id+=1
    uname = encoding.decode(login[4:])
    print(f"({process_id}) Get Notes: {uname}")
    id = getIdOfUser(uname)
    query = f"SELECT data FROM notes WHERE id='{id}';"
    notes = execute_query(con, query, True)[0]
    for note in notes:
      time.sleep(1)
      note = encoding.encode(note)
      cloud.setCloudVar("cloud_login",f"0009{login[4:]}00{note}")
    time.sleep(1)
    cloud.setCloudVar("cloud_login","0")
    print(f"({process_id}) Interaction Ended: Interaction Ended")
      