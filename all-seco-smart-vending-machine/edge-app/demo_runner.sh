
#!/bin/bash

CONFIG_FILE=$(realpath $1)

cd $(dirname $0)

source venv/bin/activate
python3 main.py -c $CONFIG_FILE