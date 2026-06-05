# Project Proposal

## Linux-Inspired Smart Campus Network Simulation Using OMNeT++ 6.0.3

---

## 1. Title

**Design and Performance Analysis of a Multi-Subnet Smart Campus Network with QoS-Based Traffic Prioritization Using OMNeT++ and INET Framework**

---

## 2. Introduction

Modern educational institutions rely heavily on computer networks to support
academic, administrative, and operational activities. A university campus
network must serve diverse user groups — students, faculty members, and
administrative staff — each with distinct bandwidth requirements and service
quality expectations. However, network resources are finite. When thousands
of users share the same infrastructure, congestion becomes inevitable, and
without proper management, critical services can be degraded or disrupted.

This project proposes the design, simulation, and performance analysis of a
**Smart Campus Network** that organizes users into logically separated subnets
and implements Differentiated Services (DiffServ) based Quality of Service
(QoS) to prioritize traffic according to user role and application criticality.
The network is modeled and simulated using **OMNeT++ 6.0.3** — a discrete event
network simulator — along with the **INET 4.5 Framework**, which provides
ready-made, production-grade implementations of Internet protocols.

The specific goals of this project are:

1. To design a realistic multi-subnet campus network topology comprising
   student, teacher, administrator, and server segments interconnected via
   a core router and Ethernet switches.

2. To configure and simulate four distinct traffic scenarios: normal operation,
   high-load congestion, QoS-based priority handling, and a TCP-versus-UDP
   transport layer comparison.

3. To collect and analyze key performance metrics including end-to-end delay,
   throughput, packet delivery ratio, and packet loss across all scenarios.

4. To demonstrate that DSCP-based traffic prioritization effectively preserves
   service quality for high-priority users even under severe network congestion.

---

## 3. Motivation

The motivation for this project arises from both academic curiosity and real-world
relevance.

**Academic Motivation:** As a student of computer networking, I wanted to move
beyond textbook diagrams and theoretical explanations to build a working,
observable network where I could see packets flow, measure delays, and witness
protocols in action. Simulation offers a risk-free, cost-free environment to
experiment with network designs that would require substantial hardware
investment to implement physically.

**Practical Motivation:** In real campuses, network administrators face a
perennial dilemma: how to ensure that critical services — such as online
examination portals, attendance systems, and emergency notifications — remain
responsive even when the network is saturated by non-critical traffic like
video streaming and social media. The DiffServ QoS model, which marks packets
with priority codes at the network edge and processes them accordingly at each
router hop, is the industry-standard solution to this problem. Understanding
and demonstrating this mechanism through simulation builds practical skills
directly applicable to enterprise network management.

**Relevance:** With the increasing adoption of smart campus initiatives, IoT
deployments, and hybrid learning models, campus networks are growing in both
scale and complexity. The ability to simulate and analyze network behavior
before deployment is a valuable engineering skill that reduces risk, saves
costs, and enables evidence-based design decisions.

---

## 4. Background

### 4.1 Computer Networks and the OSI Model

Computer networks enable communication between computing devices through a
layered architecture. The TCP/IP model — the foundation of the modern
Internet — consists of four layers:

| Layer | Function | Protocols Used in This Project |
|-------|----------|-------------------------------|
| Application | User-facing services and data generation | Ping, UDP streaming, TCP request/reply |
| Transport | End-to-end communication reliability | TCP (reliable), UDP (best-effort) |
| Network | Logical addressing and routing | IPv4, ICMP, DSCP marking |
| Link / Physical | Frame delivery over physical media | Ethernet (100 Mbps), ARP, MAC learning |

Our simulation exercises all four layers of this stack, providing a holistic
view of how data moves from an application on one host, down through the
protocol stack, across physical links, and up through the stack on the
destination host.

### 4.2 Subnetting and Routing

A **subnet** (sub-network) is a logical subdivision of an IP network. Subnetting
improves security by isolating traffic between groups, enhances performance by
reducing broadcast domain size, and simplifies network management. In our design,
four /24 subnets are allocated — one for each user category and one for server
infrastructure.

**Routing** is the process of forwarding packets from a source subnet to a
destination subnet. The core router maintains a routing table that maps
destination network prefixes to outgoing interfaces. Static routing is used
in this project for simplicity and determinism, configured automatically by
INET's `Ipv4NetworkConfigurator`.

### 4.3 Quality of Service (QoS) and DSCP

