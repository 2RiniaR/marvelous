#!/bin/bash

cd `dirname $0`
cd ../app
pipenv run pytest --cov="./src" -v --tb=short -l ./ --cov-report=html
