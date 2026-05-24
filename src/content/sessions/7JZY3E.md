---
title: 'Kubernetes as LEGO: Building Platforms one block at a time'
code: 7JZY3E
start: '2026-08-27T10:45:00+10:00'
end: '2026-08-27T11:15:00+10:00'
room: Ballroom 1
track: platform-engineering
type: talk
speakers:
- WGSFFL
trackName: Platform Engineering
graphicsLayout: left
theme: accent_coral
---

Have you ever wondered what it actually takes to deploy your Python/Django or any application to Kubernetes - and build a platform around it? Or if you already have one, whether you'd build it the same way in 2026?
This talk introduces Kubernetes as LEGO: building a real platform one block at a time, starting from raw primitives, layering Helm and Kustomize where they genuinely earn their place, and finally writing a custom operator in plain Python using kopf.
At each step, we ask: Does this next block solve a real problem, or create a new one? You'll leave with a composable mental model and a sharper instinct for when to stop.

Platform engineering has a complexity problem. The default playbook - install everything, abstract it all away - produces platforms that are expensive to operate and painful to debug. This talk is for Python developers who are Kubernetes-curious but find the ecosystem overwhelming, and for engineers already using Kubernetes to visually reflect on and revisit their experience with it.

The talk progresses through three levels, each justified by what the previous one couldn't handle:

–	Level 1 - Raw primitives: Pods, Deployments, Services, ConfigMaps. A grounded walkthrough of what plain Kubernetes already gives you - and how far a Django application gets before any extra tooling is needed.
–	Level 2 - Helm and Kustomize: Helm for consuming and distributing packages; Kustomize for environment overlays of the apps you own. Where each shines, where they create friction when combined, and the hybrid pattern the industry has converged on.
–	Level 3 - Python operators with kopf: when the built-in API can't express your domain logic, Custom Resource Definitions (CRDs) let you extend it. kopf maps Kubernetes event handlers to Python decorators - making operator development immediately legible to any Python developer, no Go required.

The through-line is a single question asked at every layer: what problem does this solve that the previous level couldn't? That question is the decision framework attendees take home. No prior Kubernetes experience assumed; familiarity with Python or Django is helpful.
