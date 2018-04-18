FROM praekeltfoundation/python-base:3.6

RUN apt-get update && apt-get install -y netcat git

WORKDIR /app/

COPY ./requirements /app/requirements

RUN pip install -r requirements/requirements.txt --src /usr/local/src

COPY . /app/

EXPOSE 8000
