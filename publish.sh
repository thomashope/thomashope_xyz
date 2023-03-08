#!/bin/bash

# puzzle together destination folder to avoid including my uname in the repo
DEST="/Volumes/webdav.fastmail.com/"
DEST="${DEST}$(ls ${DEST})/files/site"

SRC="public/"

echo "Publishing site: ${SRC} -> ${DEST}"

time rsync -az --exclude=".DS_Store" --progress ${SRC} ${DEST}