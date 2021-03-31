#!/bin/bash

cd `dirname $0`
cd ..

docker-compose -f ./docker-compose.dev.yml up -d --build
