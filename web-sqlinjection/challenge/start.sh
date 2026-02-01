#!/bin/bash

crond
echo $FLAG > /flag
unset FLAG
mv /flag /flag-$(md5sum /flag | cut -d ' ' -f 1)
cd /app
timeout $INSTANCE_TIMEOUT python app.py
