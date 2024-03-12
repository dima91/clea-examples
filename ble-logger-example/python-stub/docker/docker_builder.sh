
#!/bin/bash

cd $(dirname $0)
docker build -t ble-logger-stub -f Dockerfile ../..