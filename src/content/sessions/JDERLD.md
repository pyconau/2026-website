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
trackName: Data & AI
abstract: "AI-assisted screening tools for diabetic retinopathy (DR) are increasingly
  \r\nbeing considered for deployment within national health systems. In Aotearoa
  \r\nNew Zealand, the diabetic retinal screening programme serves over 200,000 \r\
  \npeople, and AI tools — including THEIA, a system prospectively validated \r\n\
  within the NZ programme — are being evaluated for clinical integration. \r\nPublished
  clinical trials consistently report strong aggregate diagnostic \r\naccuracy. But
  aggregate performance metrics can obscure something critical: \r\ndoes the tool
  perform equally well for *everyone*?\r\n\r\nThis talk presents a simulation-based
  evaluation framework, built entirely \r\nin Python, that interrogates the equity
  implications of deploying AI \r\nscreening tools across demographically diverse
  populations. Māori and Pacific \r\npeoples in New Zealand experience higher rates
  of both diabetes and diabetic \r\nretinopathy, greater socioeconomic deprivation,
  and lower screening attendance \r\nthan NZ European populations. If an AI tool performs
  less accurately for \r\nthese groups — even modestly — deployment at scale could
  widen existing \r\nhealth disparities rather than close them.\r\n\r\n**The Framework**\r\
  \n\r\nThe framework generates a synthetic cohort of 10,000 patients calibrated to
  \r\nthe NZ diabetic screening population, with demographics (ethnicity, age, sex,
  \r\nNZDep deprivation quintile) and true disease status drawn from published \r\n\
  epidemiological data. Three AI tool profiles are then simulated: the IDx-DR \r\n\
  system (from its pivotal trial and a recent meta-analysis) and the \r\nNZ-developed
  THEIA system. Each tool is evaluated under two scenarios — equal \r\nperformance
  across subgroups, and differential performance informed by bias \r\npatterns documented
  in the clinical AI literature.\r\n\r\nPerformance metrics (sensitivity, specificity,
  PPV, ROC curves) are \r\ndisaggregated by ethnicity, area deprivation (NZDep), and
  their intersection, \r\nwith statistical testing to identify significant disparities.\r\
  \n\r\nAll simulation parameters are fully documented with citations in a \r\n`config/parameters.yaml`
  file, making the framework transparent, reproducible, \r\nand adaptable. The code
  is structured as three Jupyter notebooks (cohort \r\ngeneration, diagnostic accuracy
  evaluation, equity analysis) backed by a \r\nclean Python module layer — so anyone
  can swap in their own AI tool's \r\nperformance data and re-run the analysis for
  their own health system context.\r\n\r\n**Key Findings**\r\n\r\nEven modest subgroup-level
  accuracy gaps — easily obscured in aggregate trial \r\nreports — translate into
  meaningfully worse outcomes for already-disadvantaged \r\npopulations when projected
  across a national programme. This is not a \r\nhypothetical concern. Studies of
  AI diagnostic tools in chest radiology, \r\nophthalmology, and dermatology have
  documented precisely this pattern.\r\n\r\n**Why Python, Why This Matters**\r\n\r\
  \nPython provides all the tools needed to build rigorous equity evaluations: \r\n\
  NumPy and Pandas for cohort simulation, SciPy for statistical testing, and \r\n\
  Matplotlib/Seaborn for disaggregated visualisation. This talk demonstrates \r\n\
  that pre-deployment equity evaluation doesn't require proprietary software or \r\
  \nlarge clinical datasets — just well-structured Python and publicly available \r\
  \nliterature.\r\n\r\nAttendees will leave with: an understanding of why aggregate
  AI performance \r\nmetrics are insufficient for equitable deployment decisions;
  a mental model \r\nfor simulation-based pre-deployment evaluation; and an open-source
  Python \r\nframework (MIT licence) they can adapt to their own context."
---

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
