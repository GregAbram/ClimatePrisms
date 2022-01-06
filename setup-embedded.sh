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

for i in $project/static/* ; do
  cp -r $i static
done

mkdir xlsx
for i in $project/*xlsx ; do
  cp $i xlsx
done

exit 0
