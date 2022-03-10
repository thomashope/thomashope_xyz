#!/bin/bash
while sleep 0.1; do
  echo
  echo "Script is running in a loop, press ctrl-z to suspend it, then type 'kill %1' to kill it!"
  echo
  find src | entr -d ./build.py
done

#
# Built on top of `entr`. `brew install entr`
#