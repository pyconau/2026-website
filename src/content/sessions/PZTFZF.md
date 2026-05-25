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
abstract: Privacy regulations around the world impose strict requirements on how
  organisations handle personal data (such as Australia's Privacy Act, the EU's 
  GDPR, US's HIPAA & CCPA, etc). Among the hardest to implement in a data 
  pipeline are protecting sensitive data from breaches, and erasing an 
  individual's personal data on request.Finding and deleting every copy of 
  sensitive data is cumbersome, error-prone, and breaks referential integrity. 
  Meanwhile, sensitive data sitting in plaintext is exposed the moment a breach 
  occurs.
---

This talk introduces a novel data pipeline architecture, enabled by an open-source Python library created by the speaker, to solve this complex compliance requirement in a single action.
The library implements the crypto-shredding pattern. 
- Sensitive fields are encrypted with a unique encryption key per customer, before data is loaded into the platform, restricting access and protecting it during leaks. 
- Analytical sensitive fields are generalised to enable analytics use, while protecting the original value.
- Encryption keys are stored separately outside the data platform, ensuring sensitive data stays unreadable even when the data platform is breached.
- Data erasure becomes a single operation: delete the encryption key, and the respective customer's data is rendered permanently unreadable across all tables — without modifying or scanning any data, preserving analytics & referential integrity.
- Decrypts sensitive data under authorisation for any customer whose key is maintained.

The talk covers the architecture, the cryptographic foundations of the Python library, practical integration into Python pipelines, and data governance framework for encryption key management and rotation, including a live demo of the library.
