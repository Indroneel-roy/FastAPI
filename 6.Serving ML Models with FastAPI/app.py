from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
from typing import Literal, Annotated
from fastapi.responses import JSONResponse
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0)]
    height: Annotated[float, Field(..., gt=0)]
    income_lpa: Annotated[float, Field(..., gt=0)]
    smoker: bool
    city: str
    occupation: Literal['retired', 'freelancer', 'student', 'government_job',
                        'business_owner', 'unemployed', 'private_job']

@app.post('/predict')
def predict_premium(data: UserInput):
    # Derived fields
    bmi = data.weight / (data.height ** 2)
    
    if data.smoker and bmi > 30:
        lifestyle_risk = "high"
    elif data.smoker or bmi > 27:
        lifestyle_risk = "medium"
    else:
        lifestyle_risk = "low"
    
    if data.age < 25:
        age_group = "young"
    elif data.age < 45:
        age_group = "adult"
    elif data.age < 60:
        age_group = "middle_aged"
    else:
        age_group = "senior"
    
    city_tier = 1 if data.city in tier_1_cities else 2 if data.city in tier_2_cities else 3

    input_df = pd.DataFrame([{
        "bmi": bmi,
        "age_group": age_group,
        "lifestyle_risk": lifestyle_risk,
        "city_tier": city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"prediction_category": prediction})