Quality of Service refers to the ability of a network to provide differentiated
treatment to different traffic classes. The **Differentiated Services (DiffServ)**
architecture, defined in RFC 2474 and RFC 2475, uses the 6-bit **DSCP (Differentiated
Services Code Point)** field in the IP header to classify packets at network
boundaries. Routers then apply per-hop behaviors (PHBs) based on these markings.

Our simulation implements three DSCP classes:

| User Group | DSCP Value | PHB | Priority Level |
|-----------|-----------|-----|---------------|
| Administrators | 46 | EF (Expedited Forwarding) | Highest |
| Teachers | 26 | AF31 (Assured Forwarding) | Medium |
| Students | 0 | BE (Best Effort) | Lowest |

EF-marked packets receive priority queuing, minimizing delay and jitter.
AF-marked packets receive guaranteed delivery with moderate priority.
BE packets receive no special treatment.

### 4.4 OMNeT++ and INET Framework

**OMNeT++** (Objective Modular Network Testbed in C++) is an open-source,
component-based simulation platform widely used in academic and industrial
research for modeling communication networks, distributed systems, and
performance evaluation.

**INET** (Internet Simulation Framework) is the standard protocol model library
for OMNeT++. It provides accurate, maintained implementations of the TCP/IP
protocol stack, Ethernet, routing protocols, application models, and
visualization tools. Version 4.5 — used in this project — is the stable
release compatible with OMNeT++ 6.0.

### 4.5 Related Work

Network simulation for campus environments has been explored in prior academic
work. Researchers have used tools like Cisco Packet Tracer, GNS3, and NS-3
for similar purposes. However, OMNeT++ with INET offers a unique combination
of: (a) accurate protocol implementations derived from real-world standards,
(b) a modular architecture that allows component-level customization, (c) an
integrated visualization environment for educational demonstration, and
(d) comprehensive statistics collection for quantitative analysis.

---

## 5. Potential Outcomes

Upon successful completion of this project, the following outcomes are expected:

### 5.1 Functional Network Simulation

A fully operational campus network simulation comprising:

- **9 computing nodes:** 4 student PCs, 2 teacher PCs, 2 admin PCs, and
  1 campus server, each running the complete TCP/IP stack with realistic
  application-layer traffic generators.

- **3 Ethernet switches:** One per user subnet, performing MAC address
  learning and frame forwarding using the IEEE 802.1D bridging protocol.

- **1 core router:** Interconnecting all four subnets with static IPv4
  routing tables and per-interface IP configuration.

- **Proper subnet isolation:** Four independent /24 subnets (10.0.1.0/24,
  10.0.2.0/24, 10.0.3.0/24, 10.0.10.0/24) with correct routing between them.

### 5.2 Quantitative Performance Data

Measurable results from four distinct simulation scenarios, exported as
vector (.vec) and scalar (.sca) files analyzable in the OMNeT++ Analysis
Tool and compatible with Python/Matlab for further processing:

**Scenario 1 — Normal Operation:**
- Baseline end-to-end delay (expected: 1–5 ms)
- Baseline throughput (expected: low, well below link capacity)
- 100% packet delivery ratio under light load

**Scenario 2 — Congestion Behavior:**
- Queue length buildup at router egress interfaces
- Increased end-to-end delay under load (expected: 10–100× baseline)
- Packet loss due to queue overflow at bottleneck links
- Demonstration that TCP flows adapt their sending rate under congestion
  (TCP congestion control), while UDP flows continue unabated

**Scenario 3 — QoS Priority Verification:**
- Admin packets (DSCP 46) experience significantly lower delay than student
  packets (DSCP 0) during congestion
- Teacher packets (DSCP 26) show intermediate delay
- Quantitative separation of delay distributions across the three classes
- Evidence that DiffServ-based QoS is effective even without per-flow
  resource reservation

**Scenario 4 — Protocol Comparison:**
- TCP sessions demonstrate reliable delivery with connection overhead
- UDP streams demonstrate lower per-packet latency but with potential loss
- Throughput comparison showing TCP's throughput is bounded by round-trip
  time and window size, while UDP throughput is limited only by the
  application send rate and available bandwidth

### 5.3 Educational Documentation

A comprehensive README document explaining every aspect of the project
from first principles — suitable for a complete beginner to understand
network topology, protocol behavior, QoS mechanisms, and simulation
methodology. This serves as both project documentation and a reusable
learning resource.

### 5.4 Reproducible Research Artifact

