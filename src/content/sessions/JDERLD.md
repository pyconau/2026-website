---
title: 'When AI Screens for Blindness: Equity Evaluation Using Python'
code: JDERLD
start: '2026-08-27T15:10:00+10:00'
end: '2026-08-27T15:40:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- SNK8RV
layout: layout_2
trackName: Data & AI
graphicsLayout: left
theme: accent_lemon
---

AI-assisted screening tools for diabetic retinopathy (DR) are increasingly 
being considered for deployment within national health systems. In Aotearoa 
New Zealand, the diabetic retinal screening programme serves over 200,000 
people, and AI tools — including THEIA, a system prospectively validated 
within the NZ programme — are being evaluated for clinical integration. 
Published clinical trials consistently report strong aggregate diagnostic 
accuracy. But aggregate performance metrics can obscure something critical: 
does the tool perform equally well for *everyone*?

This talk presents a simulation-based evaluation framework, built entirely 
in Python, that interrogates the equity implications of deploying AI 
screening tools across demographically diverse populations. Māori and Pacific 
peoples in New Zealand experience higher rates of both diabetes and diabetic 
retinopathy, greater socioeconomic deprivation, and lower screening attendance 
than NZ European populations. If an AI tool performs less accurately for 
these groups — even modestly — deployment at scale could widen existing 
health disparities rather than close them.

**The Framework**

The framework generates a synthetic cohort of 10,000 patients calibrated to 
the NZ diabetic screening population, with demographics (ethnicity, age, sex, 
NZDep deprivation quintile) and true disease status drawn from published 
epidemiological data. Three AI tool profiles are then simulated: the IDx-DR 
system (from its pivotal trial and a recent meta-analysis) and the 
NZ-developed THEIA system. Each tool is evaluated under two scenarios — equal 
performance across subgroups, and differential performance informed by bias 
patterns documented in the clinical AI literature.

Performance metrics (sensitivity, specificity, PPV, ROC curves) are 
disaggregated by ethnicity, area deprivation (NZDep), and their intersection, 
with statistical testing to identify significant disparities.

All simulation parameters are fully documented with citations in a 
`config/parameters.yaml` file, making the framework transparent, reproducible, 
and adaptable. The code is structured as three Jupyter notebooks (cohort 
generation, diagnostic accuracy evaluation, equity analysis) backed by a 
clean Python module layer — so anyone can swap in their own AI tool's 
performance data and re-run the analysis for their own health system context.

**Key Findings**

Even modest subgroup-level accuracy gaps — easily obscured in aggregate trial 
reports — translate into meaningfully worse outcomes for already-disadvantaged 
populations when projected across a national programme. This is not a 
hypothetical concern. Studies of AI diagnostic tools in chest radiology, 
ophthalmology, and dermatology have documented precisely this pattern.

**Why Python, Why This Matters**

Python provides all the tools needed to build rigorous equity evaluations: 
NumPy and Pandas for cohort simulation, SciPy for statistical testing, and 
Matplotlib/Seaborn for disaggregated visualisation. This talk demonstrates 
that pre-deployment equity evaluation doesn't require proprietary software or 
large clinical datasets — just well-structured Python and publicly available 
literature.

Attendees will leave with: an understanding of why aggregate AI performance 
metrics are insufficient for equitable deployment decisions; a mental model 
for simulation-based pre-deployment evaluation; and an open-source Python 
framework (MIT licence) they can adapt to their own context.

This talk is for Python practitioners interested in data science, healthcare, 
and responsible AI. No clinical background is needed — the focus is on 
methodology and Python implementation, accessible to intermediate Python 
users and above.

**Talk outline (~30 min):**

- **(5 min)** Why aggregate AI performance metrics miss equity problems — and 
  why this matters for real deployment decisions
- **(8 min)** The simulation framework: cohort generation, AI profile 
  modelling, and Python implementation walkthrough
- **(7 min)** Results — what equity-stratified analysis reveals that 
  aggregate metrics hide
- **(5 min)** How to adapt the framework to other contexts; a call for 
  equity evaluation as standard practice in AI deployment
- **(5 min)** Q&A
