import mysql.connector
from sqlConnectionFile import hostName, userDBName, dbPasswrd, databaseName


oneresumedatabase = mysql.connector.connect(
    host=hostName(),
    user=userDBName(),
    passwd=dbPasswrd(),
    database=databaseName()
)
mycursor = oneresumedatabase.cursor()

mycursor.execute("select * from oneresumedatabase.accountinformation")
result = mycursor.fetchall()
print(result)
items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in result]
for entry in items: 
    print(entry)


