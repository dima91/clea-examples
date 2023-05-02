
#!/bin/bash

cd $(dirname $0)
docker build -t smart-vending-machine-stub -f Dockerfile ../..