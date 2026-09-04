---
title: "SCADA System with Industrial Networking"
track: "controls-engineer"
difficulty_tier: "intermediate"
estimated_hours: 14
role: "core"
skill_tags: ["hmi-scada", "industrial-protocols", "plc-programming", "networking-fundamentals", "sql"]
skill_prerequisites: ["plc-programming"]
project_prerequisites: ["plc-machine-control-with-hmi.md"]
prerequisite_learning_hours: 3
---

# SCADA System with Industrial Networking

## Production Workflow Mirrored
1. Connecting multiple controllers over industrial protocols
2. Building a supervisory system with tags, alarms, trends, and history
3. Designing a segmented, secure industrial network
4. Handling communication failures gracefully
5. Reporting production data to business systems

## What You'll Build
A supervisory system over two or more controllers (your PLC program
plus a second simulated controller or a microcontroller speaking
Modbus): communication via Modbus TCP and OPC UA, a SCADA application
(Ignition trial, an open-source SCADA, or a Python-based one) with a
tag structure, an overview screen, alarming with priorities, trending,
and historical logging to a database, a network design with
segmentation, and a communication-failure test with documented behavior.

## Student-Scope Notes
- Ignition's trial mode is free and resets every two hours; open-source
  options (FUXA, ScadaBR) or a Python OPC UA server are fine.
- The second controller can be a Modbus simulator or an ESP32 with a
  Modbus library.
- Network segmentation can be demonstrated with VLANs on a managed
  switch or with containers and firewall rules.

## Steps
1. Design the tag structure and naming convention across both
   controllers, and the alarm priority scheme.
2. Configure Modbus TCP to the microcontroller or simulator and OPC UA
   to the PLC, and verify data flows in both directions.
3. Build the SCADA screens: an overview, per-machine detail, and a
   navigation structure following high-performance HMI principles.
4. Configure alarms with priorities, deadbands, and shelving, and an
   alarm summary with history.
5. Set up trending and historical logging to a database, and write SQL
   queries for production counts and downtime.
6. Design the network: zones, a demilitarized zone for the historian,
   firewall rules, and no direct routes from the business network to
   controllers; implement what you can.
7. Test communication failures: unplug a controller, restart the
   server, and document how tags, alarms, and history behave; fix gaps.
8. Write the SCADA design document: tags, screens, alarms, network,
   and the failure test results, plus a production report from the
   database.

## Extension Ideas
- Add MQTT and publish data to a cloud dashboard.
- Implement a redundancy or store-and-forward configuration.
- Add user roles and an audit trail.
- Integrate an overall equipment effectiveness calculation.

## Skills Demonstrated
- Multi-protocol industrial communication
- SCADA design with alarms, trends, and history
- Industrial network segmentation and security basics
- Failure testing of supervisory systems

## Industry Relevance

Utilities, Manufacturing Plants, Oil and Gas, Water Treatment. SCADA and industrial networking are the connective tissue of operations in these sectors, and controls engineers who understand both protocols and security are increasingly required. A multi-controller SCADA with a network design and failure tests is a strong portfolio piece for automation roles.
