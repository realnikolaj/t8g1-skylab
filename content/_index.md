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
    1. [x] Setup & Configure the LXD or docker  
    2. [ ] ~~[optional] get ip address for LXD or Docker from dhcp server on
groupVM~~
    3. [x] Setup security for your individual server and the containers 
       you will run [See Security in section: nikolaj-vm](/nikolaj-vm)
    4. [x] Discuss the security and other networking considerations for keeping containers isolated from local 
       network and making them available over the local network [See Security in section: nikolaj-vm](/nikolaj-vm)
3. Design a network topology (not configure) for the whole group  
   1. [ ] Database server (mysql, mongo,postgres)  
   2. [ ] Webserver (nginx,apache, caddy)  
   3. [ ] Real time communication server (jitsi, matrix)
   4. [ ] Git server  
   5. [ ] Any other type of container you think will be relevant
   6. [ ] File server (Seafile, owncloud,nextcloud)  
4. [ ] Decide where in the topology will you place the various servers. Setting up lxd on GroupVM is not a trivial task 
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
9. [ ] ~~Setup and discuss the security for each server(container) 
   individually and for the setup as a whole~~  
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

<cardContainer id="singlecard"> <span class="vm-card"></span>
    <div class="card"> 
        <h2>VM@Group</h2>
        <ul id="double"> <span class="group-list"></span>
          <li>Docker swarm manager</li>
          <li>Squid proxy container</li>
          <li>Firewall</li>
          <li>DHCP server</li>
        </ul>
        <a href="Group-vm">See more</a>
    </div>
</div>
<div class="cardContainer">
    <div class="card">
        <h2>VM@Saif</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker worker node</li>
          <li>File server container</li>
        </ul>
        <a href="saif-vm">See more</a>
    </div>
    <div class="card">
        <h2>VM@Nikolaj</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker swarm manager</li>
          <li>Hugo service replica</li>
          <li>Image registry container</li>
        </ul>
        <a href="nikolaj-vm">See more</a>
    </div>
    <div class="card">
        <h2>VM@Emin</h2>
        <ul id="single"> <span class="student-list"></span>
          <li>Docker worker node</li>
          <li>TEXT</li>
        </ul>
        <a href="emin-vm">See more</a>
    </div>
</div>

## [Read the report](t8g1-skylab-repport.html)
