#!/bin/bash

vault token create -policy=podcasts -ttl 1m -format json | jq -r '.auth.client_token' >/var/run/secrets/.vault-token
consul-template -config ./conf/config.hcl