The complete project source code, configuration files, and build
instructions are version-controlled and publicly available on GitHub
at [https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation](https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation).
Any researcher or student with OMNeT++ 6.0.3 and INET 4.5 can clone
the repository, build the project, and reproduce all results with
a single command.

### 5.5 Skills Acquired

Through this project, the following practical skills are developed:

- Network topology design using the NED (Network Description) language
- Simulation configuration and parameterization using OMNeT++ INI files
- Understanding of the TCP/IP protocol stack through hands-on experimentation
- QoS policy design and DSCP-based traffic classification
- Performance metric collection, analysis, and interpretation
- Version control with Git and collaborative development workflows
- Technical writing and documentation

---

## 6. Conclusion

This project demonstrates the end-to-end process of designing, simulating,
and analyzing a multi-subnet campus network with QoS-based traffic prioritization
using industry-standard simulation tools. By modeling four distinct user groups
with realistic traffic patterns and systematically subjecting the network to
increasing load, we can observe and quantify the behavior of TCP/IP protocols
under both normal and stressed conditions.

The implementation of DSCP-based priority handling validates the DiffServ
architecture as an effective mechanism for preserving critical service quality
during congestion events — a finding with direct relevance to real-world
campus network administration.

Beyond the technical outcomes, this project serves as a pedagogical tool that
bridges the gap between theoretical networking concepts and their practical
application. The simulation-based approach enables visualization, experimentation,
and measurement in ways that purely theoretical study cannot provide.

Future extensions to this work could include: (a) integration of wireless
access points and mobile nodes to model WiFi-enabled campus environments,
(b) implementation of dynamic routing protocols such as OSPF for adaptive
path selection, (c) addition of firewall rules and access control lists
for security policy enforcement, (d) integration of IoT sensor nodes to
model a smart campus ecosystem, and (e) performance comparison with Software
Defined Networking (SDN) based architectures.

---

## 7. References

[1] A. Varga and R. Hornig, "An Overview of the OMNeT++ Simulation Environment,"
    in *Proceedings of the 1st International Conference on Simulation Tools and
    Techniques for Communications, Networks and Systems (SIMUTools)*, Marseille,
    France, 2008.

[2] OpenSim Ltd., "INET Framework for OMNeT++," [Online].
    Available: https://inet.omnetpp.org/. [Accessed: June 2026].

[3] OMNeT++ Documentation, "OMNeT++ 6.0.3 User Manual," [Online].
    Available: https://doc.omnetpp.org/omnetpp/manual/. [Accessed: June 2026].

[4] K. Nichols, S. Blake, F. Baker, and D. Black, "Definition of the
    Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers,"
    IETF RFC 2474, December 1998. [Online].
    Available: https://datatracker.ietf.org/doc/html/rfc2474.

[5] S. Blake, D. Black, M. Carlson, E. Davies, Z. Wang, and W. Weiss,
    "An Architecture for Differentiated Services," IETF RFC 2475,
    December 1998. [Online].
    Available: https://datatracker.ietf.org/doc/html/rfc2475.

[6] J. Postel, "Internet Protocol," IETF RFC 791, September 1981. [Online].
    Available: https://datatracker.ietf.org/doc/html/rfc791.

[7] J. Postel, "Transmission Control Protocol," IETF RFC 793, September 1981.
    [Online]. Available: https://datatracker.ietf.org/doc/html/rfc793.

[8] J. Postel, "User Datagram Protocol," IETF RFC 768, August 1980. [Online].
    Available: https://datatracker.ietf.org/doc/html/rfc768.

[9] J. Kurose and K. Ross, *Computer Networking: A Top-Down Approach*,
    8th ed. Pearson, 2020.

[10] A. S. Tanenbaum and D. J. Wetherall, *Computer Networks*, 6th ed.
     Pearson, 2021.

[11] OpenSim Ltd., "INET 4.5 API Reference," [Online].
     Available: https://inet.omnetpp.org/docs/. [Accessed: June 2026].

[12] IEEE 802.1D-2004, "IEEE Standard for Local and Metropolitan Area
     Networks: Media Access Control (MAC) Bridges," IEEE, 2004.

[13] IEEE 802.3-2018, "IEEE Standard for Ethernet," IEEE, 2018.

[14] B. Forouzan, *Data Communications and Networking*, 5th ed.
     McGraw-Hill, 2012.

---

**Submitted by:** Nazrana Nahreen
**Date:** June 5, 2026
**Repository:** [https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation](https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation)
