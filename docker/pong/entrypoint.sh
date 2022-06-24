#!/bin/sh

until ip a show ns3-eth0 > /dev/null 2>&1
do
  echo 'waiting for network connection ...'
  sleep 1
done

exec "$@"
