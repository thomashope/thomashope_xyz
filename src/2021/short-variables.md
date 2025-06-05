title: Short Variable Names
description: A defence of i, j, it, et al.
date: 2021-05-14
published: true
featured: true

# Short Variable Names

We say, short variable names are bad, they are not meaningful.

We are hypocrites.

```
for(int i = 0; i < size; ++i) {
	array[i] = ...
}
```

Perhaps the advice is too simple. What are the exceptions?

It's about context. In the context of a `for` loop `i` is meaningful. We all know what it means.

Short variable names can be good.

Short variable names get out of your way, they allow you to focus on the code.

Internalise a short variable name and it becomes a symbol, then you never have to read it again.

But before you go short, check the context.

Provide context with a descriptive function name. Lay out the algorithm so it is easily recognised. Reference the paper who's solution you are implementing. Keep code short and to the point.

The codebase can also be it's own context. Use the same short name consistently so the reader can learn it once.

(If you like, you can even assign a variable a shorter name when the context changes.)

It's about judgement.