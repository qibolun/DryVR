#!/bin/bash

if [ $UID != 0 ]
then
  echo "Please run this script with sudo: sudo $0"
  exit 1
fi

apt-get install git
apt-get install python-pip
apt-get install -y libigraph0-dev
pip2 install python-igraph
pip2 install numpy sympy scipy matplotlib
git clone https://github.com/Z3Prover/z3.git
cd z3
python scripts/mk_make.py --python
cd build; make
make install
cd ../..
apt-get install glpk-utils
apt-get install gmpc-dev
apt-get install libgmp-dev
wget ftp.gnu.org/gnu/glpk/glpk-4.39.tar.gz
tar -xvzf glpk-4.39.tar.gz 
cd glpk-4.39
./configure
make install
cd ..
pip2 install glpk
export LD_LIBRARY_PATH=/usr/local/lib
apt-get install python-cairo
apt-get install -y python-tk

