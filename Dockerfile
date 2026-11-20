FROM python:3.12-slim
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY app.py .
COPY Models/ ./Models/
EXPOSE 10000
CMD ["uvicorn","app:app", "--host", "0.0.0.0", "--port", "10000"]