# Stage 1: install dependencies into a virtual environment
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: final image. copy only the venv, not pip or build tools
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY data_analysis.py .
COPY data ./data
RUN mkdir -p outputs simulated_nosql

CMD ["python", "data_analysis.py"]
