#!/usr/bin/env bash

clear
docker run -it --rm \
  -p 9005:9005 \
  --name 'ws_echo_service' \
  'ws_echo_service'