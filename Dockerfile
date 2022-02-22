FROM ubuntu

EXPOSE 1337

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y vim
RUN python3 -m pip install pymongo openpyxl web.py bs4
RUN apt-get install -y mongodb
RUN mkdir /ClimatePrisms

# To create a Docker image with embedded content, use the following:
# COPY {path to project directory} /ClimatePrisms.Content

COPY . /ClimatePrisms/
WORKDIR /ClimatePrisms

CMD /bin/bash ./start-container.sh
