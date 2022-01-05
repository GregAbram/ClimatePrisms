FROM ubuntu

EXPOSE 1337

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y vim
RUN python3 -m pip install pymongo openpyxl web.py
RUN apt-get install -y mongodb
RUN mkdir ClimatePrisms
COPY ClimatePrisms ClimatePrisms/static
COPY content ClimatePrisms/static/content
COPY server.py ClimatePrisms/server.py
COPY api.py ClimatePrisms/api.py
COPY services.sh ClimatePrisms/services.sh
WORKDIR "/ClimatePrisms"
CMD ["sh", "services.sh"]
