#!/bin/bash

echo Install henry
cd $ADP_HOME
rm -f -r henry-n700
git clone https://github.com/naoya-i/henry-n700.git

echo Compile henry
cd $ADP_HOME/henry-n700
make
