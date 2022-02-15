# Better Shell Scripts

<p>Batch and Bash scripts are never elegant, but in many scenarios they are the lowest common denominator and they get the job done. The <a href="https://betterdev.blog/minimal-safe-bash-script-template/">minimally safe bash script template</a> was doing the rounds on Hacker News a while back with some handy advice for making bash a bit less error prone.</p>

I also stumbled across <a href="https://stackoverflow.com/a/23208014">this enlightening StackOverflow</a> post, which led me to skimming the <a href="https://tldp.org/LDP/abs/html/">Advanced Bash Scripting Guide</a>.

But are there any low hanging improvements for our batch scripts on Windows?

## Better .bat

<p>One of the best tips from the minimally safe bash script template was having the script exit on the first failed command. While it seems windows dosen't have a way to exactly replicate that behavior, I was able to get something similar.</p>

```
commandThatMightFail || goto :error

... more script ...

annotherPossibleFailure || goto :error

... etc ...

goto :EOF
:error
echo Failed with error code %errorlevel%.
exit /b %errorlevel%
```

The commands after the <code>||</code> are only run if the previous command failed. In this case `goto :error` jumps to the error label, prints a message, and exits, passing out the error level from the failing command. Adding these to catch failures in the script and immediately bail out is generally much less confusing or destructive than having the script plow on regardless.

## Copying, Syncing, Compressing

<!-- TODO: add section about ROBOCOPY on windows! -->

On mac and linux you have access to `ditto` and `rsync`.

`rsync` is like a fancy version of recursive `cp`. It is geared towards copying things over the network by doing compression, deltas, and skipping unchanged files.

```
rsync -az --exclude=".DS_Store" --progress built/site network/site

# -a                        recursive archive
# -z                        compress transfer
# --exclude=".DS_Store"     skip certain files
# --progress                show copy progress
```

`ditto` does something similar, but it can also create .zip files in the process and has solved some issue I've encountered in the past with `cp` breaking symlinks inside .app bundles.

```
# copy 1 folder to another, add -v for verbose
ditto movies backup/movies

# zip at the same time.
ditto -c -k --keepParent ${APP_NAME}.app ${APP_NAME}.zip

# -c -k         creates a zip archive
# --keppParent  include the source directory in the output
#                e.g. MyApp.zip/MyApp.app/{Contents,Resources,etc.}
```

<p>Use <code>man ditto</code> and <code>man rsync</code> to learn more.</p>