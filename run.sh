#!/bin/bash

vault token create -policy=podcasts -ttl 5m -format json | jq -r '.auth.client_token' >./secrets/.vault-token
docker-compose up --build
