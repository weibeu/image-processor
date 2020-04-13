FROM python:3.8.2-slim

WORKDIR /image-processor

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD python3 run.py
