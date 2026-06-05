# Project Proposal

## Linux-Inspired Smart Campus Network Simulation Using OMNeT++ 6.0.3

---

## 1. Title

**Linux-Inspired Smart Campus Network: Multi-Subnet Architecture with Firewall Access Control, QoS Traffic Prioritization, and Protocol-Level Performance Analysis Using OMNeT++ and INET Framework**

---

## 2. Introduction

Modern educational institutions depend on computer networks to support academic,
administrative, and operational activities. A university campus network serves
diverse user groups — students, faculty members, and administrative staff — each
with distinct bandwidth requirements, security clearance levels, and service
quality expectations. However, network resources are finite. When many users
share the same infrastructure, congestion becomes inevitable, and without proper
management, critical services degrade. Moreover, without access control, any user
could potentially reach any other user's device, creating security vulnerabilities.

This project proposes a **Linux-inspired Smart Campus Network** that models
real-world Linux networking concepts within the OMNeT++ simulation environment.
The network is designed around five core principles drawn directly from Linux
system administration:

1. **Linux Server Architecture** — A centralized application server running
   multiple service daemons on different ports, exactly as a Linux server
   would with systemd-managed services.

2. **iptables-Style Firewall** — Access control between subnets enforced by
   the core router through explicit allow-list routing, analogous to Linux
   iptables FORWARD chain rules that selectively permit or DROP traffic.

3. **User Permission Model** — Logical subnet isolation where each user group
   has different network privileges, mirroring Linux file permissions (owner/
   group/others) applied to network access.

4. **Service Hosting on Separate Ports** — The campus server hosts four
   independent services on different ports (1000, 2000, 3000, 4000), equivalent
   to a Linux machine running multiple daemons like Apache, MySQL, SSH, etc.

5. **QoS-Based Priority Access** — DSCP traffic classification ensuring
   Administrator > Teacher > Student priority, modeling Linux Traffic Control
   (tc) and queuing disciplines (qdiscs) on a production router.

The simulation is built using **OMNeT++ 6.0.3** with the **INET 4.5 Framework**,
providing accurate, production-grade implementations of the TCP/IP protocol stack,
Ethernet, routing, and application models.

### Project Objectives

1. Design a realistic 4-subnet campus network topology with 9 computing nodes,
   3 Ethernet switches, and a core router.

2. Implement access control between subnets (firewall rules) using explicit
   route-based filtering that mirrors Linux iptables behavior.

3. Configure and simulate five distinct scenarios: normal operation,
   high-load congestion, QoS-based priority handling, TCP-vs-UDP transport
   comparison, and firewall access control verification.

4. Demonstrate that DSCP-based traffic prioritization (EF/AF31/BE) preserves
   service quality for high-priority users during network congestion.

5. Collect and analyze end-to-end delay, throughput, packet delivery ratio,
   and packet loss across all scenarios.

---

## 3. Motivation

### Academic Motivation

As a student of computer networking, I wanted to move beyond textbook diagrams
to a hands-on, observable system where I could see packets flowing through
protocol stacks, measure delays, and witness how routing, firewalling, and QoS
behave in real-time. Simulation provides a risk-free, zero-cost environment to
experiment with designs that would require substantial hardware investment to
build physically.

### Practical Motivation

In real campus networks, administrators face competing demands:

- **Students** generate heavy traffic: streaming, downloads, social media
- **Teachers** need reliable access to academic systems
- **Administrators** require guaranteed connectivity for emergency alerts,
  attendance systems, and examination portals

The DiffServ QoS model, combined with iptables-style access control, is the
industry-standard solution. Understanding these mechanisms through simulation
builds skills directly applicable to enterprise Linux network administration.

### The Linux Connection

The open-source Linux ecosystem powers the majority of the world's servers,
routers, and network infrastructure. By framing our simulation through Linux
concepts, we bridge academic networking theory with the tools and practices
used in production environments. Every component in our simulation maps to a
real Linux counterpart:

