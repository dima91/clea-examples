
#!/bin/bash

cd $(dirname $0)
docker build -t people-counter-stub -f Dockerfile ..