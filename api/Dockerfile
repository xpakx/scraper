FROM python:3.8-slim-buster
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY dataset.json .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