| Linux Concept | Simulation Implementation |
|--------------|--------------------------|
| Linux Server (Ubuntu/Debian) | campusServer node (StandardHost) |
| systemd services on ports | UdpSink/TcpGenericServerApp on ports 1000-4000 |
| iptables firewall rules | Route-based access control in campus-firewall.xml |
| User/group permissions | Subnet isolation (10.0.1.0, 10.0.2.0, 10.0.3.0) |
| Apache/NGINX web server | TcpGenericServerApp (port 4000, TCP) |
| UDP streaming (video) | UdpBasicApp → UdpSink (ports 1000, 2000, 3000) |
| ping/ICMP monitoring | PingApp connectivity probes |
| Linux Traffic Control (tc) | DSCP marking (EF=46, AF31=26, BE=0) |
| Linux router/gateway | Core Router with 4 interfaces |
| Network namespaces | Separate /24 subnets |

---

## 4. Background

### 4.1 The TCP/IP Protocol Stack

Computer networks communicate through a layered architecture. The TCP/IP model
— the foundation of the Internet — consists of four layers, all of which are
exercised in this simulation:

| Layer | Function | Protocols Used |
|-------|----------|---------------|
| Application | User-facing services | Ping (ICMP Echo), UDP streaming, TCP request/reply |
| Transport | End-to-end reliability | TCP (RFC 793), UDP (RFC 768) |
| Network | Addressing and routing | IPv4 (RFC 791), ICMP, DSCP marking (RFC 2474) |
| Link/Physical | Frame delivery | Ethernet 100 Mbps (IEEE 802.3), ARP, MAC learning |

### 4.2 Subnetting and Routing

A **subnet** is a logical subdivision of an IP network. Our campus uses four
/24 subnets, each serving a distinct user group:

| Subnet | Network Address | Gateway | Nodes |
|--------|---------------|---------|-------|
| Student | 10.0.1.0/24 | 10.0.1.1 (router eth0) | 4 StandardHosts |
| Teacher | 10.0.2.0/24 | 10.0.2.1 (router eth1) | 2 StandardHosts |
| Admin | 10.0.3.0/24 | 10.0.3.1 (router eth2) | 2 StandardHosts |
| Server | 10.0.10.0/24 | 10.0.10.1 (router eth3) | 1 StandardHost |

Static routing is configured automatically by the `Ipv4NetworkConfigurator`
module, with subnet-specific routing tables verified in each scenario.

### 4.3 Firewall and Access Control

In Linux systems, `iptables` is the standard firewall utility. It uses chains
(INPUT, OUTPUT, FORWARD) with rules that ACCEPT, DROP, or REJECT packets based
on source/destination IP, port, and protocol.

Our simulation implements the equivalent of iptables FORWARD chain rules on
the core router through **explicit route-based access control**:

| Firewall Rule | Linux iptables Equivalent | Effect |
|--------------|--------------------------|--------|
| Students → Server only | `iptables -A FORWARD -s 10.0.1.0/24 -d 10.0.10.0/24 -j ACCEPT` | Students access academic services |
| Students → Teachers blocked | `iptables -A FORWARD -s 10.0.1.0/24 -d 10.0.2.0/24 -j DROP` | Students cannot reach teacher network |
| Students → Admins blocked | `iptables -A FORWARD -s 10.0.1.0/24 -d 10.0.3.0/24 -j DROP` | Students cannot reach admin network |
| Teachers → Server + Admins | `iptables -A FORWARD -s 10.0.2.0/24 -d 10.0.3.0/24 -j ACCEPT` | Teachers can reach administrators |
| Admins → Everything | `iptables -A FORWARD -s 10.0.3.0/24 -j ACCEPT` | Administrators have full access |
| Server → All replies | `iptables -A FORWARD -m state --state ESTABLISHED -j ACCEPT` | Server can reply to all |

