---
title: Breaking the PR Review Bottleneck
code: QUZ9TS
start: '2026-08-28T13:25:00+10:00'
end: '2026-08-28T13:55:00+10:00'
room: Ballroom 2
track:
type: talk
speakers:
- 8SQRFW
trackName: Main Conference
graphicsLayout: right
theme: stone_emerald
---

Pull request reviews are often the single biggest bottleneck in software delivery. What takes minutes to write can sit for days waiting for review, killing velocity and frustrating teams.

This talk explores why PR queues stall, what we can learn from massive open source projects that have solved this at scale, and the practical techniques, from automation with Python tooling to team process shifts, that can dramatically reduce your time to merge.

Speed isn't about writing code faster, it's about removing waiting.

Most teams above a handful of developers know the pain: PRs sitting unreviewed, nitpick storms burying real issues, architectural debates erupting after a week of implementation. These aren't edge cases, they're the default. And if your team is adopting AI coding tools, this bottleneck is about to get worse.

This session starts with the patterns that cause PR queues to stall, you'll recognise most of them immediately. Then we'll look at how projects like Kubernetes and Chromium coordinate thousands of contributors without drowning, and translate those strategies into techniques that work for everyday teams: design alignment before code, automated quality gates using Python-ecosystem tools like Ruff, mypy, and pre-commit, process changes that make queue health visible, and practical approaches to reviewing AI-generated code.

The talk closes with a prioritised starting point, three changes that need no tooling budget and can ship this sprint.
