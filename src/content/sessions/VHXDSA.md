---
title: 'AI-assisted coding, Python and dbt: taking Chronos live in two days'
code: VHXDSA
start: '2026-08-27T10:45:00+10:00'
end: '2026-08-27T11:15:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- GLH9FZ
- 38JMFR
trackName: Data & AI
graphicsLayout: left
theme: accent_lemon
---

We needed to produce 25 years of gap-free half-hourly weather data in just two days. The output had to be continuous, reproducible, and ready for production use. We achieved that speed by combining domain knowledge, Python, dbt, and AI-assisted coding, with detailed prompting and a few tight loops of refinement rather than a zero-shot approach. In this talk, we’ll show how we used Python, dbt, and the Chronos-2 time-series foundation model to build a practical weather gap-filling pipeline for variables such as temperature, humidity, and wind speed.

This talk focuses on a practical Python engineering question: when does a foundation model become a pragmatic shortcut rather than just an impressive demo? We’ll compare our Chronos-based workflow with a more traditional approach using correlations with nearby weather stations, explain why dbt was such a strong backbone for reproducibility and maintainability, and show why that mattered for a pipeline that needed to remain understandable and easy to update. We’ll also show that gap filling is different from ordinary forecasting: because a missing window has data on both sides, future approaches could fill forward from the start of the gap, backward from the end, and meet in the middle.

This talk is for Python users who work with time series, messy data, or production data workflows and want a practical case study rather than a theoretical forecasting talk.

We’ll walk through how we built a repeatable Python and dbt pipeline for weather gap filling, how we evaluated Chronos against a more traditional approach using correlations with nearby weather stations, and why the more classical method turned out to be harder to make seamless in practice. Traditional approaches based on interpolation and correlations with nearby weather stations are often more explainable, but they can be difficult to stitch together smoothly, with the joins between methods creating visible discontinuities.

A big part of the story is how domain knowledge, data science, and AI-assisted coding worked together in practice. AI-assisted coding helped us move faster, but only because it was used in a highly specified way: detailed prompts, iterative refinement, and close human review. dbt gave us a reliable backbone for reproducibility, helped turn a one-off modelling exercise into a maintainable pipeline, and made the workflow easier to understand, test, and keep up to date. That mattered because the people maintaining the pipeline were not necessarily deep ML specialists: Python handled the modelling and analysis, while dbt provided the structure, lineage, repeatable builds, and a way for a broader team to support the pipeline.
Attendees will leave with a practical view of:

-	when a foundation model can be a pragmatic shortcut rather than just an impressive demo
-	how Python can tie together data preparation, model execution, evaluation, and operational delivery
-	how dbt can make this kind of workflow more reproducible, maintainable, and accessible to a broader team
-	why gap filling is different from ordinary forecasting, because missing windows can potentially be filled from both directions rather than only from the past
-	how challenging weather data can be, because variables such as wind speed, humidity, and temperature behave very differently and gaps can arise from sensor failures or communication dropouts
-	what trade-offs appear when you need something robust and maintainable quickly, not something theoretically perfect
