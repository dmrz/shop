#!/bin/bash
CMD=${1:-"runserver"}

if [ $CMD = "test" ]
then
  pytest shop
else
  python shop/manage.py runserver 0.0.0.0:9000
fi
