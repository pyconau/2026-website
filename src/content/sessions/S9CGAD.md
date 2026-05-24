---
title: from where?!? import what?!?
code: S9CGAD
start: '2026-08-29T10:45:00+10:00'
end: '2026-08-29T11:15:00+10:00'
room: Ballroom 3
track:
type: talk
speakers:
- RJBY8Y
trackName: Main Conference
graphicsLayout: left
theme: accent_lemon
---

`import re`. `from pathlib import Path`. Python's import system is easy to take for granted, and most of the time we don't need to think about how the import statements we write actually work. Sometimes, however, things do go wrong, and knowing where to look for more information can mean the difference between scratching our heads in bafflement and quickly solving whatever problem we're facing.

For a lot of import related problems, the exception and associated traceback tell us everything we need to know to resolve the issue. Other problems can require a deeper investigation. Are we actually importing the module we think we're importing? Is the interpreter even looking in the right place for the modules we expect it to be loading? We've noticed our application is taking ages to start, where is all that time going?

Even without any third party components, the CPython core interpreter and standard library offer a range of utilities to learn more about how the import system has been configured, and exactly what it is doing at runtime. This talk will cover several of these tips and tricks for investigating import system misbehaviour from one of the people that wrote it.
