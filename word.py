import json
import re
import os
import ast

jia="images/magic2@0@3/"
txt="magic2@0@3.txt"
jso="magic2@0@3.json"
zhui="magic2@"
nunu=2

with open ("index.json") as indexx:
    indexx=json.load(indexx)
with open ("tags.json") as tagss:
    tagss=json.load(tagss)

def qu(te,rep1,rep2):
    while rep1 in te:
        te=te.replace(rep1,rep2)
    return te

def bian(te,rep):
    if len(te)==0:
        return te
    while te[0] in rep:
        te=te[1:]
        if len(te)==0:
            break
    if len(te)==0:
        return te
    while te[len(te)-1] in rep:
        te=te[:-1]
        if len(te)==0:
            break
    return te

def zhuan(txt):
    li1=["(","[","{","}","]",")"]
    for it in range(6):
        if li1[it]==txt:
            return li1[5-it]

def kuo(tex,rep):
    ind=rep
    typ=tex[0]
    typ=typ if typ in "([{" else ""
    ee="咒语"
    inde=0
    te=tex[rep:len(tex)-rep]
    cop=bian(te," ,")
    te=bian(te," ,")
    try:
        if ind==1 and (":" in te):
            te=te.split(":")
            if "," not in te[1]:
                ind=float(bian(te[1]," "))
                te=bian(te[0]," ")
            else:
                inde=te[1].split(",")
                ind=float(bian(inde[0]," "))
                inde=float(bian(inde[1]," "))
                te=bian(te[0]," ")
    except:
        te=cop
        ind=rep
        inde=0
    if typ=="[":
        ind=-ind
    if ind%1==0 and ind>=0:
        ind=ind+1
    if ifin(te,"([{}]),"):
        print(tex,rep)
        print("复杂类型的tag",te,ind)
    return [chuli(te),ind,typ,ee,inde]

def ifin(text,init):
    for it in list(init):
        if it in text:
            return True
    return False

def chuli(tx):
    if indexx.get(tx):
        return indexx.get(tx)
    elif tx=="1girl":
        return 0
    else:
        num="-1" if ifin(tx,"([{}]),") else "10000"
        tagss.append({"index":len(tagss),"tags":tx,"chin":"","num":num})
        indexx.update({tx:len(tagss)-1})
        return len(tagss)-1

def yanzhang(zhang):
    a=zhang[0]
    for it in zhang:
        if a!=it:
            return False
        a+=1
    return True

def prompt(text):
    text=text.replace("\xa0"," ")
    text=text.replace(";",",")
    text=text.replace("（","(").replace("）",")").replace("【","[").replace("】","]")
    text=qu(text,", ",",")
    text=qu(text," ,",",")
    text=text+","
    zhang=[]
    resul=[]
    its=-1
    ind=0
    for it in range(len(text)):
        if it==len(text) and len(zhang)!=0:
            raise
        if text[it]=="." and (text[it-1] not in "0123456789"):
            text=text[:it]+","+text[it+1:]
        if (text[it] in "([{,") and len(zhang)==0:
            item=text[its:it]
            if bian(item," ,")!="":
                resul.append(kuo(bian(item," ,"),ind))
                ind=0
            its=it
        if text[it] in "([{":
            zhang.append(it)
            ind=0
        elif text[it] in ")]}":
            if yanzhang(zhang):
                ind+=1
            zhang=zhang[:-1]
        else:
            ind=0
    return resul

def promptplus(text):
    if text[0:2]=="##":
        text=text[2:].split("\n##")
        li=[]
        for it in text:
            it=it.split("%%")
            typ=it[0]
            tex=prompt(it[1])
            for i in range(len(tex)):
                tex[i][3]=typ
            li=li+tex
        return li
    else:
        return prompt(text)

with open (txt,encoding="utf-8") as file:
    txt=file.read().split("\n"*nunu)
txt=[it.split("\n@@") for it in txt]
txt=[{"name":it[0],"detail":it[1],"progress":it[2],"add":promptplus(it[3]),"reduce":promptplus(it[4]),"settings":it[5],"pic_num":int(it[6])} for it in txt]
magic={}
[magic.update({it.get("name"):it}) for it in txt]

with open (jso,"w",encoding="utf-8") as file:
    file.write(json.dumps(magic))
'''name=[it.get("name") for it in txt]
pic=[it.get("pic_num") for it in txt]
li=sorted(os.listdir(jia),key=lambda it:int(it.replace(zhui,"").replace(".png","")))
index=0
for it in range(len(name)):
    for ind in range(pic[it]):
        print(name[it])
        os.rename(jia+li[index],jia+name[it]+"@"+str(ind)+".png")
        index+=1'''
with open ("index.json","w",encoding="utf-8") as file:
    file.write(json.dumps(indexx))
with open ("tags.json","w",encoding="utf-8") as file:
    file.write(json.dumps(tagss))