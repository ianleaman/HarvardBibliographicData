'''
Tufts University - Text Mining
Writen By: Ian Leaman

About:
This is a workaround to sql, will process the formated json files without
loading from a db
'''
import json

totalErrs = 0
with open("processedFile.json", "r", encoding="utf-8") as fp:
    x = json.load(fp)
    i = 1
    for doc in x:
        try:
            print(doc)
        except UnicodeEncodeError:
            totalErrs += 1
        i += 1
    print(len(x))

print(totalErrs)
