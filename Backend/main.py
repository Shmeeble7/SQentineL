from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Analyzer.engine import analyze

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class CodeInput(BaseModel):
    def __init__(code:str):
        self.code = code

@app.get("/")
async def root():
    message = "SQentineL rocks!!!"
    return {"message": message}

@app.post("/query")
async def read_query():
    #here we see if the query is good or bad
    message = "Hopefully you know good development practices because we can't check your queries yet!"
    return {"message": message}

@app.post("/analyze/{code}")
def scan(code):
    codeInput = CodeInput(code)
    return {"issues": analyze(codeInput)}