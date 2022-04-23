# thomashope_xyz

## Building (mac)

`./build.py` to build the site into `public/`

`./serve.sh` to serve the built site to something like `localhost:8000`

`./auto_build.sh` will watch for directory changes in `src/` and rebuild the site automatically. Press `ctrl-z` at the terminal to suspend it, then `kill %1` to kill it!

## Building (windows)

`python build.py` to build

`python -m http.server --directory public` to serve

## Page Meta

```
title: Title to be displayed in the browser tab
description: Description showen on twitter cards and search engine previews
image: /2022/path/to/image.png
```

## TODO
* try get the shell scripts to work on both windows and mac
* figure out how to do auto building on windows