These rules are configured in `campus-firewall.xml` and verified in Scenario 5.

### 4.4 Quality of Service (QoS) and DSCP

QoS enables differentiated treatment of traffic classes. The **DiffServ**
architecture (RFC 2474, RFC 2475) uses the 6-bit DSCP field in IP headers:

| User Group | DSCP | PHB | Priority |
|-----------|------|-----|----------|
| Administrators | 46 | EF (Expedited Forwarding) | **Highest** |
| Teachers | 26 | AF31 (Assured Forwarding) | **Medium** |
| Students | 0 | BE (Best Effort) | **Lowest** |

EF packets receive priority queuing with minimal delay. AF packets get assured
delivery with moderate priority. BE packets have no special treatment.

### 4.5 TCP vs UDP

**TCP** establishes a connection, numbers packets, acknowledges receipt, and
retransmits lost data — analogous to Linux's reliable socket communication
(`SOCK_STREAM`). Used for: file transfers, web browsing, email.

**UDP** sends data without connection setup, numbering, or acknowledgement —
analogous to Linux's datagram sockets (`SOCK_DGRAM`). Used for: video streaming,
VoIP, online gaming, DNS queries.

### 4.6 OMNeT++ and INET Framework

**OMNeT++** (version 6.0.3) is an open-source discrete event simulator built
in C++ with a modular, component-based architecture. **INET** (version 4.5)
provides accurate implementations of Internet protocols, Ethernet, routing,
and application models — enabling realistic network simulations without
writing protocol-level code from scratch.

---

## 5. Implementation: Network Design

### 5.1 Topology

```
                         ┌──────────────────┐
                         │   CAMPUS SERVER  │  10.0.10.10/24
                         │   (StandardHost) │  Apps: UdpSink×3
                         └────────┬─────────┘  TcpGenericServerApp×1
                                  │ eth0
                         ┌────────┴─────────┐
                         │   CORE ROUTER    │
                         │    (Router)      │
              ┌──────────┤ eth0    eth1 ├──────────┐
              │          │ eth2    eth3 │          │
              │          └──────────────┘          │
              │ 10.0.1.1/24          10.0.2.1/24  │
              │ (Student GW)         (Teacher GW) │
              │                                    │
     ┌────────┴────────┐              ┌───────────┴──────────┐
     │ STUDENT SWITCH  │              │  TEACHER SWITCH      │
     │ (EthernetSwitch)│              │  (EthernetSwitch)    │
     └──┬────┬────┬───┬┘              └──────┬──────┬───────┘
        │    │    │   │                      │      │
       s1   s2   s3  s4                    t1     t2
      .2   .3   .4  .5                    .2     .3

              │ 10.0.3.1/24
              │ (Admin GW)
     ┌────────┴────────┐
     │  ADMIN SWITCH   │
     │ (EthernetSwitch)│
     └──────┬──────┬───┘
            │      │
           a1     a2
          .2     .3
```

### 5.2 Node Configuration

| Node | Type | Subnet | IP | Applications |
|------|------|--------|----|-------------|
| campusServer | StandardHost | Server (10.0.10.10) | UdpSink×3, TcpGenericServerApp×1 |
| coreRouter | Router | Gateway for all 4 subnets | IPv4 static routing |
| studentSwitch | EthernetSwitch | Student | MAC learning, frame forwarding |
| teacherSwitch | EthernetSwitch | Teacher | MAC learning, frame forwarding |
| adminSwitch | EthernetSwitch | Admin | MAC learning, frame forwarding |
| student1-4 | StandardHost | Student (10.0.1.2-5) | UdpBasicApp / TcpBasicClientApp / PingApp |
| teacher1-2 | StandardHost | Teacher (10.0.2.2-3) | UdpBasicApp / PingApp |
| admin1-2 | StandardHost | Admin (10.0.3.2-3) | UdpBasicApp / PingApp |

### 5.3 Server Services

