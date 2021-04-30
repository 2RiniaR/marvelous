#!/bin/bash

cd `dirname $0`
cd ..

docker-compose logs -tf
