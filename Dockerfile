FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_analysis.py .
COPY data ./data

RUN mkdir -p outputs simulated_nosql

CMD ["python", "data_analysis.py"]