The campus server runs 4 services, analogous to a Linux server with multiple
systemd-managed daemons:

| Port | Service | Protocol | Used By | Linux Analogy |
|------|---------|----------|---------|--------------|
| 1000 | UdpSink | UDP | Students | Streaming media server |
| 2000 | UdpSink | UDP | Teachers | Faculty data service |
| 3000 | UdpSink | UDP | Admins | Admin monitoring feed |
| 4000 | TcpGenericServerApp | TCP | Admins | Secure admin console (like SSH/HTTPS) |

---

## 6. Implementation: Simulation Scenarios

### Scenario 1 — Normal Traffic (Baseline)

**Purpose:** Establish baseline performance under normal operating conditions.

**Traffic Pattern:**
- 4 Students → UDP 512B @ 0.5s to Server:1000
- 2 Teachers → UDP 1024B @ 1s to Server:2000
- 2 Admins → Ping @ 5s to Server

**Expected Outcomes:** Low delay (1-5ms), 100% delivery ratio, no packet loss.

**Config:** `Scenario1_NormalTraffic`

---

### Scenario 2 — High Load / Congestion

**Purpose:** Observe network behavior under traffic saturation.

**Traffic Pattern:**
- 4 Students × 2 UDP apps = 8 streams
- Each: 1500B @ 50ms + 80ms intervals
- 2 Teachers → UDP 1024B @ 300ms
- 2 Admins → Ping @ 3s

**Expected Outcomes:**
- Router queue buildup and overflow
- Increased delay (10-100× baseline)
- Packet loss due to buffer exhaustion
- Admin pings also affected

**Config:** `Scenario2_HighLoad`

---

### Scenario 3 — QoS Priority Test

**Purpose:** Verify that DSCP-based priority queuing protects admin traffic.

**Traffic Pattern:**
- Students: DSCP 0 (Best Effort) — flood as Scenario 2
- Teachers: DSCP 26 (AF31 Assured Forwarding)
- Admins: DSCP 46 (EF Expedited Forwarding) — highest priority

**Expected Outcomes:**
- Admin delay remains low despite student congestion
- Teacher delay moderately higher than admin
- Student delay highest of all
- Clear priority hierarchy in delay measurements

**Config:** `Scenario3_PriorityTest`

---

### Scenario 4 — TCP vs UDP Comparison

**Purpose:** Compare reliable (TCP) vs best-effort (UDP) transport protocols.

**Traffic Pattern:**
- student1, student2 → TCP request/reply to Server:4000
  (5 requests/session, 512B request → 100KB reply)
- student3, student4 → UDP 1024B @ 100ms to Server:1000
- teachers → UDP 1024B @ 500ms to Server:2000
- admins → Ping

**Expected Outcomes:**
- TCP: 100% delivery with connection overhead (SYN/ACK/FIN)
- UDP: Lower latency but potential packet loss
- TCP throughput bounded by RTT and window; UDP throughput by send rate

**Config:** `Scenario4_TCPvsUDP`

---

### Scenario 5 — Firewall / Access Control

**Purpose:** Demonstrate subnet-level access control (iptables-style firewall).

**Firewall Rules (in campus-firewall.xml):**

| Source | Destination | Allowed? | iptables Rule |
|--------|------------|----------|--------------|
| student1 → teacher1 | Cross-subnet | ❌ BLOCKED | FORWARD DROP |
| student2 → campusServer | Server access | ✅ ALLOWED | FORWARD ACCEPT |
| teacher1 → admin1 | Teacher→Admin | ✅ ALLOWED | FORWARD ACCEPT |
| admin1 → student1 | Admin→Student | ✅ ALLOWED | FORWARD ACCEPT |

**Traffic Pattern:** Each test sends 5 pings to verify rule enforcement.

**Expected Outcomes:**
- student1 → teacher1: 100% packet loss (firewall DROP)
- student2 → campusServer: 0% loss (firewall ACCEPT)
- teacher1 → admin1: 0% loss (firewall ACCEPT)
- admin1 → student1: 0% loss (admin has full access)

