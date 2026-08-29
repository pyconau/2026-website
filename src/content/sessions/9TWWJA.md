---
title: Whoops! I Accidentally Leaked My Credentials (again)
code: 9TWWJA
start: '2026-08-28T12:05:00+10:00'
end: '2026-08-28T12:35:00+10:00'
room: Ballroom 2
track: cybersecurity
type: talk
speakers:
- XPRNP3
trackName: Cybersecurity
abstract: "Leaked credentials aren't a new problem, but the complexity of modern development
  environments means that leaked credentials are more likely than ever to be your
  problem. Not only that, but recent research has shown that it may only be a matter
  of seconds between a leak and an exploit. As the systems for developing, building,
  publishing and deploying applications become more sophisticated, the types of leaks
  developers need to guard against also change.\r\n\r\nIn this talk, we will present
  new research® into when and how developers leak credentials in modern software applications.
  We'll discuss some of the common ways leaks occur for developers of open source
  artifacts like containers and software packages. We'll also provide practical insights
  into scalable credential scanning and ecosystem-level protections for developers
  and organisations who want to keep their credentials secure to help when every second
  counts."
---

Credential leaks have been around for as long as there have been credentials to leak. Because of the history, it's easy to think of credential leaks as a solved problem.

However, as modern software infrastructure becomes more sophisticated - from increased Cloud adoption, to the rise of containers and microservices architectures, to automated CI/CD and DevOps pipelines - developers and organizations have more credentials than ever to handle. While source forges like GitHub scan commits for leaked credentials, we continue to find many instances of credentials hidden in built open source artifacts like Docker containers/software packages.

We will offer new insights into this ongoing problem, and to better equip developers and organizations to prevent and tackle cases of leaked credentials. We'll also describe ongoing ecosystem-level efforts to integrate "pre-publish" scanning into open source artifact repositories like PyPI, which can save a huge amount of time, money and energy by preventing security attacks before they happen.
