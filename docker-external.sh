#! /bin/bash

cd ClimatePrisms
bash ./setup.sh ../CPContent

mongod --port 1336 --dbpath db >> mongo.out 2>&1  &
python3 server.py 1337 >> server.out 2>&1  
sleep 100000000
