from fastapi import FastAPI
import json
from pydantic import BaseModel
import random
from fastapi.responses import RedirectResponse

app = FastAPI()

FILE_NAME = "links.json"

class Link(BaseModel):
    url: str

def url_generator():
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    code=""
    for i in range(6):
        code+=alphabet[random.randint(0,len(alphabet)-1)]
    return code

@app.post("/shorten")
def url_shortener(link: Link):
    try:
        with open(FILE_NAME,"r") as file:
            codes=json.load(file)
    except FileNotFoundError:
        codes=[]
    code_exists = True
    while code_exists:
        code_exists = False
        code = url_generator()
        for i in codes:
            if i["code"]==code:
                code_exists = True
    new_data={
        "code": code,
        "url": link.url,
        "clicks": 0
    }
    codes.append(new_data)
    with open(FILE_NAME,"w") as file:
        json.dump(codes,file)
    return {
        "code": code,
        "original_url": link.url,
        "short_url": f"http://localhost:8000/{code}"
    }

@app.get("/{code}")
def get_code(code: str):
    try:
        with open(FILE_NAME,"r") as file:
            codes=json.load(file)
    except FileNotFoundError:
        return{
            "error": "no url file"
        }
    for i in codes:
        if i["code"]==code:
            i["clicks"]+=1
            with open(FILE_NAME,"w") as file:
                json.dump(codes,file)
            return RedirectResponse(url=i["url"])
    return{
        "error": "wrong url"
    }