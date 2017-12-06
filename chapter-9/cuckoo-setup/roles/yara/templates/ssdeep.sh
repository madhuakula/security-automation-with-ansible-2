#!/bin/bash

cd /tmp/ssdeep-2.14.1
./configure
./bootstrap
make
make install