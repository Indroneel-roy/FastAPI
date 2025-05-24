
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name : Annotated[str, Field(..., description="Name of the patient")]
    city : Annotated[str, Field(..., description="City of the patient")]
    age : Annotated[int, Field(..., gt=0, lt=100, description="Age of the pathient")]
    gender : Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
    

#load json file
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

#Same data in json file
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)    
        

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

#post data into server
@app.post("/create")
def create_patient(patient : Patient):
    #load the data
    data = load_data()
    
    #check data if exist in server
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")
    
    #if not take this 
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    #save into the json
    save_data(data)
    return JSONResponse(status_code=200, content={'message' : 'patient created successfully'})
    
