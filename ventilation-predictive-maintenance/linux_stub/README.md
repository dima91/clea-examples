
# Ventilation Predicitive Maintenance - stub

This folder contains a simple linux stub for smart ventilation system demo

To build the Docker image, move to root project folder and type:

`bash linux_stub/docker_builder.sh`

This script will create an image called `ventilation-predictive-maintenance`.

---

To run the just created Docker image, create an `env.sh` file containing macros:

```
DEVICE_ID=
DEVICE_SECRET=
API_BASE_URL=
REALM_NAME=
PERSISTENCY_PATH=
INTERFACES_FOLDER=
PYTHONUNBUFFERED=

EVENTS_DELAY_BASE_S=
EVENTS_DELAY_DELTA_S=
EVENTS_DURATION_BASE_S=
EVENTS_DURATION_DELTA_S=

WIFI_SCAN_RESULT_DELAY_UPDATE_s=
CELLULAR_STATUS_DELAY_UPDATE_S=
```

Then launch it with:

`docker run --rm -it --env-file linux_stub/env.sh <image_name>`