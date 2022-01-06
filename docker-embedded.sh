#! /bin/bash

echo AAAAAAAAAA `pwd`
cd /ClimatePrisms
echo BBBBBBBBBB `pwd`

echo Starting mongod...
mongod --port 1336 --dbpath db >> mongo.out 2>&1  &
sleep 5
ps aux | grep mongod
echo Should see mongod... starting Server

python3 server.py 1337 >> server.out 2>&1  
echo Server ended
