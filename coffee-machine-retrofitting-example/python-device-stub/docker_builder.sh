
#|/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters: missing image name"
    exit
fi

DOCKER_IMAGE_NAME=$1
docker build -t $DOCKER_IMAGE_NAME -f Dockerfile ..
