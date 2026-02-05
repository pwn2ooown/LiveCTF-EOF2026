#!/bin/sh

sed 's/dev/tmp/g' pinii > pinii_tmp # /dev/urandom -> /tmp/urandom
echo 123456789 > /tmp/urandom
