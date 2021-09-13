FROM ubuntu:latest

MAINTAINER Manuel Sarfo

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY .env ./.env
COPY xmltojson.py ./xmltojson.py
COPY s3_functions.py ./s3_functions.py
COPY main.py ./main.py

EXPOSE 80
ENTRYPOINT [ "python3" ]
CMD ["main.py"]