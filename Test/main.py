from fastapi import FastAPI

app = FastAPI()
@app.get("/")

def hello():
    return {"Message" : "hello world"}

@app.get("/about")
def about():
    return {"message" : "Indroneel is going will get job at google as ML Engineer"}

