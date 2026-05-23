---
title: 'Stop Prompting, Start Composing: Agent Skills in Practice'
code: 7KE7PU
start: '2026-08-27T14:35:00+10:00'
end: '2026-08-27T15:05:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- TX8ES3
trackName: Data & AI
---

AI agents are changing how we build software. They have augmented our software engineering workflow and challenged us to practice a new discipline, Agentic Engineering. Central to this emerging discipline is the skill, a natural language markdown file that bundles workflows, tools, and domain knowledge into a new unit of work for defining what an agent can do. Adopted as an open standard across the industry, skills sit above programming languages, not within them. If you've ever written a runbook, a playbook, or an SOP, you already understand what a skill encodes. This talk explores what a skill is, how skills compose through context rather than interfaces, and what breaks when your smallest unit of work is no longer deterministic. It is drawn from real experience building an enterprise architect agent, with practical examples in Python.

We've spent decades perfecting abstractions for code such as functions, classes, modules, services. Each one helped us manage complexity at increasing levels of codebase and team size. But AI agents have bent this model by introducing a new opportunity using natural language.

Enter the skill: a natural language markdown file that bundles templates, domain references and tools into a composable unit of capability. Like a function, a skill prescribes a path, it has triggers, workflows, steps, and guardrails. But unlike a function, the execution within that path is non-deterministic. The agent decides how to fulfil each step, which tools to reach for, and when to adapt its approach based on what it finds. A skill defines the "what" and the "constraints". The agent determines the "how" within those constraints. We seek to provide our agent with structured autonomy. 

Skills are language-agnostic. They can invoke python scripts, shell commands or anything else the agent has access to. The abstraction lives above programming languages, not within them.

This talk explores using skills as a first-class abstraction in your agentic engineering practice. Drawing from real-world experience building an architect agent to navigate enterprise processes, I'll show what a skill looks like, how skills compose, and what changes when your smallest unit of work is no longer deterministic. I'll also be honest about the challenges of managing regressions, evaluations, and failure modes that surface within a non-deterministic world.

If you're a developer seeking to enhance your Agentic Engineering practice, this talk may give you a new insights to further enhance your practice.
