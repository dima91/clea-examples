
#!/bin/bash

cd $(dirname $0)
source venv/bin/activate
python3 src/main.py -i DQPcm2mQSGaGSjpkoYob7A -s jAhuEsRojW3LUppdB4YEnDOTu6dlLLw6Vrh3uHqF9Oc= \
                -u https://api.demo.clea.cloud -n showcase -p persistency.d -f ../astarte-interfaces