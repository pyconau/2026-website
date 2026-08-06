---
title: Why Your ML Pipeline Needs an Agent (and How to Build One
code: J7NSZH
start: '2026-08-27T12:05:00+10:00'
end: '2026-08-27T12:35:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- R3GBVU
- TPLK9Y
trackName: Data & AI
abstract: 'Every ML team knows the pain: the majority of practitioner time goes into
  data wrangling, pipeline plumbing, and environment configuration — not solving business
  problems. Getting a pandas prototype into production still takes months, and that’s
  before you factor in monitoring, drift, and retraining. Agentic ML offers a fundamentally
  different approach: AI agents that understand your data context, reason about which
  steps to take, and execute ML workflow stages autonomously — while keeping humans
  in the loop for strategic decisions. In this talk, we explore why Agentic ML is
  a paradigm shift beyond AutoML, what makes context-aware agents effective, and how
  these ideas connect to Python workflows in practice. We’ll walk through real patterns
  for feature engineering, distributed training, and model monitoring — with honest
  lessons about where agents shine and where they still fall short. You’ll leave with
  a practical framework for thinking about agent-assisted ML in your own stack.'
sponsor: snowflake
---

ML practitioners still spend most of their time on data preparation and pipeline plumbing rather than modeling. Agentic ML offers a different response: agents that operate in a continuous observe-reason-execute-evaluate loop with deep awareness of your data context — unlike AutoML (no reasoning) or code-generation chatbots (no execution).

In this session, we cover:

- What Agentic ML is — a precise definition centred on the iterative reasoning loop and data context awareness
- Two production patterns — notebook-to-production conversion and safe model rollout with traffic splitting and drift monitoring
- Where agents fail — three concrete failure modes with practical guardrails

Attendees will leave with a framework for where agents add value, where human judgment remains essential, and how to introduce agent-assisted workflows into their Python ML stacks
