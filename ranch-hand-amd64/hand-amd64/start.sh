#!/bin/bash

## balenaRancher/ranch-hand-amd64/start.sh
## Sam Dennon//2022

if [[ -z "$DEVICE_HOSTNAME" ]]; then
  DEVICE_HOSTNAME=$BALENA_DEVICE_NAME_AT_INIT
  HOSTNAME=$DEVICE_HOSTNAME
fi

curl -s -X PATCH --header "Content-Type:application/json" \
  --data '{"network": {"hostname": "'"${DEVICE_HOSTNAME}"'"}}' \
  "$BALENA_SUPERVISOR_ADDRESS/v1/device/host-config?apikey=$BALENA_SUPERVISOR_API_KEY" >/dev/null

echo "Starting k3s on ${HOSTNAME}, connecting to ${K3S_URL}"
/opt/k3s/k3s agent
