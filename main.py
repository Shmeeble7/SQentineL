from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Analyzer.engine import analyze
from pydantic import BaseModel

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
    text: str



@app.post("/analyze")
def scan(request: CodeInput):
    results = analyze_to_json(request.text)
    return {"results": results}


def analyze_to_json(code: str):
    issues = analyze(code)
    return [issue.to_dict() for issue in issues]