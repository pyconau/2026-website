---
title: "Please Don't Put That in a Dict: Better Data Models in Python"
code: TYXRSM
start: '2026-08-27T14:05:00+10:00'
end: '2026-08-27T14:35:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- 8SBWWP
trackName: Data & AI
abstract: "Dictionaries are one of the first tools Python developers reach for: fast,
  flexible, and easy to use when building something new. But when do they stop being
  enough? And when it's easy to generate dataclasses and classes, how do you know
  if that structure is actually useful?"
---

I used to reach for dictionaries for everything. New feature? Dict. API response? Dict. LLM call? Dict.

At some point, they started showing up everywhere and I stopped being able to hold the shape of my data in my head. Nothing was obviously broken, but everything felt harder to reason about.

That feeling crystallised when I was building a data pipeline that consumed several third-party APIs. Every response came in as a dict, got merged with other dicts, passed through a few functions, and eventually turned into... more dicts. It worked fine until I needed to change a field name upstream and spent an afternoon tracing where that key was used across the codebase.

Around the same time, it became incredibly easy to use AI to generate more structured code: dataclasses, classes, whatever I wanted. But I realised I didn't actually know when that structure was useful, and when it was just adding noise. 

In this talk, I'll walk through how I learned to tell the difference. We'll start with simple dictionaries and follow how code evolves as data becomes more stable and meaningful. We'll introduce TypedDict, dataclasses, and classes along the way. I'll show what improved at each step, what didn't, and where each approach breaks down.

If you've ever felt like your code works but is getting harder to reason about, or you're not sure when to introduce more structure, this talk will give you a clearer way to think about it.
