import mysql.connector
from sqlConnectionFile import sqlOneResumeDatabase



mycursor = sqlOneResumeDatabase()


    # sqlFormula = "INSERT INTO accountinformation (FirstName, LastName, Email, Address1, Address2, City, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # secondMember = ("Nichole", "Zapata", "nicholezapata@gmail.com", "110 Romain Ave", "null", "Pompton Lakes", "NJ", "USA")

    # mycursor.execute(sqlFormula, secondMember)
    # oneresumedatabase.commit()


mycursor.execute("select * from oneresumedatabase.accountinformation")
result = mycursor.fetchall()
print(result)
items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in result]
for entry in items: 
    print(entry)


