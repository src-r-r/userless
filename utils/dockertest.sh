#!/bin/bash

# commands
DOCKER=$(which docker)

# Defaults
NAME=userless
VERION=0.1
HOST_PORT=5000
DOCKER_PORT=5000
NETWORK=${NAME}-net

# Last I checked humans memorize things by names and not by hash strings.
# Convert the docker container name (if it's running) to the container ID.
docker-id() {
    docker ps -f name=$1 -q
}

# Get the IP address of either the running image name or its ID. The function
# will determine which one to use.
docker-ip() {
    # First filter by ID
    ID=`docker-id "$1"`
    if [ ! -n "$ID" ]; then
        ID="$1"
    fi;
    docker inspect -f \
        '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$ID"
}

# Get the directory of this script.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# Go to the root of this directory.
cd ${DIR}/..

# Build the docker container as 'userless'
${DOCKER} build -t ${NAME} .

${DOCKER} network create --driver bridge ${NETOWRK}

# Run the docker container,
# 1 - mount ./src to /userless
# 2 - Forward port 5000 to 5000 on host
${DOCKER} run -d \
  -n ${NAME} \
  --hostname ${NAME} \
  -it ${NAME}:${VERSION}
  --network ${NETWORK} \
  -v ${DIR}/../src:/${NAME} \
  -p ${DOCKER_PORT}:${HOST_PORT} \
  ${NAME}
