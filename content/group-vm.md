---
title: VM@Group
prev: "/"
next: saif-vm
---

## 1. Installing Docker and moving squid into docker:

## 2. Pass all traffic from group VM through squid and adjust firewall:

## 3. Pro and cons to using a proxy for all traffic:

There are several pros and cons to using a proxy server. Security wise, a proxy server helps with protecfting a clients computer. It works like a relay between the browser and the website, since the browser doesn't directly speak to the website, it has to go through the proxy first. The reason for the proxy to act as a relay is if the website tries something malicious, it will hit the proxy server and not the clients computer. A proxy server can also give a faster browsing experience on the clints most used sites, since a proxy server stores a local cache. Even when managing an office or a school, can a proxy server have its uses. By running all the workers/students browsing through the proxy, an administrator can easily monitor the webtraffic, since all browsing has to go through the proxy. Not only that a proxy server can also use to block specific websites eg. malicious websites, or even social media websites, to keep your employees from entering them.\
What is then bad about proxy servers? Well not much, but if the provider of the proxy server has malicious intent, it could cause harm for the client. As mentioned earlier, a proxy server keeps a cache for a faster browsing experience and to save bandwidth. THe problem with that is it could also store private information like passwords and other details, which the provider of the proxy server can have or gain access to. For that reason it is important to have trusted provider, or create a proxy server inhouse.

```python
import cv2

```


## <a name="id-1c"></a> 4. Have a common folder for the group to share files and logs

Firstly we created a folder on our group vm /usr/local/share

```
/usr/local/share
└─── Nik
│     │   subfolders
│     │   files
│     │   etc...
│     │
│     └─── share
│          │   log.txt
│          │   file112.txt
│          │   ...
│   
└─── Emin
│    │   subfolders
│    │   files
│    │   etc...
│    │
│    └─── share 
│         │   log.txt
│         │   file112.txt
│         │   ...
│
└─── Saif
     │   subfolders
     │   files
     │   etc...
     │
     └─── share
          │   log.txt
          │   file112.txt
          │   ...

```
We want it so everyone can work within their own folders, and then use their indiv







We then setup an nfs server and mount our individual folder 




5.

6.

7.
