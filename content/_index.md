---
title: IT@T8G1-Skylab
layout: single
next: Group-vm
---
<style>

h2{
    font-weight: 500;
}
.card {
  /* Add shadows to create the "card" effect */
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.3);
    transition: 0.3s;
    padding: 12px 20px;
    margin: 16px;
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

</style>

## This project consists of four main clustering nodes
### See task list bellow the cards

# At T8G1-Skylab we host, deploy and maintain services used by workers throughout the organization. Our philosophy is:  
> Can it be written into a feature request - then we can deploy it.


<div class="cardContainer">
    <div class="card">
        <h2>VM@Group</h2>
        <ul>
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
        <ul>
            <li>Docker worker node</li>
            <li>File server container</li>
        </ul>
        <a href="Saif-vm">See more</a>
    </div>
    <div class="card">
        <h2>VM@Nikolaj</h2>
         <ul>
            <li>Docker svarm manager</li>
            <li>Logwatch server</li>
        </ul>
        <a href="network-analysis">See more</a>
    </div>
    <div class="card">
        <h2>VM@Emin</h2>
        <ul>
            <li>Docker worker node</li>
            <li>TEXT</li>
        </ul>
        <a href="Emin-vm">See more</a>
    </div>
</div>

## About
This site presents the internal services and their configurations provided by IT@T8G1-Skylab group, the cluster's 
network topology and documentation for users and administrators along with the security implemented and how to do a feature request.

### Tasks

1. On group VM:
   1. [x] Install Docker on Group VM and move squid into docker  
   2. [x] Make it possible that all traffic originating from GroupVM should pass through squid and firewall is 
      adjusted accordingly  
   3. [ ] Analyze the pros/cons of using proxy for all traffic originating from individual VMs in the group and decide  
        on it. Document your resons and choice and do the needful depending on the decision  
   4. [ ] Make it possible for all individual members of the group to be able to share documents in a common folder 
      where they will update logs of what change they have made to the Group VM and only the owner of the file is 
      able to modify/delete the file. Rest should be able to read all information in the file. So, each member should have his own file  
   5. [ ] [optional] place log files in a container separate container. How does it affect security  
   6. [ ] Install a service in docker of your choosing as group which you think will need to share amongst the group, 
      for example authentication server, DNS server etc. Create a DMZ(a separate subnet –maybe a 10 subnet with your 
      group number as subnet such as t1g1 is 10.11 and t1g2 is 10.12 and so on )  
   7. [ ] Update the firewall to allow limited traffic from DMZ only to be able to use that service  
2. In your individual VM
    1. [x] Setup & Configure the LXD or docker  
    2. [ ] [optional] get ip address for LXD or Docker from dhcp server on
groupVM  
    3. [ ] Setup security for your individual server and the containers you will run  
    4. [ ] Discuss the security and other networking considerations for keeping containers isolated from local 
       network and making them available over the local network  
3. Design a network topology (not configure) for the whole group  
   1. [ ] Database server (mysql, mongo,postgres)  
   2. [ ] Webserver (nginx,apache, caddy)  
   3. [ ] Real time communication server (jitsi, matrix)
   4. [ ] Git server  
   5. [ ] Any other type of container you think will be relevant
   6. [ ] File server (Seafile, owncloud,nextcloud)  
4. [ ] Decide where in the topology will you place the various servers. Setting up lxd on GroupVM is not a trivial task 
   so anything there has to docker but in the documentation you can argue if you would rather used lxd and why?  
5. [ ] Which virtualization technology between docker and lxd will you use for the particular server and why?  
6. [ ] You should setup minimum of two docker container or lxd container on your individual VM  
7. [ ] [optional] you can configure both docker and LXD and make them work together  
8. [ ] Reasonable firewall and other security measures should be implemented and documented for the groupVM and the 
   individual VM  
9. [ ] Setup and discuss the security for each server(container) individually and for the setup as a whole  
   1. [ ] What do you think the security is for your setup  
   2. [ ] Talk about strength and vulnerabilities of your infrastructure  
10. [ ] Launch attacks like DDOS on other servers, use various tools to check
vulnerabilities in the server setup of other groups  
    1. [ ] You can reconfigure your switch(just add the vlan of the group
so that you can get ip from their dhcp) to access other groups local network in the class  
    2. [ ] Then you can run these vulnerability scanners like nmap and nikto to find out more about their network, 
       services etc.  
    3. [ ] Document your findings, vulnerabilities and suggest way to protect/attack the vulnerabilities  

62501 Linux Server and Network Course at DTU, spring 2022 edition.

## [Read the report](t8g1-skylab-repport.html)
