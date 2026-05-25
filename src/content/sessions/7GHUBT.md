---
title: What Happened in Production?! Instrumenting with OpenTelemetry
code: 7GHUBT
start: '2026-08-27T14:35:00+10:00'
end: '2026-08-27T15:05:00+10:00'
room: Ballroom 1
track: platform-engineering
type: talk
speakers:
- 9MPTPG
trackName: Platform Engineering
abstract: "Every day at 2pm, our microservice crashed. Same traffic patterns, same
  infrastructure, same code - yet the database deadlocked and our SLA burned. Logs
  showed nothing. Metrics showed capacity. Something we couldn't see was destroying
  our system.\r\n\r\nThis is a story about unknown-unknowns: the failures you can't
  predict because you can't observe them. Join us as we retrace how OpenTelemetry
  exposed what our existing tools hid, guided by the principles of observability (or
  \"O11y\" as we'll affectionately call it).\r\n\r\nWe'll explore:\r\n- \"The three
  pillars\" of observability\r\n- OpenTelemetry Tracing with auto- and manual-instrumentation
  in Python\r\n- High cardinality, high dimensionality, and intelligent sampling\r\
  \n- Querying and visualising traces to debug production mysteries\r\n\r\nLeave knowing
  exactly where to start instrumenting your own services—and why you should, before
  2pm strikes your system."
---

This talk is designed for Python developers who have relied on logs and metrics for production debugging but haven't yet adopted distributed tracing, as well as SREs who appreciate a good production war story. No prerequisites are required, basic familiarity with Python, HTTP services, and databases is helpful but not required.

The session uses a narrative mystery format: a microservice that crashes daily at 2pm despite appearing healthy through traditional monitoring. Through a live dashboard of metrics, a "real" on-call alert, and real-time tracing data, you'll see how OpenTelemetry tracing solved the mystery. The talk includes staged architecture diagrams, code walkthroughs of Python instrumentation, and live querying of genuinely generated trace data.

You'll leave knowing exactly where to start with OpenTelemetry's auto-instrumentation (and how to move into manual-instrumentation when you're ready) in your own services, and with mental models for when tracing succeeds where logs and metrics fail.
