#! /bin/bash

cd /ClimatePrisms

mkdir db
mongod --port 1336 --dbpath db >> mongo.out 2>&1  &

sleep 2

for xlsx in xlsx/* ; do
  python3 tools/fromExcel $xlsx
done

python3 tools/fillers.py static/content/fillers

python3 server.py 1337 >> server.out 2>&1  
sleep 100000000
