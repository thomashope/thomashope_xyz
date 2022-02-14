#!/bin/bash
while sleep 0.1; do
  find src | entr -d ./build.py
done

#
# Built on top of `entr`. `brew install entr`
#
# `ctrl-z` to kill the script!
#