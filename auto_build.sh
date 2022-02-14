#!/bin/bash
while true; do
  ls src/* | entr -d ./build.py
done

#
# Built on top of `entr`. `brew install entr`
#
# `ctrl-z` to kill the script!
#