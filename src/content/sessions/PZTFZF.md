---
title: Privacy data encryption & deletion while preserving analytical integrity
code: PZTFZF
start: '2026-08-28T14:35:00+10:00'
end: '2026-08-28T15:05:00+10:00'
room: Ballroom 3
track: cybersecurity
type: talk
speakers:
- UMB3JY
trackName: Cybersecurity
---

Privacy regulations around the world impose strict requirements on how organisations handle personal data (such as Australia's Privacy Act, the EU's GDPR, US's HIPAA & CCPA, etc). Among the hardest to implement in a data pipeline are protecting sensitive data from breaches, and erasing an individual's personal data on request.Finding and deleting every copy of sensitive data is cumbersome, error-prone, and breaks referential integrity. Meanwhile, sensitive data sitting in plaintext is exposed the moment a breach occurs.

This talk introduces a novel data pipeline architecture, enabled by an open-source Python library created by the speaker, to solve this complex compliance requirement in a single action.
The library implements the crypto-shredding pattern. 
- Sensitive fields are encrypted with a unique encryption key per customer, before data is loaded into the platform, restricting access and protecting it during leaks. 
- Analytical sensitive fields are generalised to enable analytics use, while protecting the original value.
- Encryption keys are stored separately outside the data platform, ensuring sensitive data stays unreadable even when the data platform is breached.
- Data erasure becomes a single operation: delete the encryption key, and the respective customer's data is rendered permanently unreadable across all tables — without modifying or scanning any data, preserving analytics & referential integrity.
- Decrypts sensitive data under authorisation for any customer whose key is maintained.

The talk covers the architecture, the cryptographic foundations of the Python library, practical integration into Python pipelines, and data governance framework for encryption key management and rotation, including a live demo of the library.

This talk is for anyone building Python pipelines and/or handling personal data, such as data architects, data engineers, platform engineers, analytics engineers, etc. The talk builds up from the problem to the solution, covering both the why and the how.

1. The problem (5 min)
- Sensitive data in plaintext stored in the data platform is a breach liability that most data platforms accept by default.
- Most companies do not have a solution for policy-compliant sensitive data erasure. The conventional approach to run DELETE statements across all tables in multiple layers fails to guarantee completeness, and breaks referential & analytical integrity.

2. The pipeline architecture and crypto-shredding pattern (8 min)
- Encrypting sensitive data per customer before loading turns data erasure from a data scanning problem into a key management problem. 
- The architecture: encryption sits between extract and load in the pipeline, keys are stored outside the data platform in a separate key store with separate access controls. 
- Why this separation matters: access to the data platform alone is not sufficient to decrypt any sensitive data. This architecture enables single-operation erasure, and protects against breaches.

3. The encryption method, and governance framework (5 min)
- The same values will encrypt into different ciphertext outputs, thereby protecting against pattern-detection to identify known individuals.
- Deleting the encryption key renders decryption mathematically impossible, fulfilling legal requirements for sensitive data erasure.
- Analytical sensitive data is generalised to allow for fair use.
- Key management, rotation, and decryption framework.

4. Live demo and additional architecture guidance (7 min)
A walkthrough using the open-source Python library created by the speaker: encrypting a DataFrame, inspecting the key store, deleting a customer's key, demonstrating the decryption fail, batch key fetching for pipeline performance, handling managed ingestion tools (Fivetran, Airbyte) where encryption happens post-load. 

5. Q&A (5 min)
