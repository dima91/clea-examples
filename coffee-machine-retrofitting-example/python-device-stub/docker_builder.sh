
#|/bin/bash

cd $(dirname $0)
docker build -t coffee-machine-retrofitting-stub -f Dockerfile ..
