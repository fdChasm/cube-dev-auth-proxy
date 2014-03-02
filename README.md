cube-dev-auth-proxy
===================

A development proxy for the sauerbraten.org master server to allow development without the servers you are developing actually needing to contact sauerbraten.org.

This allows you to add "127.0.0.1 sauerbraten.org" to your /etc/hosts file while still being able to use the full master server list in your Sauerbraten client.

Periodically the main server list from sauerbraten.org will be fetched and requests for 'list' from this server will result in both the main server
list and those servers which have registered locally being returned.

dependencies
============

* python2.7
* twisted
* pycube2common
* pycube2crypto
* pycube2protocol

getting started
===============

```Shell
# Add entry to /etc/hosts
git clone https://github.com/fdChasm/cube-dev-auth-proxy.git
cd cube-dev-auth-proxy
pip install -r requirements.txt
cd src
# edit main.py with any auth public keys you desire
python2.7 main.py
```
