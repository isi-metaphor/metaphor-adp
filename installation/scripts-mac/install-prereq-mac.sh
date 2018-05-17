#!/bin/bash

# Prerequisities for Henry

echo Install Git:
brew install git

echo Install Sqlite:
brew install sqlite3

echo Install Python-related packages:
sudo easy_install lxml

echo Install Graphviz:
brew install graphviz

# Prerequisites for Boxer

#echo Install Subversion:
#brew install subversion

echo Install Prolog:
brew install gnu-prolog
brew install swi-prolog

echo Install wget:
brew install wget

echo Update NLTK:
git clone git://github.com/nltk/nltk.git
cd nltk
sudo python setup.py install
