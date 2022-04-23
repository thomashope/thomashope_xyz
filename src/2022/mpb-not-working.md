title: Fixing MaterialPropertyBlocks on static objects in Unity
description: If your MaterialPropertyBlock aren't working in Unity, disable static batching
image: /2022/mpb-not-working/static-menu.png

# `MaterialPropertyBlock`s and Static Batching

Or, how I wasted 2 days wondering why my `MaterialPropertyBlock`s weren't working only to discover the fix was to disable Static Batching by unchecking a single checkbox.

NB: Written for Unity 2020.3 using the Universal Render Pipeline

## Why No Work? 😭

[Static Batching](https://docs.unity3d.com/2020.3/Documentation/Manual/static-batching.html) is where Unity automatically combines multiple meshes into a single mesh behind the scenes, and renders them all at once. This is sometimes faster, but requires them to all be rendered with the same properties.

`MaterialPropertyBlock`s are a way of supplying different material properties per object, e.g. a different colour, without having to create a unique material each time.

Or to put it another way. `MaterialPropertyBlock`s are an optimisation for supplying **different properties to each object**. Static Batching is an optimisation for rendering multiple objects **with the same properties**.

Do you see how these two approaches are not compatible?

Unity actually give the following hint, but until today I didn't understand what it meant and my eyes just glossed over it.

![Picture of warning text on mesh renderer when you have an instanced material. The warning Reads "This Renderer uses static batching and instanced Shaders. When the Player is active, instancing is disable. If you want instanced Shaders at run time, disable static batching."](/2022/mpb-not-working/warning.png)

One thing that added to my confusion was that the `MaterialPropertBlock`s appeared to be applied correctly by our Edit Mode tools, it was only when entering play mode that the Static Batching kicked in and the issue became visible.

My inability to read what is infront of my eyes, plus a lack of understanding of Unity's rendering terminology is why I am here, 2 days later, kicking myself, writing this blog post.

## How Fix? 👷

If you want to apply a `MaterialPropertyBlock` to an object, you must make sure it does not have Static Batching enabled.

You can change an object's static flags from the inspector or from code.

### Disable Static Batching from the Inspector

Click the arrow next to the word Static to reveal all the different *types* of static. Here you can choose which types you do and don't want individually. In my case I want everything except Batching Static.

![Screenshot of Static drop down in inspector with Static Batching is disabled](/2022/mpb-not-working/static-menu.png)

### Disable Static Batching from code

```csharp
// Setup your static flags, in my case everything except BatchingStatic

var staticFlags = ~StaticEditorFlags.BatchingStatic;

foreach (var go in myGameObjects)
{
	// Apply your static flags to each game object

    GameObjectUtility.SetStaticEditorFlags(go, staticFlags);
}
```

### Alternative Ways To Disable Static Batching

* [At the Shader Level](https://docs.unity3d.com/2020.3/Documentation/Manual/static-batching.html#:~:text=The%20Mesh%20Renderer,set%20to%20true.): Apparently you can also disable static batching at a shader level by supplying the DisableBatching keyword but I haven't figured out how yet.
* [Static Batching at Build Time](https://docs.unity3d.com/2020.3/Documentation/Manual/static-batching.html#:~:text=see%20Performance%20implications.-,Static%20batching%20at%20build%20time,-You%20can%20enable): If you want to disable the static batching that happens at build time, uncheck the checkbox at *Project Settings > Player > Other Settings > Static Batching*.

If you want to learn more about how both static and dynamic batching work, and how and when to use them, [read the docs](https://docs.unity3d.com/Manual/DrawCallBatching.html).

## Other Trivia

If you know what instanced rendering is, you may be wondering if `MaterialPropertyBlock`s are related to that. The answer is yes, they are related. However although `MaterialPropertyBlock`s are compatible with instancing, instancing is disabled by default and has to be explicitly enabled per material.

![Screenshot of Enable GPU Instancing checkbox in the material inspector](/2022/mpb-not-working/enable-gpu-instancing.png)

AFAIK, if you are using `MaterialPropertyBlock`s you almost certainly want to Enable GPU Instancing, in addition to disabling Static Batching.

And with that, happy coding!