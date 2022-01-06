#! /bin/bash

echo "setup-embedded start"

if [[ X$1 == "X" ]] ; then
  echo project required
  exit 1
fi

if [[ $1 = /* ]] ; then
  project=$1
else
  project=`pwd`/$1
fi

if [[ -e db ]] ; then 
  echo "Is ClimatePrisms already set up?   If you need to re-set it, sh cleanup.sh first"
  exit
fi

python3 create_homepage.py $project

mkdir -p db
mongod --dbpath `pwd`/db --port 1336 > mongod.out 2>&1  &
mongo_pid=$!

for i in $project/static/* ; do
  cp -r $i static
done

sleep 3

cd static

for ss in $project/*xlsx ; do
  python3 ../tools/fromExcel $ss
done

python3 ../tools/fillers.py $project

kill $mongo_pid
sleep 3

echo "setup-embedded done"

exit 0
