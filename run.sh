#!/usr/bin/env bash
IMG_NAME=$(grep -oP "IMG_NAME = \K\w+" Makefile)
CONTAINER_NAME=${IMG_NAME}-cntr
USER=$(whoami)
DOCKER_FLAGS=""
ARGS=""

error() {
    echo "u do sumting wong"
}

while getopts "du" option; do
    case $option in
        d) DOCKER_FLAGS+="-d ";;
        u) USER=${OPTARG};;
        *) error; exit;;
    esac
done

# $@ is an array or something, start at $OPTIND and rest
ARGS+=${@:$OPTIND}

docker run ${DOCKER_FLAGS} -it --hostname ${CONTAINER_NAME} \
    --user ${USER} \
    -v "$(pwd)/volume":/project \
    --rm --name ${CONTAINER_NAME} ${IMG_NAME} ${ARGS}