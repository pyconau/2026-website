---
title: 'Goodbye GIL: Exploring the Free-threaded mode in Python'
code: RQ7STH
start: '2026-08-27T14:35:00+10:00'
end: '2026-08-27T15:05:00+10:00'
room: Ballroom 2
track:
type: talk
speakers:
- GMGTSH
trackName: Main Conference
graphicsLayout: left
theme: accent_violet
---

Python 3.13 was the first Python version released with a free-threaded mode. Although the default interpreter still utilizes the GIL, it provides provisions that enable us to run a free-threaded version of the interpreter with the GIL disabled. 

Through this talk, we’ll set up and run the free-threaded interpreter, benchmarking it against the GIL-enabled version for various tasks. We'll assess the impact on single-threaded vs multithreaded code and test the performance across CPU-bound and I/O-bound tasks, aiming to identify scenarios where free-threaded Python excels.

For decades, the Global Interpreter Lock (GIL) has been one of Python’s most debated design choices. It simplified memory management while limiting true parallelism. With Python 3.13, that story begins to change.

This talk explores Python’s new free-threaded mode, introduced through PEP 703, which allows running the interpreter without the GIL. We will explore how to enable it, how it behaves, and where it makes a real difference.

We’ll start with a quick look at the history of the GIL and why removing it has been so challenging. From there, we’ll unpack the key ideas behind PEP 703 and the criteria outlined in PEP 779 that guide its path toward becoming a fully supported feature.

The core of the session focuses on hands-on experimentation. We’ll set up and run the free-threaded interpreter, compare it directly with the traditional GIL-enabled version, and benchmark performance across different workloads. This includes CPU-bound and I/O-bound tasks, as well as understanding the trade-offs (especially the impact on single-threaded performance).

By the end, you’ll have a clear understanding of where free-threaded Python stands today, when it provides meaningful benefits, and how it might reshape the way Python applications are designed in the near future.
