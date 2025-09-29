title: Releasing a C Library: Native Menu Bar
description: A cross platform C API for adding menus to your desktop game or app.
date: 2025-09-29
image: /2025/nmb/nmb.png
published: true
featured: true

# Library Release Alert: Native Menu Bar!

I made a C99 library for adding menus to your cross platform apps or games, you can [check it out on GitHub](https://github.com/thomashope/native-menu-bar) now!

![A screenshot of an app build with Native Menu Bar](nmb.png)

## Why?

Way back at my first game job I worked on an in house game editor built using Dear ImGui. As a developer Dear ImGui is awesome, but from a user perspective the UI could end up feeling a bit 'debug' and not quite like a 'real' professional desktop application.

Some people have spent time styling Dear ImGui and got some really good looking results! Nonetheless I think it's fair to say it isn't one of Dear ImGui's core strengths so as a team we were looking for ways to make the editor feel more native on both Mac and Windows.

One of our ideas was we could smooth things over by integrating or replacing select parts of Dear ImGui's UI with native UI elements from the current platform. We ran some experiments with overlaying native text editor boxes, modal dialogs, file pickers, and menu bars. While we did ship some of those changes to users we never shipped the native menu bars and moved onto other things.

Many years later though this idea was still kicking around in the back of my head, and while [Tiny File Dialogs](https://sourceforge.net/projects/tinyfiledialogs/) already exists I didn't see anything similar for integrating native menu bars.

This library is my attempt at filling that niche. I'd love to know if you find it useful!

## Implementation

I wrote the library in C99 instead of my regular language C++ in the hopes that it would be useable in a wider range of contexts through language bindings.

I also chose to write the library as 2 separate files instead of following the single file library trend that's been going on for a while. I have no problem with well made single file libraries but they do have their own gotchas and I think the burden of integrating 2 files into your build system is low enough that it's worth it for the peace of mind that the random library you downloaded from the internet is fully isolated from your code.

In the case of this library specifically since the Mac backend needs to be compiled as Objective-C it also makes it easier to mark it as such in your build system.

I'm not a regular Linux user but I did a little research and GTK seemed like a reasonable choice as a Linux backend with the advantage that it has implementations on Mac and Windows too. As an outsider the GTK versioning system looks like a bit of a mess but targeting GTK3 seemed like a pragmatic choice. While writing the backend though I found I could get the same code to work with both GTK2 and GTK3, as long as you ignore some of the deprecation warnings.

Perhaps it will make sense to drop the GTK2 backend or use something else entirely in the future, but for now this works good enough to prove the point.

If you have feedback or ideas you can share them on GitHub or BlueSky.

## Further Work

Ideas for further work include: a unified API for defining and responding to keyboard shortcuts, a Dear ImGui backend, more testing/examples, and new APIs for querying, iterating, deleting, or modifying menus. If you would like to contribute you can send me a message or open a PR and start a discussion.

Thanks for reading and happy coding :)