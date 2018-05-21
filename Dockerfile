FROM ubuntu:14.04

RUN echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections

RUN sudo apt-get update -y

RUN sudo apt-get install dialog -y

RUN sudo apt-get install software-properties-common -y

RUN sudo apt-get install build-essential -y

# install gcc v.7
RUN sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
RUN sudo apt-get update
RUN sudo apt-get install gcc-7 g++-7 -y
RUN sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7

RUN sudo apt-get install default-jre -y
RUN sudo apt-get install default-jdk -y

RUN sudo apt-get install python -y

RUN sudo apt-get install wget -y

ADD checker.py /home/check/

RUN wget https://raw.githubusercontent.com/MikeMirzayanov/testlib/master/testlib.h
RUN mv testlib.h /home/check/

WORKDIR /home/check

CMD ["python3", "./checker.py"]
