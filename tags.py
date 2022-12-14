import json
import requests as req
import lxml.html
import hashlib
import re


def bian(te,rep):
    while te[0] in rep:
        te=te[1:]
    while te[len(te)-1] in rep:
        te=te[:-1]
    return te

with open ("tags.json") as tags:
    tags=json.load(tags)
with open ("index.json") as indexx:
    indexx=json.load(indexx)

[tags[it].update({"tags":bian(tags[it].get("tags"),"\n \r")}) for it in range(len(tags))]

def transalte(tag):
    print(tag)
    return ""

[tags[it].update({"chin":transalte(tags[it].get("tags"))}) for it in range(len(tags)) if tags[it].get("chin")==""]

with open ("tags.json","w",encoding="utf-8") as file:
    file.write(json.dumps(tags))

index={}
[index.update({it.get("tags"):it.get("index")}) for it in tags]
with open("index.json","w",encoding="utf-8") as file:
    file.write(json.dumps(index))

index=[{"index":it.get("index"),"sui":list(it.get("tags"))+list(it.get("chin"))+list(it.get("type") or "")+list(it.get("one") or "")+list(it.get("two") or "")+list(" " if it.get("one") else "")} for it in tags]
tags={}
for it in index:
    for sui in list(set(it.get("sui"))):
        item=tags.get(sui) or []
        item.append(it.get("index"))
        tags.update({sui:item})
with open ("search.json","w",encoding="utf-8") as file:
    file.write(json.dumps(tags))