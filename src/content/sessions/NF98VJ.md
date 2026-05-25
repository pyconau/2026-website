---
title: Optimizing Scientific Python with C++, CUDA, and Serverless Compute
code: NF98VJ
start: '2026-08-29T11:55:00+10:00'
end: '2026-08-29T12:25:00+10:00'
room: Ballroom 2
track: research-software-engineering
type: talk
speakers:
- GVHZNZ
trackName: Research Software Engineering
abstract: "Moving computationally intensive scientific algorithms from desktop applications
  to cloud-based services presents unique challenges: How do you maintain performance
  when your code runs on ephemeral serverless infrastructure? How do you process datasets
  with 40 million points when Lambda functions have memory limits? \r\n\r\n   This
  talk shares our journey of migrating geological algorithms to a modern Python-based
  cloud platform. We'll explore the performance optimization techniques that made
  this possible, achieving 3–10× speedups through profiling-driven optimization across
  Python, C++, SIMD, GPU acceleration, and cloud-native batch processing. \r\n\r\n\
  \   This is not a talk about micro-optimizations or clever tricks. It's about building
  a sustainable performance engineering practice: measure first, optimize second,
  and automate the guardrails that prevent regression. Whether you're building ML
  pipelines, scientific simulations, or data processing systems, these principles
  will help you achieve high performance without sacrificing maintainability. \r\n\
  \r\nAfter this talk, you will learn how to: \r\n\r\n- Decide when to optimize in
  Python vs. when to reach for C++ \r\n- Use profiling tools to identify real bottlenecks—not
  assumed ones \r\n- Apply quality guardrails that catch bugs and prevent performance
  regressions \r\n- Design compute workloads for cloud-native horizontal scaling"
---

Over the past 18 months, our team has migrated several battle-tested geological algorithms to a cloud-based Python platform. The work touched every layer: from designing high-level cloud-native architecture to low-level optimization and loop vectorization. Along the way, profiling repeatedly surprised us—the bottlenecks were not where we expected. 

   The fundamental tensions between desktop and cloud—gigabytes of RAM vs. strict memory limits, persistent state vs. ephemeral execution, vertical vs. horizontal scaling—meant we couldn't simply "lift and shift" performance-critical code. Cloud-native requires rethinking our algorithms, not just our deployment. 

**Python/C++ Integration: When and Why** 

   Our decision framework helps determine when to stay in Python using batching and memory optimizations, and when switching to C++ produces real leverage. I'll share concrete examples of both paths—and how we decide between them. 

**The Performance Engineering Mindset** 

  Developers' intuition about bottlenecks can be wrong. I'll demonstrate a real investigation where profiling revealed that a slow compute-intensive loop wasn't bottlenecked by calculations—but by memory reallocations. This "measure first" methodology extends to compiler selection, where switching compilers delivered 25–80% speedups without changing a line of application code. 

**CPU and GPU Optimization** 

   When profiling reveals CPU-bound hotspots, SIMD vectorization is often our first optimization. I'll cover when it helps, when it doesn't, and how we measure effectiveness. For massively parallel workloads, we move computation to the GPU—I'll discuss when this makes sense and the Python integration patterns we use. 

**Cloud Architecture** 

   Our serverless architecture enables horizontal scaling. I'll cover how we handle data exchange and distribute computational effort between workers and maintain observability across distributed computations. 

**Lessons Learned** 

   I'll close with the key principles that emerged from this journey: why "Python first" remains our default, why measurement beats intuition, and how we prevent performance regressions through automated guardrails.
