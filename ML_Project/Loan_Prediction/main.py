# Import libraries

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib


app = FastAPI()

# Create Fast API app

app = FastAPI(
    title="Loan Approval Prediction API ",
    description="Loan approval prediction using XGBoost",
    version="1.0.0"
)


# Load and save model 

model = joblib.load(
    "loan_xgboost_model_1.pkl"
)


# input data schema

class LoanData(BaseModel):

    Gender: str
    Married: str
    Dependents: int
    Education: str
    Self_Employed: str

    ApplicantIncome: int
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float

    Property_Area: str
    TotalIncome: float


# End home point 

@app.get("/")
def home():

    return {
        "message": "Loan Approval Prediction API is running",
        "model": "XGBoost"
    }


# Prediction end point 

@app.post("/predict")
def predict(data: LoanData):

    try:

        # Convert Pydantic data into dictionary
        input_data = data.model_dump()

        # Convert dictionary into DataFrame
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = model.predict(input_df)[0]

        # Get probabilities
        probabilities = model.predict_proba(input_df)[0]

        # Probability of Approved
        approval_probability = probabilities[1]

        # Convert numeric prediction to readable result
        if prediction == 1:
            result = "Approved"
        else:
            result = "Rejected"

        return {
            "prediction": result,
            "prediction_code": int(prediction),
            "approval_probability": round(
                float(approval_probability),
                4
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )