FROM python:3.9-slim
WORKDIR /app
COPY . /app
#RUN apt-get update && \
    #apt-get install -y \
    #build-essential \
    #unixodbc-dev \
    #&& rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "clean_data_noSQL.py"]
