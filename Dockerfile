FROM openjdk:8-jdk-alpine

RUN apk update && apk upgrade 

# install python

RUN apk add python && apk add python3

# install gcc and g++

RUN apk add gcc && apk add g++

# Add script check

ADD checker.py /home/check/

# Add library for checker.cpp

ADD testlib.h /home/check/

WORKDIR /home/check

CMD ["python3", "./checker.py"]
