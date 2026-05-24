---
title: Things I don’t worry about as NumPy does them for me
code: A3XLCE
start: '2026-08-29T11:20:00+10:00'
end: '2026-08-29T11:50:00+10:00'
room: Ballroom 2
track: research-software-engineering
type: talk
speakers:
- EQJWS9
trackName: Research Software Engineering
graphicsLayout: right
theme: accent_violet
---

I regularly enjoy performance that I absolutely did not earn. That’s because NumPy quietly handles an alarming number of hard problems on my behalf. In this talk, we’ll pop the hood on NumPy and look at what it’s actually doing to make Python fast. We’ll even glance at the source code, gently, and without expecting anyone to be an expert in C. 

This isn’t a talk about becoming a NumPy wizard or writing “clever” code. It’s about building a better mental model of what NumPy already does for us, so we can stop accidentally getting in its way and continue taking credit for performance we mostly didn’t implement ourselves.

Python is slow. We all know it. And yet, here we are, running numerical workloads that would make a C programmer nod approvingly. How? NumPy. But not *magic*. NumPy deliberate, well-engineered  NumPy.

In this talk I'll walk through the handful of core ideas that explain most of NumPy's performance. The goal isn't a how-to guide  it's a mental model. One that I think will change how you write numerical Python.

We'll start by watching Python loops disappear. When you write `a ** 2`, no Python interpreter is crawling over your million elements  a pre-compiled C kernel is. NumPy isn't accelerating Python; it's relocating the work somewhere Python never touches. Once you see it that way, a lot of things click into place.

From there, we'll get into the `ndarray` itself. I'll show you the C struct underneath every array  the data pointer, shape, strides, and dtype fields that make it tick. Once you understand strides, you'll realise that transposing a massive array, reshaping it, or slicing it doesn't copy a single byte. NumPy is
pulling a surprisingly elegant trick, and once you see it, you can't unsee it.

Next up: broadcasting and cache-friendly execution. Broadcasting isn't just a convenience  it's a way to express complex operations without materialising large intermediate arrays. And when you combine it with contiguous memory access, your loops stay tight, your cache stays warm, and NumPy can quietly hand things off to SIMD and BLAS without you lifting a finger.

To tie it all together, we'll optimise a game of Minesweeper. Using stride tricks, convolution, and vectorised Monte Carlo sampling, we'll turn a nest of Python loops into clean, fast NumPy code, and I'll show you exactly how each concept from the talk contributes.

If you use NumPy regularly and have ever wondered *why* it's fast rather than just *that* it's fast, this talk is for you. You'll leave with a practical mental model that makes you a better NumPy programmer  without having to worry about any of the details NumPy is already handling for you.
