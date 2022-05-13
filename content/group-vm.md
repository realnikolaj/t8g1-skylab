---
title: VM@Group
prev: "/"
next: topology
---

# Group VM
***
## Squid
### 1. Installing Docker and moving squid into docker:
Installing docker on our group vm requires carefull considerations regarding the security measure already implemented. 
If a 
rootless docker principle is 
not established on the docker host, any container running will have root privileges which isn't really an issue for 
veteran sysadmins that knows have to restrict access to the docker daemon using aswell firewall or custom docker 
registries to allow only vetted and verified container images to run, but in the hands of non-experienced employee a 
non-rootless docker client will run any code within any docker image. 
The second major 
concern is regarding 
the iptables chains and rules applied to the group vm acting as the network's firewall. The group vm acts as a router 
for our 
internal network and routes network traffic between clients and forwards client trafic to the internet using Network 
Address so that any packets originating from our clients destined to the internet will have their source headers 
translated to that if the internet facing router i.e. our group host. Upon starting the docker daemon, the socket 
responsible for talking to the docker client service and the containers within, new docker specific chains and rules 
gets
applied to the iptables with the <code>-I</code> prefix for insertion. This is not a major concern if your aware of 
this fact, but the <code>FORWARD</code> chain policy gets set to <code>DROP</code> 
requiring
manual 
configuration to any 
docker host also acting as a router.
From docker documentation this iptables rule is supplied to help reenable ip forwarding:
```Sh
 $ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```
We've opted to run the docker in root mode for a few reasons:
1. We're under development and only configurations and log files could contain sensitive information about the 
   networks' inner workings, parameters that would resemble many other networks thus if there were to be an exploit 
   in our parameters we would likely be able to mitigate these before production.
2. Being forced to make the aforementioned critical considerations allows for a good learning environment, producing 
   a highly skilled, security oriented IT staff.
3. Docker swarm isn't supported under rootless docker mode.

** Squid container
Using the default image registry supplied with docker, we pull and run the <code>ubuntu:squid</code> container using 
this run configuration to enable host network traficking directly to the squid container:
```Sh
$ docker run -d --name squid -p  \
         --volume /etc/squid/squid.conf:/etc/squid/squid.conf \
         --volume /srv/docker/squid/log:/var/log/squid \
         --volume /srv/docker/squid/cache:/var/cache/squid \
         -e TZ=Europe/Copenhagen \
         ubuntu/squid:latest
```


## Proxy
***
### 2. Pass all traffic from group VM through squid and adjust firewall:

Below configuration implements policy routing for separate gateway and 
squid hosts

```Sh
# IPv4 address of proxy
PROXYIP4= 192.168.0.10

# IPv6 address of proxy
PROXYIP6= fe80:dead:beef::10

# interface facing clients
CLIENTIFACE= eth0

# arbitrary mark used to route packets by the firewall. May be anything from 1 to 64.
FWMARK= 2


# permit Squid box out to the Internet
iptables -t mangle -A PREROUTING -p tcp --dport 80 -s $PROXYIP4 -j ACCEPT
ip6tables -t mangle -A PREROUTING -p tcp --dport 80 -s $PROXYIP6 -j ACCEPT

# mark everything else on port 80 to be routed to the Squid box
iptables -t mangle -A PREROUTING -i $CLIENTIFACE -p tcp --dport 80 -j MARK --set-mark $FWMARK
iptables -t mangle -A PREROUTING -m mark --mark $FWMARK -j ACCEPT
ip6tables -t mangle -A PREROUTING -i $CLIENTIFACE -p tcp --dport 80 -j MARK --set-mark $FWMARK
ip6tables -t mangle -A PREROUTING -m mark --mark $FWMARK -j ACCEPT

# NP: Ensure that traffic from inside the network is allowed to loop back inside again.
iptables -t filter -A FORWARD -i $CLIENTIFACE -o $CLIENTIFACE -p tcp --dport 80 -j ACCEPT
ip6tables -t filter -A FORWARD -i $CLIENTIFACE -o $CLIENTIFACE -p tcp --dport 80 -j ACCEPT
```
### 3. Pro and cons to using a proxy for all traffic:

