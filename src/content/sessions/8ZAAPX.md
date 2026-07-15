---
title: Automation First, Regrets Later
code: 8ZAAPX
start: '2026-08-27T11:30:00+10:00'
end: '2026-08-27T12:00:00+10:00'
room: Ballroom 1
track: platform-engineering
type: talk
speakers:
- JHR9FX
trackName: Platform Engineering
abstract: "25,000+ resources across deployments, 65,000+ lines of Python, a team of
  two.\r\n\r\nYou've built a platform to deploy things, offer services, and power
  your business.\r\nBut how do you manage the platform itself? Can you make the boring
  parts truly\r\nset-and-forget: patch management, progressive rollout, compliance?
  At some\r\npoint you think you need a platform for your platform, and then you realise
  you\r\nalready have one.\r\n\r\nThis talk is the story of developing x-RD's infrastructure
  automation codebase\r\n(codenamed skywater) that runs the platform for our flagship
  product (secd3v),\r\ninternal projects, and internal infrastructure, including the
  development and CI\r\nenvironments that skywater itself is built in. It's also the
  story of the hair-pulling\r\ncomplexities we built ourselves into and had to build
  ourselves out of."
sponsor: x-rd
tags:
- not-yet-announced
---

x-RD's secd3v product hosts isolated services for customer use, such as GitLab,
GitLab Runners, and AI services including Claude Code Service and MCP tooling.
Deployed on AWS using the skywater automation codebase, which is built with
Pulumi and, of course, Python.

Pulumi was chosen specifically because it meant writing real Python, not HCL or
YAML. Early prototyping showed that problems like orchestrating cross-account
AWS resources with complex dependencies were more naturally solved in a
general-purpose language, and the dependency management would only grow
more complex from there.

From the start, infrastructure was treated as software with a commitment to an
automation-first approach. The scope goes well beyond production infrastructure:
compliance guardrails, observability, networking, and the CI and development
environments used to build skywater are all part of what it manages. This talk
explains what that philosophy looks like in practice, and why 25,000+ managed
resources isn't a sign of sprawl, but the natural result.

That investment paid off: the team handling skywater development and
operations across all environments is a permanent team of two. The platform is
used to maintain itself, with other engineers brought on as needed to support
bursts in development related to the platform, products built on top of it, and
customer support.

But early assumptions didn't survive growth. The monolithic stack that worked at
first eventually hit a wall, and had to be migrated incrementally to a modular
architecture. This talk digs into the specific problems that had to be solved: how do
you split a live Pulumi stack without reprovisioning thousands of resources? How
do you refactor a class hierarchy that production depends on? The solutions
involved moving resources between stacks at the state level while refactoring in
backward-compatible ways, and using cooperative inheritance (Python's method
resolution order used to bridge old and new class hierarchies) to refactor
incrementally while production kept running.

If starting from scratch today, the team would do things differently: architecting for
modular stacks from the start rather than unwinding tight coupling later, and
adopting well-known software patterns like dependency injection sooner, before
the codebase accumulated complex internal machinery that is now being
replaced with cleaner approaches. Moving fast enabled delivery, but it also left
behind decisions that are still being unwound.

Through real code examples and architecture decisions traced across a five-year
timeline, the audience will walk away with patterns and lessons applicable to any
team managing infrastructure as code, whether at this scale or just starting out.

The core message: automation-first compounds over time, for better and for worse.
