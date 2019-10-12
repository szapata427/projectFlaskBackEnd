from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import abort
from flask import Flask, jsonify, request
import mysql.connector
import json
from sqlConnectionFile import hostName, userDBName, dbPasswrd, databaseName
import requests
from mysql.connector.errors import Error
from flask_cors import CORS, cross_origin
from flask import Blueprint
import datetime






transaction_api = Blueprint('transaction_api', __name__)


oneresumedatabase = mysql.connector.connect(
    host=hostName(),
    user=userDBName(),
    passwd=dbPasswrd(),
    database=databaseName()
)
mycursor = oneresumedatabase.cursor()

@transaction_api.route('/saveyourfuture/api/v1.0/tranasctions', methods=['GET'])
@cross_origin()
def get_user_transactions():
    try:
        query = "select * from oneresumedatabase.UserTransactions"
        mycursor.execute(query)
        items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in mycursor]

    except mysql.connector.Error as error:
        stringerror = str(error)
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )
                        
    return ({'result': items})

@transaction_api.route('/saveyourfuture/api/v1.0/AddTransaction', methods=['POST'])
@cross_origin()

def add_transaction_for_user():

    
    try:

        print(request.args)
        data = request.get_json()

        userDBId = data["UserId"]
        amount = data["Amount"]
        transactionType = data["Type"]
        notes = data["Notes"]
        goalId = data["GoalId"]
        sql = "INSERT INTO oneresumedatabase.UserTransactions (UserId, Amount, Type, Notes, GoalId) VALUES (%s, %s, %s, %s, %s)"        
        values = (userDBId, amount, transactionType, notes, goalId)
        mycursor.execute(sql, values)
        oneresumedatabase.commit()
        datetimeCreated = datetime.datetime.now()

        print(mycursor)
        print(mycursor.rowcount, "record inserted.")


    except Exception as error:
        stringerror = str(error)
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )

    dataReturned = {
    "Success": True,
    "UserId":userDBId,
    "Amount":amount,
    "TransactionType":transactionType,
    "Notes": notes,
    "RowsAdded":mycursor.rowcount,
    "Id":mycursor.lastrowid,
    "CreatedOn": datetimeCreated,
    "GoalId": goalId
    }

    return jsonify(
        result=dataReturned
    )


@transaction_api.route('/saveyourfuture/api/v1.0/UsersTransactions')
@cross_origin()
def users_transacttions():
    userId = request.args.get('UserId')
    lastDays = request.args.get('LastDays')

    try:
        sql = f"SELECT * FROM oneresumedatabase.UserTransactions WHERE UserId={userId} ORDER BY CreatedOn DESC"

        if lastDays:
            daysToDisplay = datetime.datetime.now() - datetime.timedelta(days=int(lastDays))
            dateForSql = daysToDisplay.date().isoformat()
            sql = f"SELECT * FROM oneresumedatabase.UserTransactions WHERE UserId={userId} and CreatedOn >= '{dateForSql}' ORDER BY CreatedOn DESC"

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if myresult is None:
            return jsonify(
                result=None
            )
    except mysql.connector.Error as error:
        stringerror =  str(error)            
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )

    all_entries = []
    for entry in myresult:
        record = {
            "Id": entry[0],
            "UserId": entry[1],
            "Amount": entry[2],
            "Type": entry[3],
            "CreatedOn": entry[4],
            "Notes": entry[5],
            }
        all_entries.append(record)

    return jsonify(
        result=all_entries
    )




# if __name__ == '__main__':
#     transaction_api.run(debug=True)