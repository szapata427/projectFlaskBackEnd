import mysql.connector


def sqlOneResumeDatabase():
    oneresumedatabase = mysql.connector.connect(
        host="oneresume.c377pisenp9n.us-east-2.rds.amazonaws.com",
        user="oneresumemaster",
        passwd="colombia10",
        database="oneresumedatabase"
    )

    mycursor = oneresumedatabase.cursor()

    return mycursor