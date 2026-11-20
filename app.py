from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Models" / "student_model.pkl"

app = FastAPI(title="Student Performance Prediction API")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError as exc:
    raise RuntimeError(f"Model not found at {MODEL_PATH}") from exc


class StudentData(BaseModel):
    study_hours: float
    attendance: float
    previous_marks: float


@app.post("/predict")
def predict(student: StudentData):
    input_data = pd.DataFrame([{
        "study_hours": student.study_hours,
        "attendance": student.attendance,
        "previous_marks": student.previous_marks,
    }])

    try:
        raw_prediction = model.predict(input_data)[0]
        if isinstance(raw_prediction, str):
            prediction_result = raw_prediction
            prediction = 1 if prediction_result.lower() == "pass" else 0
        else:
            prediction = int(raw_prediction)
            prediction_result = "Pass" if prediction == 1 else "Fail"
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    return {
        "prediction": prediction,
        "result": prediction_result,
    }
