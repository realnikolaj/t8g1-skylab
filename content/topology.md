---
title: Topology
prev: emin-vm
next: about
---

## Topology

<a name="id-3"></a>
***

### 3. Topology
bla bla
***

### 4.

***
### 5. Docker or lxd for our server, and why?
We have chosen to go for docker on our server. There are a couple reasons for that. Our server is rather simple, we are hosting a website using Hugo, which already has an official docker container. So it seemed like a no-brainer. lxd has many advanced features that wouldn't be utilized in out setup, therefore i makes sense to use a more userfriendly and still powerful tool like docker. A problem with docker is that we can only run one concurrent process for each container, therefore setups with multiple docker containers are fairly standard. lxc on the other hand is more than capable of runnig multiple concurrent processes in one acontainer. Docker is also far more portable and depends more on the operating system it runs on than lxd. lxd is closest to a whole operating system out of the two, it operates like a vm machine, but without a fully kitted OS. Docker is less like a virtual machine in that regard as mentioned earlier it only handles one concurrent process, which makes it ideal to have a single program running in a container.

Another importatant reason why we went with docker, is that we discovered its swarm functionality, which is very easy to setup across multiple systems. When utilizing the swarm functionality it does our dmz with the subnet for us in a much easier way, than it would have been if we were using lxd.