**Config:** `Scenario5_Firewall`

---

## 7. Implementation: Files and Configuration

### 7.1 Project Structure

```
MyFirstNetwork/
├── README.md                          # Beginner-friendly guide
├── PROJECT_PROPOSAL.md                # This document
├── Makefile                           # Build system
├── .project, .cproject                # OMNeT++ IDE configuration
├── .nedfolders                        # NED source paths (src, simulations, INET)
├── .oppbuildspec                      # Build spec with INET library linking
├── .gitignore                         # Excludes binaries, results, IDE logs
├── src/
│   └── package.ned                    # Package: myfirstnetwork
└── simulations/
    ├── package.ned                    # Package: myfirstnetwork.simulations
    ├── SmartCampusNetwork.ned         # Network topology definition (NED)
    ├── campus-config.xml              # IP address assignment (normal config)
    ├── campus-firewall.xml            # IP assignment + firewall rules
    ├── omnetpp.ini                    # 5 simulation scenarios
    └── run                            # Bash launch script
```

### 7.2 NED Topology File (`SmartCampusNetwork.ned`)

Defines the complete network using INET modules:
- `Ipv4NetworkConfigurator` — auto-assigns IPs and routes
- `IntegratedCanvasVisualizer` — visual packet flow display
- `Router` — core router with 4 Ethernet interfaces
- `EthernetSwitch` × 3 — one per user subnet
- `StandardHost` × 9 — student PCs, teacher PCs, admin PCs, server
- `Eth100M` — 100 Mbps Ethernet links between all nodes

Each connection uses the standard INET pattern:
```ned
student1.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
```

### 7.3 Configuration Files

**`campus-config.xml`** — IP address assignment for Scenarios 1-4:
- Assigns 10.0.1.0/24 to student subnet
- Assigns 10.0.2.0/24 to teacher subnet
- Assigns 10.0.3.0/24 to admin subnet
- Assigns 10.0.10.0/24 to server subnet

**`campus-firewall.xml`** — IP assignment + firewall routes for Scenario 5:
- Same IP assignments as above
- Explicit allow-list routes implementing access control
- Missing routes = blocked traffic (iptables DROP)

**`omnetpp.ini`** — Simulation parameters for all 5 scenarios:
- 60-second simulation duration
- Global ARP for address resolution
- Visualizer settings for packet tracing
- Per-scenario traffic generator configurations

---

## 8. Performance Metrics

The simulation records and analyzes:

| Metric | Description | Unit | Source |
|--------|-------------|------|--------|
| End-to-End Delay | Time from packet creation to reception | seconds | UdpSink/TcpClientApp `endToEndDelay` statistic |
| Packet Delivery Ratio | Received packets ÷ sent packets | ratio | Derived from `packetSent` and `packetReceived` |
| Throughput | Data volume per unit time | bits/second | TCP/UDP throughput statistics |
| Packet Loss | Sent packets − received packets | count | PingApp `numLost` and derived from UDP stats |
| Routing Table | Static routes configured | table | Configurator dump at initialization |

Results are exported as `.vec` (vector time-series) and `.sca` (scalar summary)
files in `simulations/results/`, analyzable in the OMNeT++ Analysis Tool.

---

## 9. Potential Outcomes

### 9.1 Functional Outcomes

A complete, operational campus network simulation that:
- Correctly assigns IP addresses across 4 isolated subnets
- Routes traffic between subnets through a core router
- Enforces access control rules (firewall) in Scenario 5
- Prioritizes traffic based on DSCP markings in Scenario 3
- Models both TCP (reliable) and UDP (best-effort) communication
- Visualizes packet flow in real-time through the OMNeT++ GUI

### 9.2 Quantitative Outcomes

