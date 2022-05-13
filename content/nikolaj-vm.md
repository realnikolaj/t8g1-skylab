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