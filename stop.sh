if [[ ! -e cp.status ]] ; then
  echo ClimatePrisms is not running?
  exit
fi

source cp.status
if [[ $CP_MONGOD_PID != 0 ]] ; then
  kill $CP_MONGOD_PID
fi

if [[ $CP_SERVER_PID != 0 ]] ; then
  kill $CP_SERVER_PID
fi

rm cp.status

exit 0

