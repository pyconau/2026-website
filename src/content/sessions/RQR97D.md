---
title: 'Vibe-Check Your Vibe Code: Surviving the Era of Agentic Open Source Dependencies'
code: RQR97D
start: '2026-08-28T13:25:00+10:00'
end: '2026-08-28T13:55:00+10:00'
room: Ballroom 3
track: cybersecurity
type: talk
speakers:
- 3US9G9
- TJVGUM
layout: layout_2
trackName: Cybersecurity
abstract: "In the good ol' days, we worried about individual maintainers becoming
  overburdened, or ripple effects from surprise deletions in dependency graphs. Now,
  with the power of AI, we get to worry about these things on a much bigger scale:
  on repeat, across entire ecosystems!\r\n\r\nAs AI agents outpace humans in code
  output, we’re entering a delightful time where vibe-coded pull requests are checked
  in because they \"look right,\" even if they’ve silently re-introduced classes of
  security vulnerabilities we thought we'd eliminated.\r\n\r\nIn this talk, we’ll
  look at some delicious data from [suggested redaction during CFP review of the dataset]
  to see just how big the problem is (so far). We’ll explore AI slopsquatting, DDOSing
  maintainers through vulnerability reports (valid or superfluous), and whether \"\
  living at HEAD\" (with its security risks) might be our best security strategy.\r\
  \n\r\nWe’ll also talk: private forks, dynamic cooldowns, and whether or not that
  one legend in Nebraska has already left the chat. Come for the existential dread;
  stay for the practical tips on not letting your dependency graph become (more of)
  a dumpster fire."
---

We are seeing a massive shift in how code is produced and reviewed, and the scale that this is happening at. While having "eyes on the code" forms the foundation of open-source security, a significant portion of those eyes are now LLMs. ("AIs on the code", anyone? 🫠) 

This talk will cover:

- How models trained to generate code, or to prioritise passing tests (or just delete tests) are re-introducing classic vulnerability classes into modern stacks.
- How AI-generated vulnerability submissions are drowning maintainers in noise, leading to burnout and abandoned projects.
- Stats on how many critical dependencies are potentially abandoned, so that when vulns are found, they won’t be remediated.

We’ll wrap up with a slightly-hopeful practical call to action. We'll discuss why dynamic cooldown periods are your new best friend, how to use tools (both AI and not) to improve your security posture, and how to join the OSSF Malicious Package and other efforts to help hold back (or shine a light on) the tide.
