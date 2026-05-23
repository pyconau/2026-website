---
title: 'Ship Reliable RAG: Evals That Grow with Your Retrieval Complexity'
code: XWLM8L
start: '2026-08-27T11:20:00+10:00'
end: '2026-08-27T11:50:00+10:00'
room: Ballroom 3
track: data-and-ai
type: talk
speakers:
- ALM8CW
trackName: Data & AI
---

RAG applications come in many shapes. Some start as simple keyword searches over historical records. Others layer on semantic embeddings, hybrid retrieval (semantic + keyword/lexical searches), reranking, and increasingly sophisticated prompting. But regardless of where your system sits on that spectrum, the question is the same: how do you know it actually works?

This talk presents a level-by-level framework for building and evaluating RAG systems in Python, using a real AI-assisted ticket resolution application as the running example. Starting from the simplest possible retrieval setup (lexical matching with BM25 over historical tickets), the talk introduces evaluations early, explains why they matter, and then walks through growing both the RAG application and its eval suite in lockstep through four levels of complexity: lexical retrieval, semantic embedding-based retrieval, hybrid retrieval with log filtering using Drain3, and hybrid retrieval with reranking and context window tuning. At each level, the talk introduces only the evaluation metrics that become necessary at that stage, so the audience builds intuition for which evals matter and when.

Along the way, the talk covers practical topics including how to compose simple metrics like faithfulness, context precision, and recall into an experiment harness for tuning reranking strategies (comparing Weighted RRF, plain RRF, Z-score normalization, and Min-Max normalization), and for detecting context rot. At the end, the talk covers how to avoid common pitfalls in LLM-based evaluation such as positional bias and numerical scoring scales.

This talk is for Python developers and data scientists who are building or planning to build reliable & robust RAG applications and want a practical mental model for when to introduce which evaluations as their system grows in complexity.

The talk begins by introducing the use case: an AI-assisted IT support ticket resolution system that takes a ticket's title, description, comments, and log files as input and produces a one-shot resolution. 

This application serves as the running example throughout, but the framework applies to any domain where RAG is used to ground LLM responses in a knowledge base (e.g. customer support chatbots, travel agency chatbots, internal knowledge assistants).

Before diving into the levels, the talk covers a short primer on why evaluations matter for LLM applications. This includes the three stages at which evals become relevant: during feature development (20 to 100 targeted examples per workflow), just before production deployment (regression testing), and on live traffic after launch (monitoring resolution rates, knowledge drift, and user feedback). The goal is to establish that evals are not a one-time activity but something that evolves alongside the system.

**Level 1: Lexical retrieval**. The simplest retrieval approach: using BM25 keyword matching to find historically resolved tickets that resemble the incoming query. This is a viable first "vertical slice" that can be deployed for basic functionality. Evals at this stage focus on search query quality and hit rate. The audience learns how even a simple retrieval system benefits from having a ground truth test set.

**Level 2: Semantic retrieval**. Adding embedding-based vector search to capture meaning beyond exact keyword matches. This stage introduces retrieval-specific evaluation metrics: precision@k, recall@k, and contextual recall. The talk shows how these metrics help catch failure cases that lexical search alone would miss or failure cases that semantic search alone would not be able to handle.

**Level 3: Hybrid (semantic + lexical) retrieval with log filtering**. Combining semantic and lexical search, plus using Drain3 library for intelligent log filtering and preprocessing before ingestion. With two retrieval sources contributing results, the evaluation scope needs to expand. Document ingestion evals (BLEU/ROUGE for LLM-preprocessed text, chunking tuning via retrieval metrics) become relevant. Retrieval evals like embedding spread and generation evals like faithfulness, completeness, tonality, and safety/refusal checking are introduced here because the system is now complex enough for the LLM to hallucinate or produce inconsistent responses.

**Level 4: Hybrid retrieval with reranking and context window tuning**. The final level adds reranking to merge and prioritize results from multiple retrieval sources, and explores context window limits. This is where the core idea of the talk comes together: composing simple eval metrics (faithfulness, context precision, recall, answer relevancy, safety) into a systematic experiment harness, then sweeping across reranking strategies and weight configurations to find optimal settings. The talk walks through a concrete comparison of four approaches (Weighted RRF with tuned weights, plain RRF, Z-score normalization, Min-Max normalization) using a RAGAS-powered eval suite and a Streamlit dashboard. It also covers context rot evaluation to determine the maximum context size before retrieval quality degrades. Augmentation metrics like NDCG are introduced at this stage.

The talk closes with key learnings from production: designing for testability from day one, preferring binary or categorical grading scales over numerical Likert scales for LLM-based evaluation, and accounting for known LLM biases (positional, verbosity, self-bias) when building eval pipelines.
