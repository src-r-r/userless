#!/bin/bash

# commands
DOCKER=$(which docker)

# Defaults
NAME=userless
HOST_PORT=5000
DOCKER_PORT=5000

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd ${DIR}/..

${DOCKER} build .
# ${DOCKER} run -d --name=userless
${DOCKER} run --name=${NAME} \
  -v $(pwd)/${NAME}:/${NAME} \
  -p ${DOCKER_PORT}:${HOST_PORT} \
  ${NAME}:0.1
