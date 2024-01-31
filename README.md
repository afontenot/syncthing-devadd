# Syncthing Device Adder

A simple Python server to automatically share a folder in Syncthing with anyone
who sends a request containing their device ID.

Example request:

    curl 'http://yourdomainhere.example.org:8080/<syncthing device id>'
