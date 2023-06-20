from flask import Flask, make_response
from flask_restful import Api, Resource, request

import queries
import jwt_tokens
import sqlite3

app = Flask(__name__)
api = Api(app)


class Students(Resource):
    def get(self):
        verifyResult = jwt_tokens.verify("teacher")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            result = queries.getAllStudents(verifyResult["info"]["name"])
            return result
        
    def post(self):
        verifyResult = jwt_tokens.verify("teacher")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            result = queries.addStudent(args, verifyResult["info"]["name"])
            return result
        
    def put(self):
        verifyResult = jwt_tokens.verify("teacher")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            result = queries.updateStudentsMark(args, verifyResult["info"]["name"])
            return result
        
    def delete(self):
        verifyResult = jwt_tokens.verify("teacher")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            args = queries.my_args.parse_args()
            result = queries.deleteStudent(args, verifyResult["info"]["name"])
            return result

class Marks(Resource):
    def get(self):
        verifyResult = jwt_tokens.verify("")
        if "INFO" in verifyResult.keys():
            return verifyResult
        else:
            if verifyResult["info"]["role"] == "teacher":
                result = queries.getAllStudents(verifyResult["info"]["name"])
                return result
            else:
                result = queries.getMarks(verifyResult["info"]["name"])
                return result

class Authentication(Resource):
    def post(self):
        args = queries.my_args.parse_args()
        
        result = queries.loginQuery(args)
        response = ""
        if "INFO" in result.keys():
            response = make_response(result)
        else:
            token = jwt_tokens.createJWT(args["login"], args["password"])
            response = make_response({"INFO" : "You Logged In!"})
            response.set_cookie("my_token", token)
            response.set_cookie("my_role", result["role"])
            response.set_cookie("my_name", result["name"])
        return response

    def get(self):
        verifyResult = jwt_tokens.verify("")
        return verifyResult

api.add_resource(Students, "/students")
api.add_resource(Authentication, "/login")
api.add_resource(Marks, "/marks")

if __name__ == "__main__":
    app.run(debug=True)