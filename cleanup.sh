#! /bin/bash

bash stop.sh

sleep 2

for i in static/* ; do 
  if [[ -L $i ]] ; then 
    rm $i
  fi 
done

rm -f static/project.css
rm -rf static/content
rm -f static/index.html
rm -rf xlsx

if [[ -e db ]] ; then
  rm -rf db
fi

echo "cleanup done"
exit 0


