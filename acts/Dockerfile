FROM python:alpine3.7
COPY . /acts
WORKDIR /acts
RUN pip3 install -r requirements.txt
EXPOSE 80
ENV TEAM_ID CC_080_103_106_114
CMD python3 ./app.py

