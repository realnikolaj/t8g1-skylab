---
title: T8G1-Skylab
layout: single
next: group-vm
---
<style>

h2{
    font-weight: 500;
}
.card {
  /* Add shadows to create the "card" effect */
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.3);
    transition: 0.3s;
    padding: 10px 10px;
    margin: 8px;
    border-radius: 15px;
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 12px 20px 0 rgba(0,0,0,0.3);
}

.cardContainer {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
}

/* Add some padding inside the card container */

#double li  {width:50%; display:inline flex} <span class="group-list">/* 2 col */</span>
#single li  {width:15%;} <span class="student-list">/* 1 col </span>

#singlecard .cardContainer  {} <span class="vm-card">/* 1 col </span>

</style>


## About
This site presents the internal services and their configurations provided by T8G1-Skylab group, the cluster's 
network topology and documentation for users and administrators along 
with the security implemented within the network.
[See the public repository for this site here]

## Tasks
***

1. On group VM:
   1. [x] Install Docker on Group VM and move squid into docker  
      [See Docker in section: Group-vm](/group-vm)   
   2. [x] Make it possible that all traffic originating from GroupVM should pass through squid and firewall is 
      adjusted accordingly  [See Squid in section: Group-vm](/group-vm)  
   3. [x] Analyze the pros/cons of using proxy for all traffic 
      originating from individual VMs in the group and decide on it. 
      Document your resons and choice and do the needful depending on 
      the decision. [See Proxy in section: Group-vm](/group-vm)
   4. [x] Make it possible for all individual members of the group to be able to share documents in a common folder 
      where they will update logs of what change they have made to the Group VM and only the owner of the file is 
      able to modify/delete the file. Rest should be able to read all 
      information in the file. So, each member should have his own file
      [See NFS in section: #2: Group-vm](/group-vm)
   5. [ ] ~~[optional] place log files in a container separate container. How does it affect security~~  
   6. [x] Install a service in docker of your choosing as group which 
      you think will need to share amongst the group, 
      for example authentication server, DNS server etc. Create a DMZ(a separate subnet –maybe a 10 subnet with your 
      group number as subnet such as t1g1 is 10.11 and t1g2 is 10.12 
      and so on )  [See Custom ingress in section: Group-vm](/group-vm)  
   7. [x] Update the firewall to allow limited traffic from DMZ only to 
      be able to use that service  [See Mad docker in section: 
      Group-vm](/group-vm)
2. In your individual VM
    1. [x] Setup & Configure the LXD or docker  [See Host cards in section: 
   T8G1-Skylab](/)
    2. [ ] ~~[optional] get ip address for LXD or Docker from dhcp server on
groupVM~~
    3. [x] Setup security for your individual server and the containers 
       you will run [See Security in section: nikolaj-vm](/nikolaj-vm)
    4. [x] Discuss the security and other networking considerations for keeping containers isolated from local 
       network and making them available over the local network [See Security in section: nikolaj-vm](/nikolaj-vm)
3. Design a network topology (not configure) for the whole group  
   1. [ ] ~~Database server (mysql, mongo,postgres)~~  
   2. [ ] Webserver (nginx,apache, caddy)  [See Topology in section: 
   Topology](/topology)    
   3. [ ] ~~Real time communication server (jitsi, matrix)~~
   4. [ ] ~~Git server~~  
   5. [x] Any other type of container you think will be relevant [See Topology in section: 
   Topology](/topology)    
   6. [x] File server (Seafile, owncloud,nextcloud)  [See Topology in section: 
   Topology](/topology)    
4. [x] Decide where in the topology will you place the various servers. 
   Setting up lxd on GroupVM is not a trivial task 
   so anything there has to docker but in the documentation you can 
   argue if you would rather used lxd and why? [See Containers in section: 
   Topology](/topology)    
5. [x] Which virtualization technology between docker and lxd will you 
   use for the particular server and why? [See Containers in section: 
   Topology](/topology)  
6. [x] You should setup minimum of two docker container or lxd 
   container on your individual VM [See Host cards in section: 
   T8G1-Skylab](/)  
7. [ ] ~~[optional] you can configure both docker and LXD and make them work together~~  
8. [x] Reasonable firewall and other security measures should be implemented and documented for the groupVM and the 
   individual VM  [See Mad docker in section: group-vm](/group-vm) & [Security in section: nikolaj-vm](/nikolaj-vm)
9. [x] Setup and discuss the security for each server(container) 
   individually and for the setup as a whole [See Mad docker in section: group-vm](/group-vm) & [Security in section: nikolaj-vm](/nikolaj-vm)  
   1. [ ] ~~What do you think the security is for your setup~~  
   2. [ ] ~~Talk about strength and vulnerabilities of your infrastructure~~  
10. [ ] ~~Launch attacks like DDOS on other servers, use various tools to check~~
vulnerabilities in the server setup of other groups  
    1. [ ] ~~You can reconfigure your switch(just add the vlan of the group
so that you can get ip from their dhcp) to access other groups local network in the class~~  
    2. [ ] ~~Then you can run these vulnerability scanners like nmap and nikto to find out more about their network, 
       services etc.~~  
    3. [ ] ~~Document your findings, vulnerabilities and suggest way to protect/attack the vulnerabilities~~  

62501 Linux Server and Network Course at DTU, spring 2022 edition.

## T8G1-Skylab
***
### Host cards
This configuration contains four docker worker nodes with two of them 
assigned the swarm managing role.

<carContainer id="singlecard"> <span class="vm-card"></span>
    <div class="card"> 
        <h2>VM@Group</h2>
        <ul id="double"> <span class="group-list"></span>
          <li>Docker swarm manager</li>
          <li>Squid proxy</li>
          <li>Firewall</li>
          <li>DHCP server</li>
        </ul>
        <a href="group-vm">See more</a>
    </div>
</div>
<div class="cardContainer">
    <div class="card">
        <h2>VM@Saif</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker worker</li>
          <li>Jira container</li>
        </ul>
        <a href="saif-vm">See more</a>
    </div>
    <div class="card">
        <h2>VM@Nikolaj</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker swarm manager</li>
          <li>Hugo replica</li>
          <li>Image registry</li>
        </ul>
        <a href="nikolaj-vm">See more</a>
    </div>
    <div class="card">
        <h2>VM@Emin</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker worker </li>
          <li>Unbound DNS</li>
        </ul>
        <a href="emin-vm">See more</a>
    </div>
</div>

## [Read the report](t8g1-skylab-repport.html)


# Group VM

## Rootless docker
***
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

## Squid
***
### 1. Installing Docker and moving squid into docker:
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

# arbitrary mark used to route packets by the firewall. May be anything \
# from 1 to 64.
FWMARK= 2


# permit Squid box out to the Internet
iptables -t mangle -A PREROUTING -p tcp --dport 80 -s $PROXYIP4 -j ACCEPT
ip6tables -t mangle -A PREROUTING -p tcp --dport 80 -s $PROXYIP6 -j ACCEPT

# mark everything else on port 80 to be routed to the Squid box
iptables -t mangle -A PREROUTING -i $CLIENTIFACE -p tcp --dport 80 -j \
MARK --set-mark $FWMARK
iptables -t mangle -A PREROUTING -m mark --mark $FWMARK -j ACCEPT
ip6tables -t mangle -A PREROUTING -i $CLIENTIFACE -p tcp --dport 80 -j \ 
MARK --set-mark $FWMARK
ip6tables -t mangle -A PREROUTING -m mark --mark $FWMARK -j ACCEPT

# NP: Ensure that traffic from inside the network is allowed to loop \  
#back inside again.
iptables -t filter -A FORWARD -i $CLIENTIFACE -o $CLIENTIFACE -p tcp \  
--dport 80 -j ACCEPT
ip6tables -t filter -A FORWARD -i $CLIENTIFACE -o $CLIENTIFACE -p tcp \ 
 --dport 80 -j ACCEPT
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

#A new chain "block" is used and will new connection from within and 
# accept only already established by LAN connections
#Incoming tcp trafic is accepted to the default ssh port 22
#Anything else gets droped ... but only until starting a docker
# container/service that listens on a port
$IPTABLES -N block
$IPTABLES -A block -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$IPTABLES -A block -m conntrack --ctstate NEW ! -i  $INET_IF -j ACCEPT
$IPTABLES -A block -p tcp --dport ssh -j ACCEPT
$IPTABLES -A block -j DROP

#These chains gets redirected to the block chain, they're needed for
# actually providing the block chain with trafic
$IPTABLES -A INPUT -j block
$IPTABLES -A FORWARD -j block

#Here we use the "-I" option to skip or circumvent any docker created
# rules and go straight to the block chain
#This rule also works for reenabling FORWARDING on hosts running docker
# that also must suply routing capabilities 
#for our network
$IPTABLES -I DOCKER_USER -j block

#If external access is actually needed or if connection tracking isn't 
# wanted from DOCKER originating packets
#those rules must be prepended aswell to apply before the redirect rule
# above.
#EXAMPLE: #iptables -I DOCKER-USER -i $src_if -o $dst_if -j ACCEPT

#Masquerade
$IPTABLES -t nat -A POSTROUTING -o $INET_IF -j MASQUERADE
```


## Topology
***
### 3. Topology

<img src="/images/Networkdiagram.png" width="800" />

We have now designed a sketch of our network topology, which can be seen in the picture above. 
 In the diagram we show that we are hosting HUGO webserver in a docker 
 container through subnet 10.81. We also used t8g1-ingress overlay network 
 which has the benefits of automatically creating a subnet that of which,
 by 
 our individual VM's strict firewall rules [See Security in section: nikolaj-vm](/nikolaj-vm), is isolated from the 
 network and per docker's generous trafic acceptance strategy as in: 
 accepting 
 anything and everything from anywhere to everywhere, effectively becomes 
 a DMZ zone.

### 5. Docker or lxd for our server, and why?
We have chosen to go for docker on our server. There are a couple reasons for that. Our server is rather simple, we are hosting a website using Hugo, which already has an official docker container. So it seemed like a no-brainer. lxd has many advanced features that wouldn't be utilized in out setup, therefore i makes sense to use a more userfriendly and still powerful tool like docker. A problem with docker is that we can only run one concurrent process for each container, therefore setups with multiple docker containers are fairly standard. lxc on the other hand is more than capable of runnig multiple concurrent processes in one acontainer. Docker is also far more portable and depends more on the operating system it runs on than lxd. lxd is closest to a whole operating system out of the two, it operates like a vm machine, but without a fully kitted OS. Docker is less like a virtual machine in that regard as mentioned earlier it only handles one concurrent process, which makes it ideal to have a single program running in a container.

Another importatant reason why we went with docker, is that we discovered its swarm functionality, which is very easy to setup across multiple hosts. It is also very powerful. [See Security in mad docker in section: group-vm](/group-vm) When utilizing the swarm functionality it does our dmz with the subnet for us in a much easier way, than it would have been if we were using lxd.


## Docker worker node
***
>Hugo task service


## Jira Container
***
In my personal vm i want to set up a jira container
Since we want to be a hosting, deployment and infrastructure service, it would be essential to have a tool to help us with managing our projects. Jira is basically a ticket managing software, which will help us delegate work and help us with bug tracking.
To set it up it will be as simple as to use the jiras docker image (I hope)

## Containers
***
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
***
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

## Unbound 
***
I want to implement an Unbound DNS in a container. Unbound is a 
recursive DNS resolver, which has the benefits of increasing online 
privacy. Furthermore, a user can encrypt communication because it 
supports DNS-over-HTTPS and DNS-over-TLS and unbound also makes sure 
that the data which is exchanged to the authoritative servers are 
limited. All this makes the DNS stronger which help to improve privacy. 
We want to use unbound because it is one of the best ways to secure a 
DNS server.       

Group T8G1

Project Assignment

62501 Linux Server and Network Course at DTU, spring 2022 edition.

![](/images/dtu-logo.png)

<img src="/images/dtu-logo.png" width="200" />
