from flask import Flask, request, Response
import requests
import json
from flask_restful import Resource,Api
import base64
import numpy
import os
import speech_recognition as sr
import scispacy
import spacy
from bisect import bisect_right
nlp = spacy.load("en_core_sci_sm") # load it at start time so that speed is maintained

app=Flask(__name__)
api=Api(app)

class q1(Resource):
    def post(self):
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            optionstemp=msg["options"]
            options={}
            for i in range(len(optionstemp)):
                options[optionstemp[i].lower()]=optionstemp[i]
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
        text=text.lower()

        if question_key=="q1":
            doc = nlp(text)
            all_diseases=list(doc.ents)
            for i in range(len(all_diseases)):
                all_diseases[i]=str(all_diseases[i])
            ans={"answers":[]}
            if len(all_diseases)==0 or (len(all_diseases)==1 and (all_diseases[0] in {"disease","fit","no disease","sick","not sick"})):
                
                if "none" in options:
                    ans["answers"]=options["none"]
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
                else:
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
            ansk=set()
            for i in all_diseases:
                k=i
                if "disease" in k and k!="disease":
                    k=k.split("disease")[0]
                elif k in options:
                    ansk.add(options[k])
                elif k!="disease":
                    ansk.add("others")
            if "others" in ansk:
                if "others" not in options:
                    ansk=ansk-{"others"}
                elif "others" in ansk:
                    ansk=ansk-{"others"}
                    ansk.add(options["others"])
            ans={"answers":list(ansk)}
            return Response(json.dumps(ans),status=200,mimetype="application/json")
            
        if question_key=="q2":
            array=[]
            allowed=[]
            n=0
            for i in options:
                allowed.append(options[i])
                options[i]=options[i].replace("lakh","")
                if "<" in options[i]:
                    array.append(float(options[i][1:]))
                elif ">" in options[i]:
                    array.append(float(options[i][:-1]))
                else:
                    array.append(float(options[i][options[i].find("-")+1:]))
                n+=1
            
            if "lac" in text:
                text=text.replace("lac","lakh")
            if "lack" in text:
                text=text.replace("lack","lakh")
            text=text.replace("lakh","")
            s=0
            if "half" in text:
                s=0
                index=0
                while(index<len(text) and text.isdigit()):
                    s=s*10+int(text[index])
                    index+=1
                s=s+0.5
            elif "point" in text:
                text=text.split("point")
                s=float(text[0].strip()+"."+text[1].strip())
            elif "." in text:
                text=text.split(".")
                s=float(text[0].strip()+"."+text[1].strip())
            else:
                s=float(text)
            pos=bisect_right(array,s)
            if pos!=n:
                ans={"answers":[allowed[pos]]}
            else:
                ans={"answers":[allowed[-1]]}
            return Response(json.dumps(ans),status=200,mimetype="application/json")
            
        if question_key=="q3":
            pass

        os.system("del finale.wav")

api.add_resource(q1,"/v1/api")

if __name__=="__main":
    app.run(debug=True)



