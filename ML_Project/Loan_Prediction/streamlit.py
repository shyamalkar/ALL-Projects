# Import libraries 

import streamlit as st
import requests


# page configration 

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="",
    layout="centered"
)


# Title 

st.title("Loan Approval Prediction")

st.write(
    "Enter the applicant information below "
    "to predict whether the loan will be approved."
)


# Fast API url 

API_URL = "http://127.0.0.1:8000/predict"


# Input section 

st.subheader("Applicant Information")


# gender

Gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)



# Married

Married = st.selectbox(
    "Married",
    ["Yes", "No"]
)



# Dependents

Dependents = st.selectbox(
    "Dependents",
    [0, 1, 2, 3]
)



# Education

Education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)



# Self Employed

Self_Employed = st.selectbox(
    "Self Employed",
    ["No", "Yes"]
)



# Applicant Income

ApplicantIncome = st.number_input(
    "Applicant Income",
    min_value=0,
    value=5000,
    step=100
)



# Coapplicant Income

CoapplicantIncome = st.number_input(
    "Coapplicant Income",
    min_value=0.0,
    value=0.0,
    step=100.0
)



# Loan Amount

LoanAmount = st.number_input(
    "Loan Amount",
    min_value=0.0,
    value=150.0,
    step=10.0
)



# Loan Amount Term

Loan_Amount_Term = st.selectbox(
    "Loan Amount Term",
    [36, 60, 84, 120, 180, 240, 300, 360, 480]
)



# Credit History

Credit_History = st.selectbox(
    "Credit History",
    [1.0, 0.0],
    format_func=lambda x: (
        "Good Credit History (1)"
        if x == 1.0
        else "No Credit History (0)"
    )
)



# Property Area

Property_Area = st.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)



# Total Income

TotalIncome = st.number_input(
    "Total Income",
    min_value=0.0,
    value=5000.0,
    step=100.0
)



# PREDICTION BUTTON

if st.button(
    "Predict Loan Approval",
    use_container_width=True
):

# Create input data 

    input_data = {

        "Gender": Gender,

        "Married": Married,

        "Dependents": Dependents,

        "Education": Education,

        "Self_Employed": Self_Employed,

        "ApplicantIncome": ApplicantIncome,

        "CoapplicantIncome": CoapplicantIncome,

        "LoanAmount": LoanAmount,

        "Loan_Amount_Term": float(Loan_Amount_Term),

        "Credit_History": Credit_History,

        "Property_Area": Property_Area,

        "TotalIncome": TotalIncome
    }


# send data to Fast API 

    try:

        response = requests.post(
            API_URL,
            json=input_data,
            timeout=10
        )

# Check API response 

        if response.status_code == 200:

            result = response.json()


# get prediction 

            prediction = result["prediction"]

            probability = result["approval_probability"]


# Display result 

            st.subheader("Prediction Result")


            if prediction == "Approved":

                st.success(
                    f"Loan Approved"
                )

            else:

                st.error(
                    f"Loan Rejected"
                )


# Display the probability 

            st.metric(
                "Approval Probability",
                f"{probability * 100:.2f}%"
            )


# progress bar 

            st.progress(probability)


# Show submit data 

            with st.expander("View Submitted Information"):

                st.json(input_data)


        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(
                response.text
            )


# Connection error 

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to FastAPI. "
            "Make sure FastAPI is running on "
            "http://127.0.0.1:8000"
        )


# Others errors . 

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )


# Footer 

st.divider()

st.caption(
    "Machine Learning Model: XGBoost | "
    "Backend: FastAPI | Frontend: Streamlit"
)