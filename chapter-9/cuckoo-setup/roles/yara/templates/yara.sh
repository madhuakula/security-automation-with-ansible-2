#!/bin/bash

cd /tmp/yara-3.4.0
./bootstrap
./configure --with-crypto --enable-cuckoo --enable-magic
make
make install
cd yara-python
python setup.py build
python setup.py install