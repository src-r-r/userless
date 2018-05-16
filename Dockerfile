FROM alpine:3.5
EXPOSE 5000
RUN apk add --no-cache python3 curl sqlite
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev python3-dev && \
    apk add postgresql-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python3 get-pip.py
RUN mkdir /userless
COPY ./src /userless
WORKDIR /userless
RUN pip install -r requirements.txt
ENV FLASK_APP=userless.main:app
RUN /usr/bin/python3 -m flask run
