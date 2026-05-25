---
title: Can I Trust You? Service-to-Service Identity with SPIFFE
code: KFJLUE
start: '2026-08-28T11:20:00+10:00'
end: '2026-08-28T11:50:00+10:00'
room: Ballroom 3
track: cybersecurity
type: talk
speakers:
- PAU3DM
layout: layout_2
trackName: Cybersecurity
abstract: "Sam built a great gateway. Users are authenticated, requests are validated,
  the front door is solid. Inside the cluster, services trust each other — because
  they're inside the cluster.\r\n\r\nThen Omen shows up.\r\n\r\nThis talk follows
  Sam the SRE through a nightly battle against Omen the Evil Hacker — and how SPIFFE
  and SPIRE finally give every Python service a cryptographic identity it can prove,
  not just claim."
---

We've all built Castle walls. A solid perimeter and user authentication at the gateway, and then implicit trust everywhere inside — because it's inside the walls, right? Only legitimate traffic gets in.
But "inside the walls" is not an identity. Any service can walk up to any other and say "hey, it's me." And the other service believes it. Because why wouldn't it?

This talk follows Sam the SRE and Omen the Evil Hacker who keeps ruining Sam's sleep. Sam gets woken up by alerts of services doing things they shouldn't — the Order Service telling the Dispatch Service to ship packages without charging the customer. Sam finds the problem and fixes it. Omen finds another way in.

We will journey through the nightly battle between Sam and Omen, as Sam works through the natural progression of service identity solutions — from implicit network trust, through API keys and shared secrets, to mTLS — each time discovering a new gap that Omen is happy to exploit. Until Sam finally arrives at SPIFFE.

Along the way we'll look at the Python ecosystem for working with SPIFFE and SPIRE — using py-spiffe (spiffe and spiffe-tls packages) and the Workload API, wiring mTLS into httpx, and using SVIDs for services that need to reach beyond the cluster boundary.

Level: Intermediate — familiarity with HTTP services and basic TLS concepts will help, but isn't required.

You'll leave with a clear mental model of workload identity, a high-level understanding of how SPIFFE/SPIRE closes the gaps that other approach leaves open, and patterns you can take straight back to your Python services.

Omen doesn't stand a chance.
