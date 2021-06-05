from flask import Flask, request, Response
import requests
import json
from flask_restful import Resource,Api

app=Flask(__name__)
api=Api(app)

class q1(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            options=msg["options"]
            audio=msg["audio"]
        except:
            return Response({},status=400,mimetype="application/json")
        
        
        


class q2(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            options=msg["options"]
            audio=msg["audio"]
        except:
            return Response({},status=400,mimetype="application/json")
        

class q3(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            options=msg["options"]
            audio=msg["audio"]
        except:
            return Response({},status=400,mimetype="application/json")

api.add_resource(q1,"/v1/api/q1")
api.add_resource(q2,"/v1/api/q2")
api.add_resource(q3,"/v1/api/q3")

if __name__=="__main":
    app.run(debug=True)



