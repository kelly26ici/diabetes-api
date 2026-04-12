from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

class ModelInput(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int    
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

model = pickle.load(open('diabetes_model.pkl', 'rb'))

@app.post("/diabetes_prediction")
def diabetes_pred(input_parameters: ModelInput):

    input_list = [
        input_parameters.Pregnancies,
        input_parameters.Glucose,
        input_parameters.BloodPressure,
        input_parameters.SkinThickness,
        input_parameters.Insulin,
        input_parameters.BMI,
        input_parameters.DiabetesPedigreeFunction,
        input_parameters.Age
    ]

    prediction = model.predict([input_list])

    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Not Diabetic"

    return {
        "prediction": int(prediction[0]),
        "result": result
    }
    