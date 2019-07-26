import mysql.connector



oneresumedatabase = mysql.connector.connect(
    host="oneresume.c377pisenp9n.us-east-2.rds.amazonaws.com",
    user="oneresumemaster",
    passwd="colombia10",
    database="oneresumedatabase"
)

    # print(mydb)

mycursor = oneresumedatabase.cursor()


    # sqlFormula = "INSERT INTO accountinformation (FirstName, LastName, Email, Address1, Address2, City, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # secondMember = ("Nichole", "Zapata", "nicholezapata@gmail.com", "110 Romain Ave", "null", "Pompton Lakes", "NJ", "USA")

    # mycursor.execute(sqlFormula, secondMember)
    # oneresumedatabase.commit()


mycursor.execute("select * from oneresumedatabase.accountinformation")

for entry in mycursor: 
    print(entry)


