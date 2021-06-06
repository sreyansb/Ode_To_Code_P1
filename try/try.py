"""
import base64
#from pydub import AudioSegment
import os
import speech_recognition as sr


#music_file=open("example.ogg","rb")
#encoded_string=base64.b64encode(music_file.read())
#music_file.close()
#print(encoded_string)

encoded_string="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"

final_file=open("written2.ogg","wb")
final_file.write(base64.b64decode(encoded_string))
final_file.close()

os.system("ffmpeg -i written2.ogg finale.wav")
r=sr.Recognizer()
spoken=sr.AudioFile('finale.wav')
with spoken as source:
    audio=r.record(source)
text=r.recognize_google(audio)
print(text)

'''
AudioSegment.converter = "C:/Users/sreya/FFmpeg"
ogg_version = AudioSegment.from_ogg("C:/Users/sreya/Desktop/PYTHONandCfiles/ode_to_code/try/written.ogg")
ogg_version.export("wavfile.wav",format="wav")
'''
'''
import soundfile as sf
data, samplerate = sf.read('written2.ogg')
sf.write('new_file.wav', data, samplerate)

'''
"""
'''

from nltk import pos_tag
from nltk import RegexpParser
text ="I have cancer and high blood pressure".split()
print("After Split:",text)
tokens_tag = pos_tag(text)
print("After Token:",tokens_tag)
patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
chunker = RegexpParser(patterns)
print("After Regex:",chunker)
output = chunker.parse(tokens_tag)
print("After Chunking",output)
'''

import nltk
text = "I was born is 4th December 1995"
tokens = nltk.word_tokenize(text)
print(type(tokens),type(tokens[0]))
tag = nltk.pos_tag(tokens)
print(type(tag),type(tag[0][0]),tag[0][1]=="CD")
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp  =nltk.RegexpParser(grammar)
result = cp.parse(tag)
print(result)
#result.draw()


'''
import scispacy
import spacy
nlp = spacy.load("en_core_sci_sm")
#text = """I have no disease""" - > no disease
#text="I am well"->()
text="I am sick"
doc = nlp(text)
print((doc.ents))
'''

'''
import nltk
nltk.download('punkt')
'''
'''
import scispacy
import spacy
import json
nlp = spacy.load("en_core_sci_sm")
#text = """I have no disease""" - > no disease
#text="I am well"->()

optionstemp=["Diabetes","Thyroid","Cancer","None"]
options={}
for i in range(len(optionstemp)):
    options[optionstemp[i].lower()]=optionstemp[i]
def finder(text):
    doc = nlp(text)
    all_diseases=list(doc.ents)
    for i in range(len(all_diseases)):
        all_diseases[i]=str(all_diseases[i])
    #print(all_diseases)
    ans={"answers":[]}
    if len(all_diseases)==0 or (len(all_diseases)==1 and (all_diseases[0] in {"disease","fit","no disease","sick","not sick"})):
        
        if "none" in options:
            ans["answers"]=[options["none"]]
            print(json.dumps(ans))
            return 1
        else:
            print(json.dumps(ans))
            return 2
    ansk=set()
    for i in all_diseases:
        k=i
        if "disease" in k and k!="disease":
            k=k.split("disease")[0]
        if k in options:
            ansk.add(options[k])
        elif k!="disease":
            ansk.add("others")
    if "others" not in options:
        ansk=ansk-{"others"}
    elif "others" in ansk :
        ansk=ansk-{"others"}
        ansk.add(options["others"])
    ans={"answers":list(ansk)}
    print(json.dumps(ans))
    return 3
    #return Response(json.dumps(ans),status=200,mimetype="application/json")

#print(finder("I have cancer and thyroid".lower()))
#print(finder("I have no disease".lower()))
print(finder("I have High Blood pressure".lower()))
'''
'''
from bisect import bisect_right
import json
import nltk

optionstemp=["<5lakh","5lakh-15lakh","15lakh-20lakh","20lakh>"]
options={}
for i in range(len(optionstemp)):
    options[optionstemp[i].lower()]=optionstemp[i]
#text="My income is 3 lack"
text="I earn 15 lakh per annum"
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
print(text,array,s,json.dumps(ans))
'''
'''
import json
#text="23rd december 1998".lower()
#text="22 10 1998".lower()
text="1998 10 22".lower()

text=text.split()
s=""
index=0

while(index<len(text[0]) and text[0][index].isdigit()):
    s=s+text[0][index]
    index+=1

date,year,month=0,0,0
if len(s)<4:
    date=s
    if len(date)<2:
        date="0"+date

    allowed={"january":"01","jan":"01","february":"02","feb":"02","march":"03","april":"04",\
        "may":"05","june":"06","july":"07","august":"08","aug":"08","september":"09","sept":"09",\
            "oct":"10","october":"10","november":"11","december":"12","dec":"12"}
    
    if text[1] in allowed:
        month=allowed[text[1]]
    else:
        month=text[1]
    year=text[2]
else:
    year=text[0]
    month=text[1]
    date=text[2]
ans={"answer":[date+"/"+month+"/"+year]}
print(json.dumps(ans))
'''
'''
import ffmpeg
stream=ffmpeg.input("no_health.ogg")
ffmpeg.output(stream,"abc.wav")
'''
'''
from pydub import AudioSegment
sound = AudioSegment.from_ogg("no_health.ogg")
sound.export("ainvayi.wav", format="wav")
'''