---
title: 'Testing Beyond Examples: Property Based Testing with Hypothesis'
code: JZQG9G
start: '2026-08-29T10:45:00+10:00'
end: '2026-08-29T11:15:00+10:00'
room: Ballroom 3
track:
type: talk
speakers:
- GX9AZX
trackName: Main Conference
abstract: "Most of us learn testing by writing examples. Put some input in, check
  the output, move on. That works… until it doesn’t. Edge cases slip through, assumptions
  hide in plain sight, and the tests that felt thorough turn out to only cover the
  obvious cases.\r\n\r\nThis talk is an introduction to property based testing in
  Python using Hypothesis. Instead of hand writing endless individual test cases,
  we describe the rules that should always hold true, then let Hypothesis generate
  a huge range of inputs for us, including the weird ones we probably would not have
  thought to test ourselves. I’ll show how this changes the way you think about tests,
  where it works especially well, and how to start using it in real Python projects
  without making your test suite harder to understand."
---

Property based testing is one of those ideas that can feel slightly magical the first time you see it working. You write down the behaviour that should always be true, and suddenly your tests are exploring inputs you never bothered to write by hand. Empty strings, giant integers, unexpected Unicode, awkward combinations of values, all the annoying little corners where bugs like to hide… Hypothesis goes looking for them on purpose.

In this talk I’ll introduce the core ideas behind property based testing through practical Python examples. We’ll look at how Hypothesis generates data, how shrinking helps produce useful failures instead of unreadable chaos, and how to recognise the kinds of problems that are a good fit for this style of testing. I’ll also cover some of the common sticking points, like tests that become too vague, properties that sound clever but do not actually prove much, and the difference between writing a test that feels abstract versus one that is genuinely useful.

The goal is not to convince you that every test should be property based. It is to give you another tool for the jobs where example based tests are brittle, incomplete, or just plain tedious. By the end, attendees should have a solid practical introduction to Hypothesis, a clearer mental model for how property based testing works, and a good sense of where it can immediately improve the way they test Python applications.
