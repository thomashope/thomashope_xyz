title: Fixing the Home and End Keys on MacOS
description: With a little Cocoa trick form the early days of NeXT
image: /2022/home-end/keys.jpg

# Fixing the Home and End Keys

On Windows, in most text editing situations, the Home and End keys move the cursor to the start and end of the current line respectively. On Mac they apparently scroll you to the start or end of the current document, in my opinion this is much less useful.

## Introducing DefaultKeyBindings.dict

Thankfully on mac we can change how native text boxes behave system wide using a file called `DefaultKeyBindings.dict`.

If, like me, you just want to make the Home and End keys do the same as they do on windows, copy and paste this into a new file called `DefaultKeyBindings.dict`, then place it in `~/Library/KeyBindings/`.

```
{
  "\UF729"  = "moveToBeginningOfLine:";                   /* Home         */
  "\UF72B"  = "moveToEndOfLine:";                         /* End          */
  "$\UF729" = "moveToBeginningOfLineAndModifySelection:"; /* Home + Shift */
  "$\UF72B" = "moveToEndOfLineAndModifySelection:";       /* End + Shift  */
}
```

If you are unfamiliar with the `~/Library` folder you can access it from finder by pressing `CMD+SHIFT+G`, typing `~/Library`. and pressing enter. If the `KeyBindings` folder doesn't exist create it.

## Customisation

For an in depth look at this feature checkout [Customizing the Cocoa Text System](https://web.archive.org/web/20191223051449/http://www.hcs.harvard.edu/~jrus/site/cocoa-text.html) published by Jacob Rus while at Harvard in 2006. But here's a brief overview to wet your appetite.

The syntax of `DefaultKeyBindings.dict` is apparently that of a NeXT era property list. Basically it's a dictionary with the keyboard shortcut as the key and action to be taken (a.k.a. Objective-C selector) as the value.

The shortcut can be include control characters, letters, and unicode character sequences for non-letter keys.

```
"a" for the lowercase letter
"A" for the uppercase (shifted) version

"^" for Control
"~" for Option
"$" for Shift
"#" for numeric keypad

"\UF729" is the Home key
"\UF72B" is the End key
```

And here is a non-exhaustive list of actions I gleaned from [this post](http://support.multimarkdown.com/kb/composer-v4/custom-key-bindings-and-macros) (See the original post for an even longer list).

```
delete:
deleteBackward:
deleteBackwardByDecomposingPreviousCharacter:
deleteForward:
deleteToBeginningOfLine:
deleteToBeginningOfParagraph:
deleteToEndOfLine:
deleteToEndOfParagraph:
deleteToMark:
deleteWordBackward:
deleteWordForward:
indent:
insertTabIgnoringFieldEditor:
insertBacktab:
insertDoubleQuoteIgnoringSubstitution:
insertNewline:
insertNewlineIgnoringFieldEditor:
insertSingleQuoteIgnoringSubstitution:
insertTab:
insertText:
lowercaseWord:
moveBackward:
moveBackwardAndModifySelection:
moveDown:
moveDownAndModifySelection:
moveForward:
moveForwardAndModifySelection:
moveLeft:
moveLeftAndModifySelection:
moveParagraphBackwardAndModifySelection:
moveParagraphForwardAndModifySelection:
moveRight:
moveRightAndModifySelection:
moveSelectionToNextParagraph:
moveSelectionToPreviousParagraph:
moveToBeginningOfDocument:
moveToBeginningOfDocumentAndModifySelection:
moveToBeginningOfLine:
moveToBeginningOfLineAndModifySelection:
moveToBeginningOfParagraph:
moveToBeginningOfParagraphAndModifySelection:
moveToEndOfDocument:
moveToEndOfDocumentAndModifySelection:
moveToEndOfLineAndModifySelection:
moveToEndOfParagraph:
moveToEndOfParagraphAndModifySelection:
moveToLeftEndOfLine:
moveToLeftEndOfLineAndModifySelection:
moveToRightEndOfLine:
moveToRightEndOfLineAndModifySelection:
moveUp:
moveUpAndModifySelection:
moveWordBackward:
moveWordBackwardAndModifySelection:
moveWordForward:
moveWordForwardAndModifySelection:
moveWordLeft:
moveWordLeftAndModifySelection:
moveWordRight:
moveWordRightAndModifySelection:

etc...
```

## Taking It Further

As far as I understand `DefaultKeyBindings.dict` essentially allows you to send messages (a.k.a. call functions) on Cocoa objects running up the entire application hierarchy, stopping at the first one that responds. You can navigate text, use hidden Emacs like behaviour built in to Cocoa including key combinations with leaders, and generally create custom shortcuts and override default system behaviour system wide.

If you want to know more definitely checkout Jacob Rus' article linked above.

You can also checkout [Apple's own documentation](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/TextDefaultsBindings/TextDefaultsBindings.html) on the subject.

Happy hacking!

[Comments on Twitter](https://twitter.com/thope_xyz/status/1580237481353838592?s=20&t=CVkQUF1rbAhUerebNN0TEw)