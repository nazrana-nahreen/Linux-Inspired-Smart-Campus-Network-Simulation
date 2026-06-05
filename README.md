# Linux-Inspired Smart Campus Network Simulation

## A Complete Beginner's Guide

---

# PART 0: WHAT EVEN IS THIS?

Imagine you want to build a real computer network for a university campus.
You would need to buy computers, switches, routers, cables, and then
configure everything. That costs lakhs of rupees and takes weeks.

**This project is a SIMULATION.** It's like a video game where we build
a virtual campus network on our computer. We can test how it behaves
without spending a single rupee on real hardware.

We are using a tool called **OMNeT++** (version 6.0.3). Think of OMNeT++
as a "network simulator game engine." It lets us:
- Place virtual computers (called "nodes") on a canvas
- Connect them with virtual cables
- Make them talk to each other
- Measure how fast and reliable the communication is

The add-on library we use is called **INET** (version 4.5). If OMNeT++
is the game engine, INET is the "DLC pack" that gives us ready-made
computer models, router models, and communication protocols.
Without INET, we would have to build every single piece from scratch —
like building a car starting from mining iron ore!

---

# PART 1: WHAT IS A NETWORK? (The Absolute Basics)

## 1.1 What is a Network?

A **network** is simply two or more computers connected together so they
can share information. That's it.

Think of it like a telephone system:
- Each computer is like a person with a phone
- The wires connecting them are like phone lines
- When computer A wants to talk to computer B, it "dials" B's number
  (in networking, this number is called an **IP address**)

## 1.2 What is a Topology?

**Topology = the MAP of how computers are connected.**

Just like a city has a map showing roads connecting buildings, a network
has a topology showing cables connecting computers. Our campus uses a
**Star Topology** — all computers in one group connect to a central
switch (like spokes on a wheel connecting to a hub).

### Our Campus Topology (The Map)

```
                    ┌──────────────────┐
                    │   CAMPUS SERVER  │  ← The main computer that
                    │  (10.0.10.10)    │     stores all the data
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │   CORE ROUTER    │  ← The "traffic police"
                    │  Four ports:     │     directing data between
                    │  eth0  eth1      │     different groups
                    │  eth2  eth3      │
                    └──┬────┬────┬─────┘
        ┌──────────────┼────┼────┼──────────────┐
        │              │    │    │              │
   ┌────┴────┐    ┌────┴────┐ ┌──┴──────┐       │
   │ STUDENT │    │ TEACHER │ │  ADMIN  │       │
   │ SWITCH  │    │ SWITCH  │ │  SWITCH │       │
   └─┬─┬─┬─┬─┘    └──┬──┬───┘ └──┬──┬───┘       │
     │ │ │ │         │  │        │  │           │
     s1 s2 s3 s4    t1 t2      a1 a2           │
                                                  │
                Groups of computers              │
              connected to switches              │
```

**Let's understand each piece:**

| Icon | Name | What It Does | Real-Life Analogy |
|------|------|-------------|-------------------|
| s1-s4 | Student PCs | 4 computers used by students | Laptops in a computer lab |
| t1-t2 | Teacher PCs | 2 computers used by teachers | Staff room computers |
| a1-a2 | Admin PCs | 2 computers used by administrators | Principal's office computer |
| Campus Server | Server | One powerful computer storing all data | The school's main database |
| Core Router | Router | Device that connects all 4 groups | Traffic police at a junction |
| Student Switch | Switch | Connects all 4 student PCs together | A power strip, but for network cables |
| Teacher Switch | Switch | Connects 2 teacher PCs together | Same as above |
| Admin Switch | Switch | Connects 2 admin PCs together | Same as above |

## 1.3 What is an IP Address?

An **IP address** is like a house address for computers.

Just like your house has "42, MG Road, Bangalore" so the postman knows
where to deliver letters, every computer has an IP address like
`10.0.1.5` so data packets know where to go.

