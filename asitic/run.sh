#!/bin/bash

xhost +
docker run --rm -ti --net=host -v $PWD:/tech -e DISPLAY=:0 asitic /bin/bash -c "/asitic_linux -t /tech/sky130.tek"
