for cid in `docker container ls -q` ; do
  docker stop $cid
  docker rm $cid
done
