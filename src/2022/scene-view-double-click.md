title: Custom Selection in Unity Scene View
description: Track the click count on mouse down, but do selection on mouse up
date: 2022-05-18
published: true
featured: true

# Double Click Selection in the Scene View

One of the designers requested that double clicking on an object in the scene view would select all objects in the same group.

$$AUTOPLAY_VIDEO(/2022/scene-view-double-click/double-click.webm)$$

A good idea that in the end didn't require much code to implement, but it did require a little hunting around to find an acceptable solution.

## How to Do Custom Selection

For those who don't know, selection behaviour in the vast majority of situations happens on *mouse up*, not mouse down. I wanted to keep this feature consistent with that expected behaviour. Also, if you try modifying the selection on mouse down, it will get overridden by the default selection behaviour on the following mouse up anyway.

Mouse events in Unity have an integer [`clickCount`](https://docs.unity3d.com/ScriptReference/Event-clickCount.html) field which tells you if it's part of a single or double click. Unfortunately the `clickCount` is only used on mouse down events, not mouse up.

The solution I found was to track the `clickCount` of the previous mouse down event, then modify the selection on the next mouse up and consume the event inside `SceneView.beforeSceneGui`, preventing it from being passed further along and doing Unity's default selection behaviour.

The example code below shows a simple script that makes double clicking select all objects with that script attached. Note the `[ExecuteAlways]` attribute at the top.

The version we actually use in The Game has a single root object with an instance of the double click script, which then behaves differently based on the object clicked on. In theory this is slightly more efficient than having this same script checking mouse events on 100s objects but hopefully this simple example demonstrates what's going on and you can adapt it to your needs.

Anyway, that's all from me today. As always, happy coding :)

```csharp
[ExecuteAlways]
public class DoubleClickSelectionScript : MonoBehaviour
{
    int lastMouseDownClickCount;

    private void OnEnable()
    {
        SceneView.beforeSceneGui += BeforeSceneGui;
    }

    private void OnDisable()
    {
        SceneView.beforeSceneGui -= BeforeSceneGui;
    }

    void BeforeSceneGui(SceneView scene)
    {
        Event e = Event.current;

        if(e.type == EventType.MouseDown)
        {
            lastMouseDownClickCount = e.clickCount;
            if(lastMouseDownClickCount == 2 && HandleUtility.PickGameObject(e.mousePosition, false) == gameObject)
            {
                e.Use();
            }
        }

        if(e.type == EventType.MouseUp && e.button == 0 && lastMouseDownClickCount == 2)
        {
            var picked = HandleUtility.PickGameObject(e.mousePosition, false);
            if(picked && picked.GetComponent<DoubleClickSelectionScript>())
            {
                var cubes = FindObjectsOfType<DoubleClickSelectionScript>();                

                var gs = new GameObject[cubes.Length];
                for (int i = 0; i < gs.Length; ++i)
                    gs[i] = cubes[i].gameObject;

                Selection.objects = gs;

                e.Use();
            }
        }
    }
}
```