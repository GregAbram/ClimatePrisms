#! /bin/bash

if [[ -e cp.status ]] ; then
  echo "is ClimatePrisms already running?"
  exit
fi

mongod --port 1336 --dbpath db >> mongo.out 2>&1  &
mongod_pid=$!

if [[ X$1 == 'X-p' ]] ; then

server_pid=0

cat > cp.status << EOF
CP_MONGOD_PID=$mongod_pid
CP_SERVER_PID=$server_pid
EOF

python3 server.py 1337 
 
else

sleep 2
python3 server.py 1337 >> server.out 2>&1  &
server_pid=$!

cat > cp.status << EOF
CP_MONGOD_PID=$mongod_pid
CP_SERVER_PID=$server_pid
EOF

fi
