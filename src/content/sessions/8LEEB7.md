---
title: 'The 20-Year Port: from PhD project to polished professional Python packaging'
code: 8LEEB7
start: '2026-08-28T16:10:00+10:00'
end: '2026-08-28T16:40:00+10:00'
room: Ballroom 2
track:
type: talk
speakers:
- 9YWARS
trackName: Main Conference
graphicsLayout: right
theme: accent_violet
---

Porting a scientific software library from a proprietary language to Python can potentially increase its user base, but the porting process itself can be tedious and error prone, and therefore cries out for automation, such as the use of AI coding agents. At the same time, scientific software libraries must be accurate, performant, easy to use, and easy to maintain. An over-reliance on automated tools can result in the software porting equivalent of AI slop: code that is unreliable and unmaintainable. The application of Research Software Engineering principles to the porting of scientific code can complement AI coding agents in preserving both academic rigour and thorough testing throughout the porting process, resulting in a reliable, well-tested and well-documented library.

In 2006, my mathematics PhD project resulted in a highly specialized geometrical toolbox that over the years has been used in diverse scientific and engineering applications. In 2013, at a SciPy conference, one of the attendees asked when the toolbox would be ported to Python.

On and off over a period of 20 years, I took that toolbox on a journey from an open source package within a proprietary mathematical software ecosystem to its current state as a polished, production-grade Python library. Firstly, in 2024, motivated by my deepening understanding of the diversity of its applications, I modernized the toolbox itself, including automating the testing of help examples. Next, in 2025, the rapid rise of Large Language Models as coding agents prompted me to undertake the long-delayed Python port. The coding agents did far more than a superficial translation of language syntax to Python. They improved the performance of the code by implementing improved algorithms, they converted the help examples into doctests, they created an automated test harness, they helped me to organize and improve the documentation, and they helped automate the PyPI release process.

This talk presents a case study in transforming specialized high-quality mathematical software from a proprietary interpreter environment to modern Python. It focuses on the application of Research Software Engineering principles to a single-maintainer project, including preserving the integrity of the science while improving usability and maintainability. It covers three stages of the transformation.

1. The first stage involved maintaining the original toolbox as a single maintainer project while the proprietary interpreter environment changed around it. This included my attempts to add new features  while running out of time and energy. This stage reached a turning point in 2024 with my realization that the publication of a survey of applications of the toolbox would be enhanced by an uplift of the toolbox to make it more usable and more reliable through completion of promised features and through better testing.
2. The second stage involved seizing the opportunity of that coding agents provided. This began with the use of GitHub Copilot and the Google Antigravity harness with Large Language Models such as Gemini 3 and Claude Sonnet 4.6 as coding agents to translate the toolbox code, the help text and the help examples to Python code, Sphinx docstrings and executable doctests.
3. The third stage involved greatly increasing the rigour and polish of the project. This included pushing the Python project to 100% test coverage using doctest and pytest, strict 10.0 linting with Ruff and Pylint, and automated PyPI deployment. The final polish includes organizing the documentation into a User Guide and Maintenance Guide, and automating the testing of document quality.

**Key Audience Learning Outcomes**:
- Strategies for preparing scientific codebases for expansion from proprietary language ecosystems to Python.
- A model for AI-assisted porting that prioritizes the migration of tests and documentation alongside code.
- Techniques for navigating the shift in focus from PhD-level research tools to production-grade software.
