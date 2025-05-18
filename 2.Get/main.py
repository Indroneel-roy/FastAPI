from fastapi import FastAPI, Path
from fastapi.responses import Response
import json

app = FastAPI()

#load json file
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data
        

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

#view endpoint
@app.get("/view")
def view():
    data = load_data()
    pretty = json.dumps(data, indent=2)
    return Response(content=pretty, media_type="application/json")