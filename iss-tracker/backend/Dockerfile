FROM python:3.9-slim

ARG OPENSKY_USERNAME
ARG OPENSKY_PASSWORD

ENV OPENSKY_USERNAME=$OPENSKY_USERNAME
ENV OPENSKY_PASSWORD=$OPENSKY_PASSWORD

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]