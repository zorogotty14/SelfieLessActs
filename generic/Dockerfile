FROM python:alpine3.7
COPY ./app1 /app1
WORKDIR /app1
RUN pip3 install flask flask-cors requests
EXPOSE 80
CMD python3 ./app.py

