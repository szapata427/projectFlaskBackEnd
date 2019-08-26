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
        sql = "INSERT INTO oneresumedatabase.UserTransactions (UserId, Amount, Type, Notes) VALUES (%s, %s, %s, %s)"        
        values = (userDBId, amount, transactionType, notes)
        mycursor.execute(sql, values)

        print(mycursor.rowcount, "record inserted.")

        oneresumedatabase.commit()
    except mysql.connector.Error as error:
        stringerror = str(error)
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )

    dataReturned = {
    "Email":userDBId,
    "LastName":amount,
    "FirstName":transactionType,
    "Notes": notes,
    "count":mycursor.rowcount,
    "Id":mycursor.lastrowid
    }

    return jsonify(
        result=dataReturned
    )



# if __name__ == '__main__':
#     transaction_api.run(debug=True)