title: Implementing `OnDestroyInEditor()` in Unity
description: How to call a function when an object is destroyed in edit mode.

# Implementing `OnDestroyInEditor()` in Unity

While developing level editing tools in Unity I found myself wanting to call a function if the user deleted an object from the Scene View while in Edit mode.

## Use Case

Specifically, I had list of FloorNode objects referencing each other in a loop, each with an attached FloorNodeScript with the `[ExecuteAlways]` attribute. The user could drag around the floor nodes which defined the edges of a polygonal floor mesh generated in real time.

I had working code that allowed creating new nodes and deleting existing nodes, fixing up the references as it did so. However if the user selected a node in the editor and pressed the delete key those functions would not be called, and the loop of node references would become broken.

## Failed Attempt

The first attempt to fix this issue was to use `if(Application.isEditor)` inside `OnDestroy()` and call the appropriate function, `JoinNeighbours()`, to fix up the references. Unfortunately I later realised that `OnDestroy()` was also being called while entering and exiting play mode, due to the `[ExecuteAlways]` attribute, which meant `JoinNeighbours()` was being called inappropriately, causing issues with seralization.

## Current Solution

*FloorNodeScript.cs*:

```csharp
void OnDestroy()
{
    if (Application.isEditor
    	&& !EditorApplication.isPlayingOrWillChangePlaymode
    	&& !EditorState.exitingPlayMode)
    {
        OnDestroyInEditor();
    }
}

void OnDestroyInEditor()
{
    // code that should only be called in edit mode!
}
```

*EditorState.cs*:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEditor;

[InitializeOnLoad]
public static class EditorState
{
    static public bool exitingPlayMode;

    static EditorState()
    {
        EditorApplication.playModeStateChanged += PlayModeStateChanged;
    }

    private static void PlayModeStateChanged(PlayModeStateChange state)
    {
        exitingPlayMode = state == PlayModeStateChange.ExitingPlayMode;
    }
}
```

`EditorApplication.isPlayingOrWillChangePlaymode` is true if the application is in play mode, or critically, if it is about to enter play mode. This check is what prevents `OnDestroyInEditor()` from being called when pressing play from inside the editor.

Similarly `EditorState.exitingPlayMode` prevents `OnDestroyInEditor()` from being called when exiting play mode. For more info on how that's implemented check out the docs page for [`EditorApplication.playModeStateChanged`](https://docs.unity3d.com/ScriptReference/EditorApplication-playModeStateChanged.html)

Hope that helps!