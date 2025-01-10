#!/bin/bash

# Install Python 3.9
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-distutils

# Upgrade pip
/usr/bin/python3.9 -m pip install --upgrade pip

# Install Cloudant
/usr/bin/python3.9 -m pip install Cloudant
/usr/bin/python3.9 -m pip install ibmcloudant
/usr/bin/python3.9 -m pip install ibm-cloud-sdk-core

# Install dotenv
/usr/bin/python3.9 -m pip install python-dotenv

# Install Flask
/usr/bin/python3.9 -m pip install Flask
