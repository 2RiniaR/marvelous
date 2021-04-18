#!/bin/bash

cd `dirname $0`
cd ..

docker-compose -f ./docker-compose.dev.yml down
#sudo rm -r ./db/data
