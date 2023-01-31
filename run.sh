#!/usr/bin/env bash
IMG_NAME=$(awk '/IMG_NAME = [A-Za-z0-9]+/ {print $3}' ./Makefile)
CONTAINER_NAME=${IMG_NAME}-cntr
USER=$(whoami)
DOCKER_FLAGS=""
ARGS=""

error() {
    echo "u do sumting wong"
}

while getopts "dpu" option; do
    case $option in
        d) DOCKER_FLAGS+="-d ";;
        p) DOCKER_FLAGS+="--publish 8080:8080 ";;
        u) USER=${OPTARG};;
        *) error; exit;;
    esac
done

# $@ is an array or something, start at $OPTIND and rest
ARGS+=${@:$OPTIND}

docker run ${DOCKER_FLAGS} \
    -it \
    --rm \
    --hostname ${CONTAINER_NAME} \
    --user ${USER} \
    -v "$(pwd)/volume":/project \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -u `id -u`:`id -g` \
    --name ${CONTAINER_NAME} ${IMG_NAME} ${ARGS}
