import mysql.connector as mysql
import cred

db = mysql.connect(
    host = cred.db_host,
    user = cred.db_user,
    passwd = cred.db_pass,
    database = cred.db
)


