#!/bin/bash

cd `dirname $0`
cd ..

docker-compose down
sudo rm -r ./db/data
