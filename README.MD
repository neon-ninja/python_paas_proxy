# Python PAAS Proxy

This is a WSGI proxy that can be run on free-tier PAAS providers. Tested on Azure Cloud Services, Red Hat Openshift, and Heroku - Openshift is recommended as it has the least restrictions on it's free tier (referred to as gears)  

# Why this way

Free tier PAAS providers don't allow non-http traffic, so we can't run a socks server for example. Additionally, they run multiple apps on the same IP, so apps need to be identified by the Host header - so we can't run a regular HTTP proxy - we need to recieve the target url in the query string.  

# How it works
We use the /etc/hosts file to redirect all requests for TARGET_URL to localhost, then use apache to recieve those requests and forward them to our proxy  

# Installation

Deploy this git project to red hat openshift  
Edit vhost.conf and replace "YOURURL-YOURACC" with the url to your openshift app, and replace TARGET_URL with your target url  
Copy vhost.conf to /etc/apache2/sites-enabled and restart apache (or if you're running nginx, perform the corresponding configuration changes)  
sudo echo 127.0.0.1 TARGET_URL www.TARGET_URL >> /etc/hosts  

# Check it works

curl -vv -k https://TARGET_URL - you should get a certificate error (as you don't have a valid certificate for TARGET_URL) which is ignored by the -k switch, and you can see the responding server is 127.0.0.1  
# Credits

wsgi_proxy.py heavily derived from https://bitbucket.org/dahlia/wsgi-proxy