
FROM ubuntu:14.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

EXPOSE	 5000

RUN sudo apt-get -y update

RUN apt-get install dialog -y

RUN sudo apt-get -y install build-essential

ADD app.py /home/app/

ADD /tests /home/tests

ADD testlib.h /home/app/

ADD check.cpp /home/app/

ADD app.json /home/app/

WORKDIR /home/app

CMD ["python3", "./app.py"]






