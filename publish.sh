#!/bin/bash

# puzzle together destination folder to avoid including my uname in the repo
SITE_DIR="/Volumes/webdav.fastmail.com/"
SITE_DIR="${SITE_DIR}$(ls ${SITE_DIR})/files/sites/thomashope_xyz"

SRC="public/"
DEST="${SITE_DIR}"

# If we pass an argument, only update that folder
if [ $# -eq 1 ]; then
    SRC="${SRC}$1/"
    DEST="${SITE_DIR}/$1"
fi

echo "Publishing site: ${SRC} -> ${DEST}"

time rsync -az --exclude=".DS_Store" --progress ${SRC} ${DEST}

# If we only updated a folder, also update the index
if [ $# -eq 1 ]; then
	echo "Updating index.html"
    cp "public/index.html" "${SITE_DIR}/"
fi