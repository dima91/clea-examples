
#!/bin/bash

cd $(dirname $0)
docker build -t offgrid-solar-system-stub -f Dockerfile ../..