There are several pros and cons to using a proxy server. Security wise, a proxy server helps with protecfting a clients computer. It works like a relay between the browser and the website, since the browser doesn't directly speak to the website, it has to go through the proxy first. The reason for the proxy to act as a relay is if the website tries something malicious, it will hit the proxy server and not the clients computer. A proxy server can also give a faster browsing experience on the clints most used sites, since a proxy server stores a local cache. Even when managing an office or a school, can a proxy server have its uses. By running all the workers/students browsing through the proxy, an administrator can easily monitor the webtraffic, since all browsing has to go through the proxy. Not only that a proxy server can also use to block specific websites eg. malicious websites, or even social media websites, to keep your employees from entering them.\
What is then bad about proxy servers? Well not much, but if the provider of the proxy server has malicious intent, it could cause harm for the client. As mentioned earlier, a proxy server keeps a cache for a faster browsing experience and to save bandwidth. THe problem with that is it could also store private information like passwords and other details, which the provider of the proxy server can have or gain access to. For that reason it is important to have trusted provider, or create a proxy server inhouse.

## NFS
***
### 4. Have a common folder for the group to share files and logs

Firstly we create a folder for every individual on our group vm /usr/local/share with this kind of folder structure:

```
/usr/local/share
└─── nik
│    │   files
│    │   etc...
│    └─  subfolders
│   
└─── emin
│    │   files
│    │   etc...
│    └─  subfolders
│
└─── saif
│     │   files
│     │   etc...
│     └─  subfolders
│
└─── shared
      │   saif-logs.txt
      │   emin-logs.txt
      │   nik-logs.txt
```
We want it so everyone can work within their own folders, and then use the share folder to share logs and other files. We want to make sure everyone only has access to their individual folder, while they all have access to the share folder. Although they should only be able to modify and delete their own files in the share folder. \
First we want to make sure permissions are correct, and we start by adding a group, and a user for each individual. We then assign each individual to their own group and to the main group.

```sh
$ groupadd t8g1-skylab
$ groupadd emin/nik/saif
```
```sh
$ useradd emin/nik/saif
```
```sh
$ usermod -a -G t8g1-skylab emin/nik/saif
$ usermod -a -G emin/nik/saif emin/nik/saif
```
After adding groups and assigning the individual users to the desired group we assign each directory to a group.


```sh
$ chgrp -R emin/nik/saif /usr/local/share/(emin/nik/saif)
$ chgrp -R t8g1-skylab /usr/local/share/shared
```
After assigning each directory to a group, we can then set permissions.
```sh
$ chmod g+w /usr/local/share/(emin/nik/saif)
$ chmod g+w /usr/local/share/shared
```
Now each individual has access to their own directory, and the all have access to the shared directory. Now we have to make it so only the creator of the file in the shared direcotry can modify it.
```sh
chmod +t /usr/local/share/shared
```
We then setup an nfs server and mount our individual folder and the shared folder on our individual vms. We setup the nfs server on our group vm, and make sure we give rw access, so if the user mounting the nfs is in the correct group, he or she shoud have rw access.\
To mount the nfs filesystem we need to have the nfs client package installed. 
```sh
$ sudo apt install nfs-common
```
Then we mount:
```sh
$ sudo mount -t nfs 192.168.165.1:/usr/local/share/(shared_or_emin...) /the_directory_we_want_to_mount_it_on_local_machine
```
We can now through our own machine access our directories and the shared directory


## Custom ingress
***
### 6. Install a service in docker of your choosing as group which you 
think will need to share amongst the group, 
      for example authentication server, DNS server etc. Create a DMZ(a separate subnet –maybe a 10 subnet with your 
      group number as subnet such as t1g1 is 10.11 and t1g2 is 10.12 and so on ) 

We've opted to present a static website using Hugo and its official docker container as a service on the docker swarm. 
The 
service is created and attached to a 
custom ingress network which is a an overlay type network exclusive for docker nodes running in swarm mode. The ingress 
network and any other custom overlay networks are connected to the docker daemons physical network on each 
individiul node through a virtual bridge <code>docker_gwbridge</code> enabling each node accept trafic destined for 
the swarm service even when no task is running on the specific node. This relieves 
the need 
for for 
manually 
creating a subnet or DMZ zone on our dhcp 
server and negates the need for manipulating the iptables in our firewall, since this is done by the docker service. A 
docker swarm automatically 
initializes 
an overlay network called <code>ingress</code> which we reconfigured using the bellow commands:
```Sh
 $ docker network rm ingress
 $ docker network create \
    --driver overlay \
    --ingress \
    --subnet=10.81.0.0/16 \
    --gateway=10.81.0.2 \
    --opt com.docker.network.driver.mtu=1200 \
    t8g1-ingress
```
The ingress network, and any 
overlay type 
networks encrypts management trafic between the nodes rotating the AES key every 12 hours. A docker swarm 
also allows for splitting management and data trafic onto separate network interfaces using the 
<code>--advertise-addr</code> and <code>--datapath-addr</code> for each node when joining the swarm or at swarm 
initialization. 
Overlay networks such as the ingress network and any custom overlay networks acts 
as a 
load-balancing proxy for optimizing connections to the services within them, which a: improves loading time for 
requests to services with replicas i.e. multiple, indentical and independent tasks of a single service 
distributed in the swarm and b: 
enables 
sys-admins to create custom policies for updating services allowing rules to keep a certain amount of tasks running 
at all times during the update process and thus increasing availability to the service.  
Only custom overlay networks i.e. networks created without the parameter and option: <code>--mode ingress</code> permits
setting 
the 
attachable flag enabling 
standalone containers to attach to 
the network.
It is recommended to always create separate custom overlay networks for independent services.

