
# People Counter demo stub

This folder contains a simple linux stub for people counter demo

To build the Docker image, move to root project folder and type:

`bash linux_stub/docker_builder.sh`

This script will create an image called `people-counter-stub`.

---

To run the just created Docker image, create an `env.sh` file containing macros:

```

PYTHONUNBUFFERED=1

# Astarte details
DEVICE_ID=
DEVICE_SECRET=
API_BASE_URL=
REALM_NAME=
PERSISTENCY_PATH=persistency.d
INTERFACES_FOLDER=astarte-interfaces

CONFIG_FILE_PATH=/app/config.json

UPDATE_INTERVAL_MS=5000
TZ=Europe/Rome
COUNTRY=IT
```

Then launch it with:

`docker run --rm -it --env-file env.sh people-counter-stub`

You can also provide a custom configuration file as a volume.