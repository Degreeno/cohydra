#!/bin/bash -e

docker build -t osmhpi/cohydra .

cd examples

docker-compose build
docker-compose up -d

docker run --rm \
    --net host --pid host --userns host --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v $PWD:/examples -w /examples \
    osmhpi/cohydra ./basic_example.py

docker-compose down
