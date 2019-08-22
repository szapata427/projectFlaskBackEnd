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



app = Flask(__name__)
# CORS(app, support_credentials=True)


oneresumedatabase = mysql.connector.connect(
    host=hostName(),
    user=userDBName(),
    passwd=dbPasswrd(),
    database=databaseName()
)
mycursor = oneresumedatabase.cursor()





@app.route('/saveyourfuture/api/v1.0/users', methods=['GET'])
@cross_origin()
def get_users():
    try:
        query = "select * from oneresumedatabase.Users"
        mycursor.execute(query)
        items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in mycursor]

    except mysql.connector.Error as error:
        return jsonify(
            result=error
                        ) 
    return ({'tasks': items})


# search specific user by email
@app.route('/saveyourfuture/api/v1.0/SearchUserEmail')
@cross_origin()
def search_user():
    userEmail = request.args.get('email')
    try:
        sql = f"SELECT * FROM oneresumedatabase.Users where Email='{userEmail}'"
        mycursor.execute(sql)
        myresult = mycursor.fetchone()

    except mysql.connector.Error as error:
        stringerror =  str(error)            
        return jsonify(
            result=stringerror
        )
    dataToReturn = {
        "Id": myresult[0],
        "FirstName": myresult[1],
        "LastName": myresult[2],
        "Email": myresult[3]
    }
    return jsonify(
        result=dataToReturn
    )

@app.route('/saveyourfuture/api/v1.0/NewUser', methods=['POST'])
@cross_origin()
def add_user():
    
    print(request.args)
    data = request.get_json()

    email = data["Email"]
    lastname = data["LastName"]
    firstName = data["FirstName"]
    try:
        sql = "INSERT INTO oneresumedatabase.Users (FirstName, Email, LastName) VALUES (%s, %s, %s)"        
        values = (firstName, email, lastname)
        mycursor.execute(sql, values)

        print(mycursor.rowcount, "record inserted.")

        oneresumedatabase.commit()
    except mysql.connector.Error as error:
        stringerror = str(error)            
        return jsonify(
            result=stringerror
        )

    return jsonify(
        Email=email,
        LastName=lastname,
        FirstName=firstName,
        count=mycursor.rowcount,
        Id=mycursor.lastrowid
    )


        


if __name__ == '__main__':
    app.run(debug=True)

# app = Flask(__name__)
# api = Api(app)

# class CreateUser(Resource):
#     def post(self):
#         try:
#             parser = reqparse.RequestParser()
#             parser.add_argument('Email', type=str)
#             parser.add_argument('Password', type=str)
#             parser.add_argument('Firstname', type=str)

#             args = parser.parse_args()

#             _userEmail = args['Email']
#             _userPassword = args['Password']
#             _userFirstName = args["FirstName"]

#             return {'Email': args["Email"], "Password": args["Password"], "FirstName": args["FirstName"] }
#         except Exception as e:
#             return {'error': str(e) }



# api.add_resource(CreateUser, '/CreateUser')

# if __name__ == '__main__':
#     app.run(debug=False, host = '0.0.0.0',port=5005)









