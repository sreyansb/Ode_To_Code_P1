from flask import Flask, request, Response
import requests
from pydub import AudioSegment
import json
from flask_restful import Resource,Api
import base64
import numpy
import os
import speech_recognition as sr
import scispacy
import spacy
from bisect import bisect_right
import nltk
nlp = spacy.load("en_core_sci_sm") # load it at start time so that speed is maintained

app=Flask(__name__)
api=Api(app)

class q1(Resource):
    def post(self):
        try:
            os.remove("finale.wav")
        except:
            pass
        msg=request.get_json()
        try:
            question_key=msg["question_key"]
            optionstemp=msg["options"]
            options={}
            for i in range(len(optionstemp)):
                options[optionstemp[i].lower()]=optionstemp[i]
            audio=msg["audio"]
        except:
            return Response({},statfindus=400,mimetype="application/json")#the order doesnt match the requirements given to us
        #print("DONE")
        final_file=open("written1.ogg","wb")
        final_file.write(base64.b64decode(audio))#to write base64 to the server
        final_file.close()
        # print("here")
        # os.system("ffmpeg -i written.ogg finale.wav")
        # print("there")
        sound=AudioSegment.from_ogg("written1.ogg")
        sound.export("finale.wav",format="wav")#export it as a WAV file got google
        r=sr.Recognizer()
        spoken=sr.AudioFile('finale.wav')
        with spoken as source:
            audio=r.record(source)
        text=r.recognize_google(audio)
        
        if question_key=="q1":

            #using scispacy's model get all the diseases possible

            text=text.lower()
            doc = nlp(text)
            all_diseases=list(doc.ents)
            for i in range(len(all_diseases)):
                all_diseases[i]=str(all_diseases[i])
            #print(all_diseases)
            ans={"answers":[]}
            if len(all_diseases)==0 or (len(all_diseases)==1 and (all_diseases[0] in {"disease","fit","no disease","sick","not sick"})):
                
                if "none" in options:
                    ans["answers"]=[options["none"]]
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
                else:
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
            if "don't" in text or "do not" in text:
                if "none" in options:
                    ans["answers"]=[options["none"]]
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
                else:
                    return Response(json.dumps(ans),status=200,mimetype="application/json")
            
            j=[i.split() for i in all_diseases]
            #print(j)
            all_diseases=[]
            for i in j:
                all_diseases=all_diseases+i

            print(all_diseases)
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
            text=text.lower()
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

            if "point" in text:
                text=text.split("point")
                text=(text[0].strip()+"."+text[1].strip())
            if "." in text:
                text=text.split(".")
                text=(text[0].strip()+"."+text[1].strip())
            
            s=0
            tokens = nltk.word_tokenize(text)
            tag = nltk.pos_tag(tokens)
            for i in tag:
                if i[1]=="CD":
                    s=float(i[0])
                    break

            if "half" in text:
                s=s+0.5
            
            pos=bisect_right(array,s)
            if pos!=n:
                ans={"answers":[allowed[pos]]}
            else:
                ans={"answers":[allowed[-1]]}
            return Response(json.dumps(ans),status=200,mimetype="application/json")
            
        if question_key=="q3":
            tokens = nltk.word_tokenize(text)
            tag = nltk.pos_tag(tokens)
            allowed={"january":"01","jan":"01","february":"02","feb":"02","march":"03","april":"04",\
                    "may":"05","june":"06","july":"07","august":"08","aug":"08","september":"09","sept":"09",\
                        "oct":"10","october":"10","november":"11","december":"12","dec":"12"}
            date,month,year="0","0","0"
            count=0
            final=[]
            for i in tag:
                if i[1]=="CD":
                    count+=1
                    final.append(i[0])

            if count==3:
                month=final[1]
                if len(final[0])==4 and final[0].isdigit():
                    year=final[0]
                    date=""
                    for i in final[2]:
                        if i.isdigit():
                            date+=i
                        else:
                            break
                else:
                    date=""
                    for i in final[0]:
                        if i.isdigit():
                            date+=i
                        else:
                            break
                    year=final[2]
                    
            else:
                for i in tag:
                    if i[1]=="CD":
                        if i[0].isdigit() and len(i[0])==4:
                            year=i[0]
                        else:
                            s=""
                            index=0
                            while(index<len(i[0]) and i[0][index].isdigit()):
                                s=s+i[0][index]
                                index+=1
                            date=s
                            date="0"*(max(0,2-len(date)))+date
                    elif i[1]=="NNP":
                        month=allowed[i[0].lower()]
                    elif i[1]=="NN" and i[0].lower() in allowed:
                        month=allowed[i[0].lower()]

            ans={"answer":[date+"/"+month+"/"+year]}
            return Response(json.dumps(ans),status=200,mimetype="application/json")
        
        os.system("del finale.wav")

api.add_resource(q1,"/v1/api")

if __name__=="__main__":
    app.run(debug=True)



