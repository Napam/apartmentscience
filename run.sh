#!/usr/bin/env bash
IMG_NAME=$(grep -oP "IMG_NAME = \K\w+" Makefile)
CONTAINER_NAME=${IMG_NAME}-cntr

docker run -it --hostname ${CONTAINER_NAME} \
    --user $(whoami) \
    -v "$(pwd)/volume":/project \
    --rm --name ${CONTAINER_NAME} ${IMG_NAME} bash