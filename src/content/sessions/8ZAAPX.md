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
abstract: "25,000+ resources, 65,000+ lines of Python, two engineers.\r\n\r\nFive
  years ago we made a commitment to automating (almost) everything we could about
  our platform. Deployments, Guardrails, Observability, Identity, and everything between.\r\
  \nSo far we have been seeing that through with extensive use of Infrastructure as
  Software.\r\n\r\nFive years later, I have regrets.\r\n\r\nSolving complex problems
  with Infrastructure as Software is a great way to create complex problems with Infrastructure
  as Software."
sponsor: x-rd
---

x-RD's platform secd3v hosts isolated services for customers. Every tenant is encapsulated within it's own AWS account. We heavilty use Pulumi to manage nearly every aspect of this environment, our internal environments, and the stacks we use for development. This automation is powered from a shared Python codebase; skywater (so named for the 1964 cloud-seeding projects).

Building this level of automation is not exactly simple, and we've made and re-made lots of decisions along the way.

We will broadly discuss some context around Infrastructure and Software and x-RD's approach to building a model that maps to our environment. Then we will examine major challenges we faced and the decisions they forced from the early days of development through to running the platform in the present.

The juicy technical content of this talk includes:

- Building an async attribute resolution engine to support circular dependencies between Python objects
- Using cooperative inheritance to incrementally refactor a codebase under active development
