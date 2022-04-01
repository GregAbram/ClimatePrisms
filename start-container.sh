#! /bin/bash

if test -e /db ; then
  rm -rf /db
fi

mkdir -p /db
mongod --port 1336 --dbpath /db >> mongo.out 2>&1  &
sleep 2

echo "setup start"

project=/ClimatePrisms.Content

for i in $project/static/* ; do
  lcl=`echo $i | sed "s?\$project/??"`
  if [[ -e $lcl ]] ; then
    echo removing $lcl
    rm $lcl
  fi
  ln -s $i static
done

python3 create_homepage.py $project > /tmp/sc.log 2>&1

cd static

for ss in $project/*xlsx ; do
  python3 ../tools/fromExcel $ss 
done

cd ..

python3 ./tools/fillers.py $project

echo "setup done"

python3 server.py 1337 > /var/log/cp.log 2>&1 &
sleep 999999999
