---
title: VM@Nikolaj
prev: saif-vm
next: emin-vm
---
## Containers
Apart from being the leading node and one of the two managers 
responsible for creating the custom overlay networks this host also 
participates in running one replica of the Hugo webservice distributed 
on the t8g1-ingress network.
One standalone container running in host mode supplies a local 
registry which purpose is to ensure 
a higher level of network integrity by allowing only a subset of 
container images to be deployed throughout all docker nodes. This 
measure is highly relevant for docker clusters running in swarm mode 
where rootless docker is not supported [See rootless docker in section: 
Group-vm](/group-vm)  

#### Hugo container
---
```shell
 docker run --rm -it \
  --name hugo \
  -v /home/nik/public/:/src \
  -p 1313:1313 \
  klakegg/hugo:ubuntu \
  server
```

## Docker swarm services
---
Docker swarm services is a convenient platform for ochestrating several 
docker nodes and services across one or multiple custom networks.
With a docker compose file we can start an entire stack of services 
with just one simple command: <code>docker stack deploy t8g1 
--compose-file docker-compose.yml</code>.
This is our compose file that has all the mentioned container services 
migrated into a single docker compose file.

```yml
version: '3'

services:
  registry:
    image: registry:2
    environment:
      - REGISTRY_HTTP_ADDR=0.0.0.0:5000
    networks:
      - t8g1-registry-overlay
    ports:
      - "5000:5000"
    volumes:
      - /mnt/registry:/var/lib/registry
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - "node.labels.registry==true"
  proxy:
    image: ubuntu/squid:latest
    environment:
      - TZ=Europe/Copenhagen
    networks:
      t8g1-squid-overlay:
    ports:
      - "8888:3128"
    volumes:
      - /etc/squid/squid.conf:/etc/squid/squid.conf
      - /srv/docker/squid/log:/var/log/squid
      - /srv/docker/squid/cache:/var/spool/squid
      - /var/cache/squid:/var/cache/squid
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - "node.labels.proxy==true"
  hugo:
    image: klakegg/hugo:ubuntu
    networks:
      - t8g1-squid-overlay
    ports:
      - "1313:1313"
    volumes:
      - /home/nik/public/:/src
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints:
          - "node.labels.hugo==true"
    command: server

networks:
  t8g1-registry-overlay:
    external: true
  t8g1-squid-overlay:
    external: true
```

We can also define networks from within the compose file, but in this 
case we flag them with the "external" parameter to let docker know not 
to create these networks.
Any service initialized on the swarm to one or more networks will also 
always attach to the swarm default ingress network.

## Security
Our reasonably hardened firewall doesn't cover mitm attacks such as 
rouge services or containers, but by utilizing docker clients extensive 
nework measure and implementing the same overriding rule on each 
individual client running docker, we can lock back down all routes and 
isntead utilize the custom t8g1-ingress network created by a managing 
node such as Group VM or Nikolaj VM. Having two or more, managing nodes 
is highly recomend for fault taularance in case of e.g. network 
failures or a single unresponsive manager. We define similar iptables 
as the group vm, but importatantly is that upon initializing the docker 
daemon we configure it to bind to only the loopback and prohibits any 
trafic outside of the required ports for swarm overlay communication.