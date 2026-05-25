---
title: Launching Rockets with Python
code: 9KBBEQ
start: '2026-08-28T10:45:00+10:00'
end: '2026-08-28T11:15:00+10:00'
room: Ballroom 2
track:
type: talk
speakers:
- GRFBNL
layout: layout_2
trackName: Main Conference
abstract: "I'm not joking. In 2025 and 2026 our university rocketry team launched
  several high-powered 12ft tall competition rockets with a custom Python-based process
  manager framework that controlled all of their rocket telemetry and ground control
  systems. We called it the Ground Control Station, or GCS for short. \r\n\r\nI lead
  the creation of the GCS software to compete at the 2025 International Rocket Engineering
  Competition (IREC) with the intention of winning the Rocket Telemetry Visualisation
  Sub-Category. We have our own custom flight computer with it's own custom firmware
  and LoRa networking setup. So we build our visualisation system from the ground
  up for reliability, scaleability and deployability. All in our Python process manager"
---

The GCS, known as SOTERIA, is a computer control system for GSE control, avionics communication, and data visualisation. The core of the GCS is a single computer running Student Researched And Designed (SRAD) software with SRAD LoRa radio hardware peripherals. All OSI layers in our networking stack above the physical protocol are SRAD for use with our Australis (avionics) ecosystem. The software converts raw serial input from physical radio interfaces into human-readable output for efficient system monitoring by the GCS operator and visualisations for observers. We use a WebSocket and a protocol buffer based IPC API to communicate with our GCS services. Our web frontend is fully SRAD aside from industry-standard libraries. The GCS operator can see if any system is performing sub-optimally via alert and warning readouts, so they can make an informed GO/NO-GO call quickly. Spectators and other team members have access to several different views detailing all telemetry from both the GSE and avionics systems

This project was built using the following tools, languages and systems.

- Radio communication:
    - [LoRa](https://en.wikipedia.org/wiki/LoRa) with both COTS and SRAD hardware
- Multithreaded data ingestion server
    - Written in C++
    - Built with [ZeroMQ](https://zeromq.org/) for IPC communication
    - IPC Data serialisation with [Google's Protocol Buffers](https://protobuf.dev/)
- Multithreaded CLI based process manager
    - Written in Python
    - Includes a device emulator for internal system tests that attaches from the hardware layer to create a fake unix device file at `/dev/`

**Cool fact**: Our GCS runs at less than 1% CPU utilization on a Raspberry Pi 5 during regular use.
