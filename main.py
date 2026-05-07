from fastapi import FastAPI
import json
from pydantic import BaseModel
import random

app = FastAPI()

def url_generator():
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTTUVWXYZabcdefghijklmnopqrstuvwxyz"
    url=""
    for i in range(6):
        url+=alphabet[random.randint(0,len(alphabet))]
    return url
print(url_generator())