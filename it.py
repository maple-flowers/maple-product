import json

with open ("tags.json","r",encoding="utf-8") as tags:
    tags=[it.get("tags") for it in json.load(tags) if it.get("chin")==""]
print(len(tags))
with open ("tags.txt","w",encoding="utf-8") as file:
    file.write(json.dumps(tags))