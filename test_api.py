import requests

url = "http://127.0.0.1:8000/predict"
student_data = {
    "study_hours": 5,
    "attendance": 90,
    "previous_marks": 75,
}

response = requests.post(url, json=student_data, timeout=10)
response.raise_for_status()
print("status code", response.status_code)
print("prediction", response.json())