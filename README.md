# [Tom's Website](https://thope.xyz)

## Building (mac)

`./build.py` to build the site into `public/`

`./serve.sh` to serve the built site to something like `localhost:8000`

`./auto_build.sh` will watch for directory changes in `src/` and rebuild the site automatically. Press `ctrl-z` at the terminal to suspend it, then `kill %1` to kill it!

## Building (windows)

Open a CMD at this repo

`build.py` to build

`python -m http.server --directory public` to serve

## Page Meta

```
title: Title to be displayed in the browser tab
description: Description showen on twitter cards and search engine previews
image: /2022/path/to/image.png
date: YYYY-MM-DD
published: true
featured: true
```

You can preview the rendered social card using [this site](https://www.opengraph.xyz/url/https%3A%2F%2Fthomashope.xyz%2F) or on [twitter](https://cards-dev.twitter.com/validator).

## How to Update the Favicon

Favicon was added by following [these instructions](https://dev.to/masakudamatsu/favicon-nightmare-how-to-maintain-sanity-3al7)

* Create an .svg image. vectr.com is a free online vector editor
* Upload the .svg to [Real Favicon Generator](https://realfavicongenerator.net/)
* Download the generated files. Extract favicon.ico, apple-touch-icon.png, the two android-chrome pngs, and site.webmanifest and place them in the src folder.

Just replacing the files should be enough, no need to modify the html unless something is broken.

## Publishing

You can connect to Fastmail file hosting via WebDAV on Mac via finder, or Windows from Explorer by following [these instructions](https://www.fastmail.help/hc/en-us/articles/1500000277882-Remote-file-access)

Alternatively use [Cyberduck](https://cyberduck.io) to connect to the Fastmail server. Then choose *Action > Syncronize*, select the Public folder, set the type to *Upload*, then press *Continue*.

## TODO

* publish automatically when pushing to git main
* add macro for video gif embeds {{ video, path/to/video.mp4 }}, could maybe use the attribute extension instead?
* try get the shell scripts to work on both windows and mac
* figure out how to do auto building on windows
* some kind of tip jar button
* improve 404 page
	* fancy glitch css on 404 text
	* suggest wayback machine archive link
	* suggest git repo link
* try unifying serve and publish scripts on windows and mac using python?
	- could maybe fix robocopy copying all the files every time due to timezones being different