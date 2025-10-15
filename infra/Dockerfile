FROM python:3.14-rc-bookworm

RUN apt-get update && \
    pip install numpy && \
    pip install pandas && \
    pip install polars && \
    pip install requests && \
    pip install python-dotenv && \
    mkdir /app 

ENTRYPOINT python3 /app/mhanya.py