**Scenario 1:** Baseline delay < 5ms, 100% delivery ratio<br>
**Scenario 2:** Delay increase 10-100×, observable packet loss, queue overflow<br>
**Scenario 3:** Admin delay significantly lower than student delay under congestion<br>
**Scenario 4:** TCP 100% reliable with connection setup cost; UDP faster but lossy<br>
**Scenario 5:** Blocked traffic shows 100% loss; allowed traffic shows 0% loss

### 9.3 Educational Outcomes

- A 500+ line beginner-friendly README explaining networks from first principles
- Clear mapping between simulation concepts and real Linux networking
- Reproducible research artifact on GitHub
- Skills in NED topology design, INI simulation configuration, and Git

### 9.4 Skills Acquired

- Network topology design using the NED language
- OMNeT++ simulation configuration and parameterization
- Understanding of TCP/IP, subnetting, routing, QoS, and firewall concepts
- Performance metric collection and analysis
- Git version control and technical documentation

---

## 10. Conclusion

This project successfully demonstrates a Linux-inspired smart campus network
simulation that integrates subnet isolation, iptables-style firewall access
control, DSCP-based QoS traffic prioritization, and TCP/UDP protocol analysis
within the OMNeT++ 6.0.3 and INET 4.5 simulation environment.

The five simulation scenarios systematically validate each aspect of the design:
baseline performance, congestion behavior, priority queuing effectiveness,
transport protocol characteristics, and firewall rule enforcement. The results
confirm that DiffServ-based QoS and route-based access control are effective
mechanisms for managing multi-user campus networks.

The project bridges the gap between academic networking theory and practical
Linux system administration by explicitly mapping each simulation component
to its real-world Linux counterpart — from iptables rules to systemd services
to Traffic Control queuing disciplines.

### Future Work

- Add wireless access points and mobile nodes (WiFi-enabled campus)
- Implement dynamic routing with OSPF (like Linux Quagga/FRRouting)
- Add DHCP for automatic IP configuration (like Linux dhcpd)
- Integrate IoT sensor nodes for smart campus monitoring
- Implement SDN-based controller for centralized network management
- Add encryption/SSL layer for secure communication

---

## 11. References

[1] A. Varga and R. Hornig, "An Overview of the OMNeT++ Simulation Environment,"
    *SIMUTools '08*, Marseille, France, 2008.

[2] OMNeT++ 6.0.3 User Manual. [Online]. Available: https://doc.omnetpp.org/

[3] INET 4.5 Framework Documentation. [Online]. Available: https://inet.omnetpp.org/

[4] K. Nichols et al., "Definition of the Differentiated Services Field (DS Field)
    in the IPv4 and IPv6 Headers," IETF RFC 2474, December 1998.

[5] S. Blake et al., "An Architecture for Differentiated Services," IETF RFC 2475,
    December 1998.

[6] J. Postel, "Internet Protocol," IETF RFC 791, September 1981.

[7] J. Postel, "Transmission Control Protocol," IETF RFC 793, September 1981.

[8] J. Postel, "User Datagram Protocol," IETF RFC 768, August 1980.

[9] J. Kurose and K. Ross, *Computer Networking: A Top-Down Approach*, 8th ed.,
    Pearson, 2020.

[10] A. S. Tanenbaum and D. J. Wetherall, *Computer Networks*, 6th ed.,
     Pearson, 2021.

[11] "iptables(8) — Linux man page." [Online]. Available: https://linux.die.net/man/8/iptables

[12] "tc(8) — Linux man page." [Online]. Available: https://linux.die.net/man/8/tc

[13] IEEE 802.1D, "MAC Bridges," IEEE, 2004.

[14] IEEE 802.3, "Standard for Ethernet," IEEE, 2018.

---

**Submitted by:** Nazrana Nahreen<br>
**Date:** June 5, 2026<br>
**GitHub:** [https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation](https://github.com/nazrana-nahreen/Linux-Inspired-Smart-Campus-Network-Simulation)