## Mad docker
***
### 7. Update the firewall to allow limited traffic from DMZ only to be able to use that service 

As mentioned simple firewall rules gets cluttered by the docker clients running on each node. Extensive measure must 
be taken to secure the network and especially the containers running withing it.
As a deafult docker will open any published ports from services and standalone containers to the external network, 
and running these services and containers in a non-rootless docker environment which is dictated by the docker 
engine when running docker in swarm mode, exposes the integrety of the entire network. Luckyli the official 
documentation for docker is an endless source of consideration and warnings regarding the "feature" and supplies 
several recommendations for securing the environment.
Docker creates new iptables chains per default and drops all forwarding on the host, which is an issue for the group 
vm which also acts as a router. The following command reenables forwarding on the group vm:
```Sh
$ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```
When starting a service or a container created with the flags <code>--publish [host_port]:[container_port]</code> 
docker will 
insert 
rules in the 
DOCKER chain opening the specified host port on the interface upon which docker binds which is <code>0.0.0.0</code> 
by default. This means that docker will listen for any incomming requests on those ports from any interface on the 
host!
A simply but not commonly known fix is to specifiy the entire host and port on which to listen for requests: 
<code>--publish 192.168.165.1:3128:3128</code>.
At first having such a significant setting enabled by default seems malignant, but it actually offers a very 
opportune scenario where we can restrict access to the network pre-docker, blocking any and all 
trafic not originating 
from within the network, and let docker and running containers or services dictate which ports to open. 
We consider this way of configuring the firewall optimal given the requirements posed upon our network by 
docker.
The following table implemented on our group vm drops all trafic except ssh trafic to the network, outgoing connections 
from withing the internal LAN and then uses the DOCKER_USER chain to insert custom rulesets that will do the very 
same thing only this chain superceeds the DOCKER chain that initializes once the docker service is running, this 
incremental configuration is remniscent of common UNIX package and services behavior where administrator are 
instructed or discouraged from altering the default configuration files and instead use custom user configuration 
which the package software will se as overruling to any default settings and also like how shell profile scripts 
exists at various levels for contemplating structured and context aware behavior such as simply providing defaults 
to multiple users and allowing users to overrule the defaults. 

```Sh
#!/bin/bash
INET_IF=eth0
IPTABLES=/usr/sbin/iptables

#This will purge the firewall rules
$IPTABLES -F
$IPTABLES -t nat -F
$IPTABLES -X

#A new chain "block" is used and will new connection from within and accept only already established by LAN connections
#Incoming tcp trafic is accepted to the default ssh port 22
#Anything else gets droped ... but only until starting a docker container/service that listens on a port
$IPTABLES -N block
$IPTABLES -A block -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$IPTABLES -A block -m conntrack --ctstate NEW ! -i  $INET_IF -j ACCEPT
$IPTABLES -A block -p tcp --dport ssh -j ACCEPT
$IPTABLES -A block -j DROP

#These chains gets redirected to the block chain, they're needed for actually providing the block chain with trafic
$IPTABLES -A INPUT -j block
$IPTABLES -A FORWARD -j block

#Here we use the "-I" option to skip or circumvent any docker created rules and go straight to the block chain
#This rule also works for reenabling FORWARDING on hosts running docker that also must suply routing capabilities 
#for our network
$IPTABLES -I DOCKER_USER -j block

#If external access is actually needed or if connection tracking isn't wanted from DOCKER originating packets
#those rules must be prepended aswell to apply before the redirect rule above.
#EXAMPLE: #iptables -I DOCKER-USER -i $src_if -o $dst_if -j ACCEPT

#Masquerade
$IPTABLES -t nat -A POSTROUTING -o $INET_IF -j MASQUERADE
```