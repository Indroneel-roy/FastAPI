from fastapi import FastAPI, Path, HTTPException, Query
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
#view a particular patient
@app.get("/patient/{patient_id}")
def view_patient(patient_id : str = Path(..., description="ID of the patient", example= "P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found") #HTTPException used to return custom HTTP error respons like 404 not found

#sort by value
@app.get("/sort")
def sort_patient(sort_by : str = Query(..., description="Sorted by height, weight or bmi"), order : str = Query("acs", description="sorted in acs or desc order")):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ["acs", "desc"]:
        raise HTTPException(status_code=400, detail=f'Invalid order select between acs and desc')
    sort_order = True if order=='desc' else False
    data = load_data()
    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by, 0), reverse = sort_order)
    return sorted_data

