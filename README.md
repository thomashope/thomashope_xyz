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

## How to Update the Favicon

Favicon was added by following [these instructions](https://dev.to/masakudamatsu/favicon-nightmare-how-to-maintain-sanity-3al7)

* Create an .svg image. vectr.com is a free online vector editor
* Upload the .svg to [Real Favicon Generator](https://realfavicongenerator.net/)
* Download the generated files. Extract favicon.ico, apple-touch-icon.png, and site.webmanifest and place them in the src folder.

Just replacing the files should be enough, no need to modify the html unless something is broken.

## TODO
* try get the shell scripts to work on both windows and mac
* figure out how to do auto building on windows
* favicon
* some kind of tip jar button
* email newsletter signup