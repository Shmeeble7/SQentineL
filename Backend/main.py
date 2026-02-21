from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    message = "SQentineL rocks!!!"
    return {"message": message}

@app.get("/query/{query_str}")
async def read_query(query_str):
    #here we see if the query is good or bad
    message = "Hopefully you know good development practices because we can't check your queries yet!"
    return {"message": message}