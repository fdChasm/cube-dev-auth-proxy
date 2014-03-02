cube-dev-auth-proxy
===================

A development proxy for the sauerbraten.org master server to allow development without the servers you are developing actually needing to contact sauerbraten.org.

This allows you to add "127.0.0.1 sauerbraten.org" to your /etc/hosts file while still being able to use the full master server list in your Sauerbraten client.

Periodically the main server list from sauerbraten.org will be fetched and requests for 'list' from this server will result in both the main server
list and those servers which have registered locally being returned.