In our simulation:
- **Student computers** have addresses like `10.0.1.2`, `10.0.1.3`, etc.
- **Teacher computers** have addresses like `10.0.2.2`, `10.0.2.3`
- **Admin computers** have addresses like `10.0.3.2`, `10.0.3.3`
- **Server** has address `10.0.10.10`

Notice the pattern:
- `10.0.1.x` → all in the Student group
- `10.0.2.x` → all in the Teacher group
- `10.0.3.x` → all in the Admin group
- `10.0.10.x` → all in the Server group

This grouping is called a **SUBNET** (short for "sub-network").
It's like dividing a school into different classrooms — students in
Room 101, teachers in Room 201, admin in Room 301.

The `/24` at the end (like `10.0.1.0/24`) means "all addresses that
start with `10.0.1` belong to this group." The `/24` is a technical
way of saying "the first 3 numbers are fixed, the last number can
vary from 1 to 254."

---

# PART 2: WHAT IS A PROTOCOL? (The Rules of Communication)

## 2.1 Protocols = The Language Computers Speak

When two humans talk, they need to agree on a language (English, Hindi,
Tamil, etc.) AND on rules (don't interrupt, take turns speaking, etc.).

**Protocols do the same for computers.** They are the RULES that
computers follow when communicating. Without protocols, one computer
might send data that the other computer doesn't understand — like
someone speaking Japanese to someone who only knows Spanish.

## 2.2 The Protocols We Use

### Internet Protocol (IP) — The "Postal Service"

```
[Your Computer]  ─── IP Packet ───>  [Server]
    10.0.1.2                             10.0.10.10
```

IP is the most basic protocol. It's like the postal service:
- It puts data in an "envelope" with a destination address
- It tries to deliver it
- But it does NOT guarantee delivery (letters can get lost!)
- It does NOT guarantee order (letter 2 might arrive before letter 1!)

In our simulation, IP is what the **Core Router** uses to move data
between different subnets. The router reads the destination IP address
and decides which path to send the packet on. This is called **routing**.

This is what the router's routing table looks like in our simulation:

```
Destination      Gateway          Which Port?
──────────────────────────────────────────────
10.0.1.0/24      *                eth0 (towards Student Switch)
10.0.2.0/24      *                eth1 (towards Teacher Switch)
10.0.3.0/24      *                eth2 (towards Admin Switch)
10.0.10.0/24     *                eth3 (towards Campus Server)
```

Translation: "If a packet is going to the 10.0.1.x area → send it out
port eth0. If going to 10.0.2.x area → send out port eth1. And so on."

The `*` means "I am directly connected to this network, no middleman needed."

For the student computers, their routing table is simpler:

```
Destination      Gateway          Which Port?
──────────────────────────────────────────────
10.0.1.0/24      *                eth0 (same subnet, direct delivery)
* (everything)   10.0.1.1         eth0 (send everything else to the router!)
```

The `*` in the destination means "default route" — "if I don't know
where to send this, give it to the router (10.0.1.1) and let it figure out."

### Transmission Control Protocol (TCP) — The "Registered Post"

```
Sender                          Receiver
  │────── SYN ──────>│  "Hello, can we talk?"
  │<──── SYN-ACK ────│  "Yes, I'm ready!"
  │────── ACK ──────>│  "Great, here's data #1"
  │────── DATA ─────>│  "Here's data #2"
  │<───── ACK ───────│  "Got data #2!"
  │────── DATA ─────>│  "Here's data #3" (lost!)
  │   ... waiting ... │
  │────── DATA ─────>│  "Re-sending data #3"
  │<───── ACK ───────│  "Got it!"
  │────── FIN ──────>│  "I'm done, goodbye!"
```

TCP is like Registered Post with Acknowledgement:
- It ESTABLISHES a connection first (like saying "hello" before talking)
- It NUMBERS every piece of data (so order is maintained)
- It CONFIRMS receipt of every piece (acknowledgement)
- If something is missing, it RESENDS it
- It's RELIABLE but slower

**Real-life example of TCP:** When you visit a website (HTTP), you need
every single piece of the page to load correctly. If even one image is
missing, it looks broken. So websites use TCP.

In our simulation (Scenario 4), students 1 and 2 use TCP to talk to the
server. This represents things like:
- A student submitting an assignment online
- A teacher uploading attendance records
- An admin downloading a report

### User Datagram Protocol (UDP) — The "Postcard"

```
Sender                          Receiver
  │────── DATA ─────>│  "Here's data!"
  │────── DATA ─────>│  "Here's more data!"
  │────── DATA ─────>│  (this one got lost, nobody knows)
  │────── DATA ─────>│  "Here's even more data!"
```

UDP is like sending a postcard:
- NO connection setup (just start sending)
- NO numbering of packets
- NO confirmation of receipt
- If something is lost, TOO BAD — nobody resends it
- It's FAST but unreliable

**Real-life example of UDP:** Video calls (Zoom, Google Meet). If one
tiny piece of the video is lost, you don't want the call to pause and
wait for it to be resent — you'd rather have a tiny glitch and keep going.
Also online games use UDP — you need split-second reactions, not perfect data.

In our simulation, students 3 and 4 use UDP. This represents:
- Streaming a lecture video
- Live attendance monitoring
- Real-time sensor data from lab equipment

### Internet Control Message Protocol (ICMP) — The "Are You There?"

ICMP is used by the **Ping** tool. It's like shouting "HELLO?" and
waiting for someone to shout back "I'M HERE!"

```
Admin PC                    Campus Server
  │──── Ping Request ────>│  "Are you alive?"
  │<─── Ping Reply ──────│  "Yes, I'm here! (took 5ms)"
```

Ping measures **Round Trip Time (RTT)** — how long it takes for a
message to go there and back. This is like measuring how long it takes
to hear an echo after you shout.

In our simulation, admin computers use Ping to check if the campus
server is reachable.

---

# PART 3: HOW OUR CAMPUS NETWORK IS DESIGNED

## 3.1 Why Separate Subnets?

We divided the campus into 4 groups (Student, Teacher, Admin, Server)
instead of putting everyone in one big network. Why?

**Reason 1: Security**
If everyone is in the same network, a student could potentially access
a teacher's private files or the admin's confidential data. By separating
them, we can control who can talk to whom. It's like having different
buildings with locked doors instead of one big open hall.

**Reason 2: Performance**
If all 1000+ students, teachers, and staff were in one network, every
single message would reach every single computer (this is called
"broadcast traffic"). It would be like 1000 people all talking at once
in a room — nobody can hear anything. Subnets reduce this noise.

**Reason 3: Organization**
Different groups have different needs:
- Students need lots of bandwidth (streaming, downloads)
- Teachers need reliable access to the server (attendance, grades)
- Admins need PRIORITY access (emergency notifications, system alerts)

Separate subnets let us give each group different rules.

## 3.2 The Role of Each Device

### Campus Server (10.0.10.10)
This is the heart of the campus. It runs 4 applications:

| Port | Application | Who Uses It | Purpose |
|------|------------|-------------|---------|
| 1000 | UdpSink | Students | Receives student data |
| 2000 | UdpSink | Teachers | Receives teacher data |
| 3000 | UdpSink | Admins | Receives admin data |
| 4000 | TcpGenericServerApp | Admins (TCP) | Reliable admin connections |

Think of "ports" like different counters at a bank:
- Counter 1000 → For students
- Counter 2000 → For teachers
- Counter 3000 → For admins
- Counter 4000 → For important admin work (TCP, more reliable)

The server "listens" on these ports, waiting for someone to send data.

### Core Router
The router has 4 network ports (eth0 through eth3), each connected to
a different group:

```
eth0 → Student Switch → 4 Student PCs
eth1 → Teacher Switch → 2 Teacher PCs
eth2 → Admin Switch   → 2 Admin PCs
eth3 → Campus Server   → 1 Server
```

The router's job:
1. Read every incoming packet's destination address
2. Look at its routing table to find the best path
3. Forward the packet out the correct port
4. If it doesn't know where to send it, drop the packet

In our simulation, the **Ipv4NetworkConfigurator** module automatically
sets up the routing tables for all devices. We don't have to manually
configure routes — it's all automatic, just like in a real network where
routers can auto-discover each other.

### Ethernet Switches
Each group has a switch. A switch connects all computers in that group.

```
Student Switch has 5 ports:
  Port 0 → student1
  Port 1 → student2
  Port 2 → student3
  Port 3 → student4
  Port 4 → Core Router (to reach other subnets)
```

A switch is smarter than a simple wire splitter. It LEARNS which
computer is connected to which port by watching the traffic.
When it receives a packet for `student3`, it knows to send it only
out port 2 — not to all ports. This is called **MAC address learning**.

### Student PCs (4 computers)
Each student PC runs a **UdpBasicApp** (or TcpBasicClientApp in Scenario 4).
This app generates data and sends it to the campus server.

In Scenario 1 (Normal Traffic):
```
Student1 sends: 512 bytes every ~0.5 seconds to Server:1000
Student2 sends: 512 bytes every ~0.5 seconds to Server:1000
Student3 sends: 512 bytes every ~0.5 seconds to Server:1000
Student4 sends: 512 bytes every ~0.5 seconds to Server:1000
```

In Scenario 2 (High Load), each student sends TWICE as much data,
TWICE as fast. This creates congestion — like a traffic jam on a highway.

### Teacher PCs (2 computers)
Teachers also send UDP data, but with larger packet sizes (1024 bytes)
and less frequently (every ~1 second). This represents things like
uploading documents or checking student records.

### Admin PCs (2 computers)
Admins use Ping in most scenarios to monitor network health.
In Scenario 3, admin1 switches to UDP with **high priority** marking.

## 3.3 How Data Actually Flows

Let's trace what happens when **student1 (10.0.1.2)** sends data to
the **campus server (10.0.10.10)**:

```
Step 1: student1 creates a UDP packet
        Destination: 10.0.10.10:1000
        Data: 512 bytes of student data

Step 2: student1 checks: "Is 10.0.10.10 in my subnet (10.0.1.0/24)?"
        Answer: No. 10.0.10.x is NOT in 10.0.1.x range.
        Action: Send to default gateway (the router at 10.0.1.1)

Step 3: The packet travels through the cable to the Student Switch.

Step 4: The Student Switch reads the MAC address.
        "This is for 0A-AA-00-00-00-01 (the router's MAC)"
        Forwards it out the port connected to the router.

Step 5: The Core Router receives it on eth0.
        "Destination is 10.0.10.10. Let me check my routing table...
        10.0.10.0/24 → eth3. Forward it out eth3!"

Step 6: The packet travels to the Campus Server.

Step 7: The Campus Server receives it.
        "This is for port 1000. UdpSink is listening on port 1000.
        Let me record this packet and its arrival time."

Step 8: The UdpSink records:
        - Packet received
        - End-to-end delay: (arrival time - send time)
        - Throughput: (total bytes received / time)
```

All of this happens in MILLISECONDS in the simulation.

---

# PART 4: THE 4 SIMULATION SCENARIOS

Each scenario is like a different "experiment" we run on our virtual
campus. We change the traffic patterns and observe what happens.

## Scenario 1: Normal Traffic (The Baseline)

**What we test:** How does the network perform under NORMAL conditions?

```
Students: 4 PCs × 512 bytes every 0.5 seconds → Server port 1000
Teachers: 2 PCs × 1024 bytes every 1 second → Server port 2000
Admins:   2 PCs × Ping every 5 seconds → Check if server is alive
```

**What to observe:**
- All packets should arrive (no loss)
- Delay should be low (~1-2 milliseconds)
- The network is "bored" — lots of unused capacity

**Why this matters:** This gives us a BASELINE. When we test under stress
(Scenario 2), we can compare against this to see how much worse things get.

## Scenario 2: High Load / Congestion (The Stress Test)

**What we test:** What happens when students flood the network?

```
Students: 4 PCs × 2 apps × 1500 bytes every ~0.05 seconds
          = 8 simultaneous high-speed streams!
Teachers: 2 PCs × 1024 bytes every 0.3 seconds
Admins:   2 PCs × Ping every 3 seconds
```

**What changes:**
- Each student now runs 2 UDP apps instead of 1
- Each app sends 1500 bytes (3× larger than normal)
- Each app sends every ~50ms (10× faster than normal)
- Total traffic is roughly 30× more than Scenario 1!

**What to observe:**
- The router's packet queue fills up
- Some packets get dropped (queue overflow)
- Delay increases (packets wait longer in queue)
- Admin pings might take longer or get lost

**Real-life parallel:** This is like what happens on a university WiFi
during exam registration — thousands of students hitting the server at
once, causing slowdowns or crashes.

## Scenario 3: Priority Traffic Test (QoS in Action)

**What we test:** Can we give admin traffic VIP treatment during congestion?

This introduces **QoS (Quality of Service)** — the network equivalent of
a "VIP pass" at an airport. We mark packets with different DSCP values:

| Group | DSCP Value | Meaning | Priority |
|-------|-----------|---------|----------|
| Students | 0 (BE = Best Effort) | "Send whenever, I'll wait" | LOWEST |
| Teachers | 26 (AF31 = Assured Forwarding) | "I'm somewhat important" | MEDIUM |
| Admins | 46 (EF = Expedited Forwarding) | "EMERGENCY! Let me through!" | HIGHEST |

**DSCP (Differentiated Services Code Point)** is a 6-bit field in every
IP packet header. It's like a stamp on a letter saying "URGENT" or
"NORMAL." Routers read this stamp and process URGENT packets first.

```
Without QoS (Scenario 2):
  Queue: [Student][Student][Student][Admin][Student][Teacher][Student]
  → Admin packet waits behind 3 student packets

With QoS (Scenario 3):
  Queue: [Admin][Teacher][Student][Student][Student][Student][Student]
  → Admin packet jumps to the front!
```

**What to observe:**
- Admin end-to-end delay should be MUCH lower than student delay
- Teacher delay should be lower than student delay but higher than admin
- The DSCP marking creates a clear "priority hierarchy"

**Real-life parallel:** In a hospital network, patient monitoring data
gets priority over YouTube streaming. In our campus, admin emergency
alerts get priority over student social media traffic.

## Scenario 4: TCP vs UDP (Protocol Comparison)

**What we test:** How does TCP (reliable) compare to UDP (fast)?

```
Student 1: TCP → Server:4000 (reliable, like HTTP/file download)
Student 2: TCP → Server:4000 (reliable, like HTTP/file download)
Student 3: UDP → Server:1000 (fast, like video streaming)
Student 4: UDP → Server:1000 (fast, like video streaming)
Teachers:  UDP → Server:2000 (moderate traffic)
Admins:    Ping (connectivity check)
```

**TCP pattern:** Student 1 and 2 use a REQUEST-REPLY pattern:
1. Open connection to server
2. Send ~5 requests per session, each 512 bytes
3. Wait for ~100KB reply from server
4. Wait ~100ms thinking time
5. Repeat

This is like browsing a website — small request (URL), large reply (webpage).

**UDP pattern:** Student 3 and 4 just blast data continuously without
any setup or confirmation.

**What to observe:**
- TCP: Higher reliability, but more overhead (connection setup, ACKs)
- UDP: Lower delay, but possible packet loss
- The `numActiveSessions` stat shows TCP connection lifecycle
- TCP throughput might be lower per-packet but guarantees delivery

---

# PART 5: THE FILES — WHAT DOES EACH ONE DO?

## Project Files (The Configuration)

### `.project` and `.cproject`
These are Eclipse IDE configuration files. They tell the OMNeT++ IDE
that this is a C++ simulation project and that it depends on INET.
You don't need to edit these manually — the IDE handles them.

### `.nedfolders` — Where to Find Building Blocks
```
src
simulations
../inet4.5/src
```

This tells OMNeT++ where to look for NED files (network description files).
Without the `../inet4.5/src` line, our project can't find the INET modules
like `StandardHost`, `Router`, etc.

### `.oppbuildspec` — How to Build
Tells `opp_makemake` (OMNeT++'s build tool) how to compile the project:
- `--deep`: Look in subdirectories for source files
- `-o MyFirstNetwork`: Name the output executable
- `--meta:use-exported-libs`: Link against INET's compiled library

### `Makefile` — Build Instructions
The top-level Makefile. Running `make makefiles` generates a detailed
Makefile in `src/`, then `make` compiles everything.

## Source Files (The Code)

### `src/package.ned` — Project Package Declaration
```
package myfirstnetwork;
```
Every OMNeT++ project lives in a "package" (like a Java package
or Python module). This declares ours as `myfirstnetwork`.

### `simulations/SmartCampusNetwork.ned` — THE NETWORK BLUEPRINT
This is the most important file. It defines our entire network topology
using INET's building blocks.

Let's understand it section by section:

```ned
package myfirstnetwork.simulations;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.ethernet.Eth100M;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;
```

**What this does:** The `import` statements are like `#include` in C or
`import` in Python. They tell OMNeT++ which pre-built components we want
to use from the INET library.

- `StandardHost` = A regular computer (with IP, TCP, UDP, apps)
- `Router` = A router (forwards packets between networks)
- `EthernetSwitch` = A network switch (connects computers in one group)
- `Eth100M` = A 100 Mbps Ethernet cable (the "wire" between devices)
- `Ipv4NetworkConfigurator` = Auto-configures IP addresses and routes
- `IntegratedCanvasVisualizer` = Shows the network visually in the GUI

```ned
network SmartCampusNetwork
{
    @display("bgb=1850,1250");
```

**What this does:** Declares our network. `@display` sets the canvas
size (1850×1250 pixels) — big enough to fit all our devices with
space between them.

```ned
    submodules:
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,50");
        }
        visualizer: IntegratedCanvasVisualizer {
            @display("p=100,150");
        }
```

**What this does:** Adds the auto-configurator and visualizer.
`@display("p=x,y")` sets where on the canvas each module appears.

```ned
        coreRouter: Router {
            @display("p=1000,600");
        }
```

**What this does:** Adds our core router. Position (1000, 600) is
roughly at the center-right of our canvas.

```ned
        studentSwitch: EthernetSwitch {
            @display("p=600,300");
        }
        student1: StandardHost {
            @display("p=200,150");
        }
        student2: StandardHost {
            @display("p=350,150");
        }
        // ... student3, student4 similar
```

**What this does:** Adds the Student Switch at (600, 300) and 4 student
computers arranged in a 2×2 grid on the left side.

```ned
    connections:
        student1.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        student2.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        // ... more connections
        studentSwitch.ethg++ <--> Eth100M <--> coreRouter.ethg++;
```

**Let me break down this syntax:**
- `student1.ethg++` = "use the next available Ethernet port on student1"
- `<-->` = bidirectional connection (data flows both ways)
- `Eth100M` = use a 100 Mbps Ethernet cable (the channel type)
- `studentSwitch.ethg++` = "use the next available Ethernet port on the switch"

The `++` means "increment the port count by 1." So if this is the first
connection, it uses port 0. Next connection uses port 1. And so on.

### `simulations/campus-config.xml` — Subnet & IP Address Assignment

```xml
<config>
    <interface hosts="coreRouter" names="eth0"
               address="10.0.1.1" netmask="255.255.255.0"/>
    <interface hosts="studentSwitch student?" names="eth*"
               address="10.0.1.x" netmask="255.255.255.0"/>
    ...
</config>
```

**What this does:** Tells the configurator how to assign IP addresses:
- Router port eth0 gets fixed address 10.0.1.1/24
- All student devices get addresses like 10.0.1.x/24 (x = 2, 3, 4, 5)
- Router port eth1 gets 10.0.2.1/24
- All teacher devices get 10.0.2.x/24
- And so on...

The `netmask="255.255.255.0"` means "the first 3 numbers are the
network address, the last number identifies individual computers."
This is the `/24` notation explained earlier.

### `simulations/omnetpp.ini` — Simulation Scenarios

This is the configuration file that controls every aspect of the
simulation. Let me explain each section.

```ini
[General]
network = myfirstnetwork.simulations.SmartCampusNetwork
sim-time-limit = 60s
```

**What this does:** These settings apply to ALL scenarios.
- `network` = which network topology to simulate
- `sim-time-limit` = stop after 60 simulated seconds

```ini
*.configurator.config = xmldoc("campus-config.xml")
```

**What this does:** Use our XML file for IP assignment.
`xmldoc()` means "read from an XML file."

```ini
*.*.ipv4.arp.typename = "GlobalArp"
```

**What this does:** Use Global ARP. ARP (Address Resolution Protocol)
converts IP addresses to MAC addresses. "Global" means the simulation
has a central ARP table instead of each device maintaining its own —
this is faster for simulation but wouldn't work in real life.

```ini
*.campusServer.numApps = 4
*.campusServer.app[0].typename = "UdpSink"
*.campusServer.app[0].localPort = 1000
```

**What this does:** Put 4 applications on the campus server.
- `app[0]` through `app[2]` are UdpSinks (UDP receivers) on ports 1000, 2000, 3000
- `app[3]` is a TcpGenericServerApp (TCP receiver) on port 4000

```ini
[Config Scenario1_NormalTraffic]
description = "Normal traffic - students and teachers accessing campus server"

*.student?.numApps = 1
*.student?.app[0].typename = "UdpBasicApp"
*.student?.app[0].destAddresses = "campusServer"
*.student?.app[0].destPort = 1000
*.student?.app[0].messageLength = 512B
*.student?.app[0].sendInterval = exponential(0.5s)
```

**What this does:** This is Scenario 1's configuration:
- `*.student?` matches student1, student2, student3, student4
  (the `?` matches exactly 1 character, so it WON'T match studentSwitch)
- Each student runs 1 UdpBasicApp
- They send to the campus server on port 1000
- Each message is 512 bytes
- Messages are sent with an interval that follows an exponential
  distribution with mean 0.5 seconds (this creates realistic, bursty
  traffic rather than perfectly spaced messages)

**Why exponential distribution?** In real networks, traffic is "bursty" —
sometimes a lot arrives at once, sometimes nothing for a while.
`exponential(0.5s)` creates this realistic pattern. On average, the
gap between messages is 0.5 seconds, but sometimes it's 0.1s and
sometimes it's 2s.

```ini
*.admin?.app[0].typename = "PingApp"
*.admin?.app[0].destAddr = "campusServer"
*.admin?.app[0].count = 10
```

**What this does:** Admin computers send 10 pings each to check connectivity.
Each ping measures: "How long does it take to reach the server and get a reply?"

### `simulations/run` — The Launch Script

This bash script handles finding the INET library and running the
simulation with the correct paths. You use it like:

```bash
./run -c ScenarioName -u Qtenv     # GUI mode
./run -c ScenarioName -u Cmdenv    # Command-line mode (faster)
```

---

# PART 6: PERFORMANCE METRICS — WHAT ARE WE MEASURING?

When the simulation runs, it records data. Here's what each metric means:

## End-to-End Delay
```
Delay = Time_packet_arrived_at_server - Time_packet_left_student_PC
```

**Unit:** seconds (or milliseconds)
**Good value:** < 10ms for a local network
**Bad value:** > 100ms (users notice lag)

**What affects it:**
- Congestion (packets waiting in router queues)
- Distance (in real networks; in simulation this is negligible)
- Processing time at each device

**In our scenarios:**
- Scenario 1: Delay should be very low (~1-2ms)
- Scenario 2: Delay increases as queues build up
- Scenario 3: Admin delay should stay low even when student delay rises

## Packet Delivery Ratio (PDR)
```
PDR = Number_of_packets_received / Number_of_packets_sent
```

**Good value:** 1.0 (100%) for TCP, close to 1.0 for UDP
**Bad value:** < 0.95 (more than 5% loss)

**What affects it:**
- Queue overflow at routers/switches
- Link errors (rare in simulation)
- Congestion

## Throughput
```
Throughput = Total_bytes_received / Time_duration
```

**Unit:** bits per second (bps), Kbps, Mbps
**What it tells us:** How much useful data is flowing through the network

**In our scenarios:**
- Scenario 1: Low throughput (light traffic)
- Scenario 2: High throughput but with packet loss
- Scenario 4: TCP might have lower throughput than UDP but guarantees delivery

## Packet Loss
```
Loss = Packets_sent - Packets_received
```

**What it tells us:** How many packets never made it to their destination.
In real networks, packet loss causes:
- Web pages loading slowly or incompletely
- Video calls freezing
- Online games lagging

---

# PART 7: HOW TO RUN THE SIMULATION

## Step 1: Open OMNeT++ Shell
Double-click **OMNeT++ 6.0.3 Shell** on your desktop.
A terminal window opens with the OMNeT++ environment ready.

## Step 2: Build INET (First Time Only)
```bash
cd samples/inet4.5
source setenv
make makefiles
make -j$(nproc)
```

`make -j$(nproc)` uses all CPU cores to compile faster.

## Step 3: Build Our Project
```bash
cd ../MyFirstNetwork
make makefiles
make -j$(nproc)
```

## Step 4: Run a Scenario
```bash
cd simulations
./run -c Scenario1_NormalTraffic -u Qtenv
```

This opens the OMNeT++ GUI:
- You'll see all 13 devices on the canvas
- Press the **Run** button (green play icon) to start
- Watch packets flow as colored arrows
- Press **Stop** when done

## Step 5: View Results
Results are saved in `simulations/results/`:
- `.vec` files = time-series data (delay over time, throughput over time)
- `.vci` files = vector index (helps OMNeT++ find data quickly)

Open these in the OMNeT++ IDE to create graphs.

---

# PART 8: REAL-WORLD APPLICATIONS

What we built is not just an academic exercise. The concepts map directly
to real networking:

| Our Simulation | Real-World Equivalent |
|---------------|----------------------|
| Student subnet | University computer lab VLAN |
| Teacher subnet | Faculty network with access to academic systems |
| Admin subnet | Management network with access to sensitive data |
| Core Router | Campus backbone router (Cisco/Juniper) |
| Campus Server | University web server / LMS (Moodle, Blackboard) |
| QoS / DSCP marking | Enterprise network traffic prioritization |
| UDP traffic | Video streaming, VoIP, online gaming |
| TCP traffic | Web browsing, file downloads, email |
| Ping monitoring | Network monitoring tools (Nagios, Zabbix) |

---

# PART 9: KEY TAKEAWAYS

1. **A network topology is a map** of how computers are connected.
   Our campus uses a star topology with 4 separate subnets.

2. **IP addresses are like house addresses** for computers.
   `10.0.1.5/24` means "house #5 on 10.0.1 street."

3. **Routers are traffic police** that direct data between different
   networks. Each router port connects to a different subnet.

4. **Switches are like power strips** — they connect multiple computers
   in the same group and learn which computer is on which port.

5. **TCP is reliable but slow** (like registered post with acknowledgement).
   Use it for file transfers, web pages, email.

6. **UDP is fast but unreliable** (like sending postcards).
   Use it for video calls, online games, live streaming.

7. **QoS gives VIP treatment** to important traffic. In our campus,
   admin emergency alerts get priority over student entertainment traffic.

8. **Congestion is like a traffic jam** — too many packets, not enough
   road capacity. Packets get delayed or dropped.

9. **Simulation lets us test without real hardware.** We can create
   scenarios that would be expensive or impossible to test in real life
   (like flooding a network with traffic until it breaks).

10. **Every number in the configuration has a meaning.** 512 bytes vs
    1500 bytes, 0.5 second vs 50 millisecond intervals, DSCP 0 vs 46 —
    each choice represents a real design decision about how the network
    should behave.
