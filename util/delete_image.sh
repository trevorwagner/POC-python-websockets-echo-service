#!/usr/bin/env sh

image="$(docker image ls 'ws_echo_service' -q)"
docker image rm -f "${image}"