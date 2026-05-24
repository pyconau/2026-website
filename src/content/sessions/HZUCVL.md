---
title: The Virtues of Being Lazy
code: HZUCVL
start: '2026-08-29T14:00:00+10:00'
end: '2026-08-29T14:30:00+10:00'
room: Ballroom 1
track:
type: talk
speakers:
- WD9KCJ
trackName: Main Conference
graphicsLayout: right
theme: charcoal
---

Title: The Virtues of Being Lazy
Sub title: The virtue of being a lazy programmer, understanding lazy evaluation, and understanding lazy imports (3.15)

-------------------------------
Abstract:
Your boss wants your program to "run faster". But performance can be a tricky thing.
Sometimes we can make a choice of _when_ the program will be slow.
This talk will explore the "virtue" of laziness with regards to programmer approach, and lazy evaluation (with generators and `yield`).
But mainly the talk will focus on the new 3.15 keyword `lazy` and how it can affect module loading times.

This talk will cover briefly the role of "laziness" in being a programmer. I will then examine the role of laziness in evaluation (generators and `yield`). That will lead us to laziness in imports.

The main focus of this talk will be on lazy (on-demand) imports and the new `lazy` keyword in 3.15, and how that can significantly improve your program's start up speed, and lower memory consumption. I will cover detail about the new feature, and how to control whether an import is lazy or eager. Also covering some new terminology, including lazy, eager, elide and reification. Some alternative approaches will also be considered.

Particularly if you have a CLI program that has different behaviours based on switches, this can make a big difference.

Lazy imports are an accepted new feature in 3.15 (final due October 2026), and I will be live demonstrating with pre-release Python.
