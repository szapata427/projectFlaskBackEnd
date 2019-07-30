from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import abort
from flask import Flask, jsonify
import mysql.connector
import json
from sqlConnectionFile import hostName, userDBName, dbPasswrd, databaseName

app = Flask(__name__)

oneresumedatabase = mysql.connector.connect(
    host=hostName(),
    user=userDBName(),
    passwd=dbPasswrd(),
    database=databaseName()
)
mycursor = oneresumedatabase.cursor()


@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_users():
    query = "select * from oneresumedatabase.accountinformation"
    mycursor.execute(query)
    items = [dict(zip([ key[0] for key in mycursor.description ], row)) for row in mycursor]

    return ({'tasks': items})

if __name__ == '__main__':
    app.run(debug=False)




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









