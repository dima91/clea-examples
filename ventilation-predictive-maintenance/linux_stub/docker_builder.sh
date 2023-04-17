
#!/bin/bash

cd $(dirname $0)
docker build -t ventilation-predictive-maintenance -f Dockerfile ..