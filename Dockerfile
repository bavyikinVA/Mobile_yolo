FROM python:3.12

RUN mkdir client
RUN mkdir client/Images_screen
ADD main.py client/main.py
ADD Images_screen client/Images_screen

RUN apt update
RUN apt install sudo
RUN usermod -aG sudo root

RUN pip install --user --upgrade buildozer
RUN sudo apt update
RUN sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
RUN pip install --user --upgrade Cython==0.29.33 virtualenv
RUN sudo apt install -y vim

RUN export PATH=$PATH:~/.local/bin/
