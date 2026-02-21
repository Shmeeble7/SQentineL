from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:64101",
    "http://localhost:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    message = "SQentineL rocks!!!"
    return {"message": message}

@app.post("/query")
async def read_query():
    #here we see if the query is good or bad
    message = "Hopefully you know good development practices because we can't check your queries yet!"
    return {"message": message}