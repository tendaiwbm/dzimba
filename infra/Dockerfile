FROM python:3.14-rc-bookworm

RUN apt-get update && \
    pip install numpy && \
    pip install pandas && \
    pip install requests && \
    pip install python-dotenv && \
    pip install beautifulsoup4 && \  
    mkdir /app 

ENTRYPOINT python3 /app/mhanya.py

