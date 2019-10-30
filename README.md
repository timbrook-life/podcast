# podcast

Podcast manager and distribution

## Installing role

This uses the default role because a role binding hasn't been added to the appshell yet

```
vault write auth/kubernetes/role/podcasts \
    bound_service_account_names=podcast-service-account \
    bound_service_account_namespaces=production \
    policies=podcasts \
    ttl=1h
```
