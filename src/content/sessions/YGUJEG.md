---
title: 'From Pixels to Points: Inferring Archery Scores with Computer Vision'
code: YGUJEG
start: '2026-08-27T12:30:00+10:00'
end: '2026-08-27T13:00:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- SNSDVY
trackName: Data & AI
---

Improving in archery often goes beyond simply increasing your score; it also means building consistency, tightening groupings, and recognising patterns such as shots drifting off-centre.  However, tracking the final position of arrows after each shot is a slow, imprecise, and awkward process. 

In this talk, I show how I trained and validated a computer vision pipeline using oriented object detection to infer arrow locations and scores directly from a target image. By deploying this system on a Raspberry Pi, the process becomes simple enough to use during regular practice, while also creating a record of shot placement that can be analysed over time. This makes it possible to look beyond individual scores and start tracking broader patterns in accuracy and consistency.

This talk goes beyond just detecting objects in an image: I cover the realities of hand annotating hundreds of training images, transforming model predictions into calibrated target co-ordinates, inferring scores from geometry, wrangling with validation, and making the whole thing usable in the field. 

It is aimed at a broad audience and assumes no prior knowledge of computer vision or object detection. While I touch on concepts such as coordinate transformations and validation, the focus is on practical understanding rather than detailed mathematical implementations. The goal is to give a clear picture of what it actually takes to build and deploy a real-world model. Plus, archery is an inherently cool activity that everyone should enjoy.
