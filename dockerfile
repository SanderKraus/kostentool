FROM python:3.8-slim-buster
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y git
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD gunicorn --bind 0.0.0.0:80 "app:create_app()"
EXPOSE 80
