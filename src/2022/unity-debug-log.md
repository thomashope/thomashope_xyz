title: Pretty Debug.log() formatting
description: How to use colored text in Unity's debug console
image: /2022/unity-debug-log/text.png
date: 2022-05-13
published: true
featured: true

# `Debug.log()` Formatting

If you’ve ever found yourself squinting at Unity's console as hundreds of messages scroll by, trying to catch the needle in the haystack, I have good news. You can use [Rich Text markup](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/StyledText.html) in `Debug.log()` strings to make things easier to spot at a glance.

<!-- ![Screen shot of Unity's debug console showing orange and green coloured text.](/2022/unity-debug-log/color.png) -->

Surround text in html style `<b></b>` tags to make it bold, or `<color=#00ff00ff></color>` to make it coloured.

The colour value can be defined either as a named colour from a [built in list](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/StyledText.html#supported-colors), or an RGBA hex code.

```csharp
Debug.Log("<b>Bold text</b>");

Debug.Log("<color=lime>Coloured text!</color>");

Debug.Log("<color=#ff00ffff><b>Bold and Coloured text!</b></color>");
```

![Image showing more coloured debug text. Shows the output of the above code sample](/2022/unity-debug-log/text.png)

Tip: If, like me, you want to display success and failure messages you may find the `red` and `green` named colours hard to read. Try `orange` and `lime` instead :)

Happy coding!