#!/bin/bash


#docker run --d --privileged -v /var/run/docker.sock:/var/run/docker.sock \
#iptables -F
#update-alternatives --set iptables /usr/sbin/iptables-legacy
#update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

curl -sfL https://get.k3s.io | K3S_URL=${K3S_URL} K3S_TOKEN=${K3S_TOKEN} sh -