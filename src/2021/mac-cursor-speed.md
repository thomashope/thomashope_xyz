title: Mac Cursor Speed
description: Increase the cursor speed on mac above what is allowed in the UI.

# Faster Cursor on Mac

My cursor speed was too slow, but I already had the speed maxed out in System Preferences.

Thankfully you can use `defaults` command line tool to increase the mouse speed beyond what you can do in the UI.

```
# read your current mouse speed
defaults read -g com.apple.mouse.scaling

# Set it to > 3, requires a restart to take effect
defaults write -g com.apple.mouse.scaling 9
```

There are plenty more things you can change with this tool, do `man defaults` to learn more.