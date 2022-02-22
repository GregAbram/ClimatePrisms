#! /bin/bash

bash ./setup-container.sh

mongod --port 1336 --dbpath db >> mongo.out 2>&1  &
sleep 2
python3 server.py 1337 

