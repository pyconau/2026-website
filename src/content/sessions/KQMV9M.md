---
title: Your Python container is 90% stuff you didn't ask for
code: KQMV9M
start: '2026-08-27T12:40:00+10:00'
end: '2026-08-27T13:10:00+10:00'
room: Ballroom 2
track:
type: talk
speakers:
- XXBN8R
trackName: Main Conference
abstract: 'Docker pull python:3.x feels like you asked for Python. What you actually
  got was ~430 packages: a shell, two package managers, a C compiler, and a few hundred
  known CVEs - an entire distro userland your app will never use, but an attacker
  with RCE absolutely will.'
sponsor: chainguard
---

Docker pull python:3.x feels like you asked for Python. What you actually got was ~430 packages: a shell, two package managers, a C compiler, and a few hundred known CVEs - an entire distro userland your app will never use, but an attacker with RCE absolutely will. In this session we'll dissect a stock base image live using open tools (syft, grype, trivy), count exactly what an attacker gets for free, then rebuild the same app on a minimal/distroless base and measure the difference: 20x fewer packages, near-zero findings, no living-off-the-land toolkit. Along the way we'll map the result onto the frameworks Australian teams answer to the ISM's hardening controls, the Essential Eight's 48-hour patch clock, PSPF 2026's zero-trust push, and what an IRAP assessor actually asks about your scanner output. Less to attack, less to patch, less to explain.
