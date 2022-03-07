#!/bin/bash

echo "Starting k3s on ${HOSTNAME}, connecting to ${K3S_URL}"
/opt/k3s/k3s-arm64 agent
