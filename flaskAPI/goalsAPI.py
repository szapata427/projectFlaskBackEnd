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






goals_api = Blueprint('goals_api', __name__)

oneresumedatabase = mysql.connector.connect(
    host=hostName(),
    user=userDBName(),
    passwd=dbPasswrd(),
    database=databaseName()
)
mycursor = oneresumedatabase.cursor()


@goals_api.route('/saveyourfuture/api/v1.0/Goals', methods=['GET'])
@cross_origin()
def get_user_goals():
    try:
        query = "select * from oneresumedatabase.Goals"
        mycursor.execute(query)
        items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in mycursor]

    except mysql.connector.Error as error:
        stringerror = str(error)
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )
                        
    return ({'result': items})



@goals_api.route('/saveyourfuture/api/v1.0/AddGoal', methods=['POST'])
@cross_origin()
def add_goal_for_user():

    try:

        print(request.args)
        data = request.get_json()

        userDBId = data["UserId"]
        amount = data["Amount"]
        goalName = data["Name"]
        endDate = data["EndDate"]
        notes = data["Notes"]


        sql = "INSERT INTO oneresumedatabase.Goals (UserId, Amount, Name, Notes, EndDate) VALUES (%s, %s, %s, %s, %s)"        
        values = (userDBId, amount, goalName, notes, endDate )
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
    "Name": goalName,
    "Notes": notes,
    "EndDate": endDate,
    "RowsAdded":mycursor.rowcount,
    "Id":mycursor.lastrowid,
    "CreatedOn": datetimeCreated
    }

    return jsonify(
        result=dataReturned
    )



@goals_api.route('/saveyourfuture/api/v1.0/UsersGoals')
@cross_origin()
def search_goals_for_user():
    userId = request.args.get('UserId')

    try:
        sql = f"SELECT * FROM oneresumedatabase.Goals WHERE UserId={userId} ORDER BY DateCreated DESC"

        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if myresult is None:
            return jsonify(
                result=None
            )


    except Exception as error:
        stringerror = str(error)
        errormessage = {"Error": stringerror}            
        return jsonify(
            result=errormessage
        )


    all_entries = []
    print(myresult)
    for entry in myresult:
        record = {
        "Id":entry[0],
        "Name":entry[1],
        "Notes":entry[2],
        "Amount": str(entry[3]),
        "EndDate": entry[4],
        "CreatedOn": entry[5],
        "UsedId": entry[6]
        }
        all_entries.append(record)


    return jsonify(
        result=all_entries
    )



    