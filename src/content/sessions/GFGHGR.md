---
title: 'Vibing Vision: how we built a pose tracking art installation in two weeks'
code: GFGHGR
start:
end:
room: ''
track: data-and-ai
type: talk
speakers:
- WUPRPT
trackName: Data & AI
abstract: "Can you use AI to vibe-code a computer vision pipeline? Yes... sort of.\r\
  \n\r\nIn December 2025, a group of friends built an art installation for Lost Paradise
  music festival. We built the bulk of the project in two weeks, after work hours,
  during late night hackathons in someone's living room. There is no way we would
  have been able to do this without Claude Code. That being said, computer vision
  is an interesting case such that most of the debugging happens when you press play
  and run the system live - and AI tools can't sit and watch video streams in the
  same way a human can. It is difficult to describe with words the exact results you're
  looking for in the output, in a way that Claude can meaningfully understand and
  act on. As a result, we came up with clever ways to share our outputs and problems
  with Claude, and learned a lot about its capabilities and limits in image processing
  and computer vision tasks. \r\n\r\nThis talk will take you through the process -
  from running pose tracking models on AI cameras, using OpenCV for camera calibration,
  iterating on DepthAI pipelines, creating real-time data visualisations to track
  keypoints, and what we learned about the limits of generative AI models when debugging
  real-world systems."
---

This talk will cover the following topics
- The art installation we built, the premise of it, the real-world constraints 
- The tech stack: DepthAI pipelines and YOLO pose tracking running on OAK-D (OpenCV AI Kit with Depth)
- What Claude did well: visualisations, quick code iterations, testing scripts, consolidating notes into a project whitepaper, allowed us to build a very complex, working system in two weeks of after-hours work rather than several months of full-time work 
- What Claude struggled with: visual reasoning, computer vision concepts, reasoning about how real-world constraints like physical environment and human behaviour impact system performance
- Workarounds we developed to get enormous benefit from working with Claude despite all of the above
- Advice for people who want to use AI to build projects that involve real-world systems - you absolutely can do it, but it will take some extra consideration and careful communication - AI assistants don't experience and reason about the world in the same way we do!
