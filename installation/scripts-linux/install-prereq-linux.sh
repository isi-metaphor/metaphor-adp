#!/bin/bash

# Prerequisites for Henry

echo Install Git:
sudo apt-get install git-core
sudo apt-get install g++

echo Install Sqlite:
sudo apt-get install libsqlite3-dev

echo Install Python-related packages:
sudo apt-get install python-dev
sudo apt-get install python-lxml
sudo apt-get install python-nltk

echo Install Graphviz:
sudo apt-get install graphviz

# Prerequisites for Boxer

echo Install Subversion:
sudo apt-get install subversion

echo Install Prolog:
sudo apt-get install gprolog swi-prolog

echo Update NLTK:
git clone git://github.com/nltk/nltk.git
cd nltk
sudo python setup.py install
