from flask import Flask, request, Response
import requests
import json
from flask_restful import Resource,Api
import base64
import numpy
import os
import speech_recognition as sr

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
        final_file=open("written.ogg","wb")
        final_file.write(base64.b64decode(audio))
        final_file.close()
        os.system("ffmpeg -i written2.ogg finale.wav")
        r=sr.Recognizer()
        spoken=sr.AudioFile('finale.wav')
        with spoken as source:
            audio=r.record(source)
        text=r.recognize_google(audio)
        print(text)
        os.system("del finale.wav")

class q2(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            options=msg["options"]
            audio=msg["audio"]
        except:
            return Response({},status=400,mimetype="application/json")
        final_file=open("written.ogg","wb")
        final_file.write(base64.b64decode(audio))
        final_file.close()
        os.system("ffmpeg -i written2.ogg finale.wav")
        r=sr.Recognizer()
        spoken=sr.AudioFile('finale.wav')
        with spoken as source:
            audio=r.record(source)
        text=r.recognize_google(audio)
        print(text)
        os.system("del finale.wav")
        

class q3(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            options=msg["options"]
            audio=msg["audio"]
        except:
            return Response({},status=400,mimetype="application/json")
        final_file=open("written.ogg","wb")
        final_file.write(base64.b64decode(audio))
        final_file.close()
        os.system("ffmpeg -i written2.ogg finale.wav")
        r=sr.Recognizer()
        spoken=sr.AudioFile('finale.wav')
        with spoken as source:
            audio=r.record(source)
        text=r.recognize_google(audio)
        print(text)
        os.system("del finale.wav")

api.add_resource(q1,"/v1/api/q1")
api.add_resource(q2,"/v1/api/q2")
api.add_resource(q3,"/v1/api/q3")

if __name__=="__main":
    app.run(debug=True)



