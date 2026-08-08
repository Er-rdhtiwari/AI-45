# 6-Day Lead Software Engineer / VP Network Automation Study Plan

## Overall learning instructions for every day

Act as an experienced Senior/Staff/Principal Engineer and technical mentor.

Teach the material for **deep, reusable engineering understanding**, not for memorising interview answers.

For every important concept:

1. Explain it first in simple language.
2. Explain what problem it solves and why it exists.
3. Explain how it works technically.
4. Connect it to related concepts.
5. Give a simple practical example.
6. Explain important design trade-offs and failure modes where relevant.
7. Progress gradually from beginner understanding to Lead/Staff/VP engineering depth.

Use concise ASCII diagrams whenever they materially improve understanding.

Prefer examples from:

* Network automation
* Distributed systems
* Kubernetes
* Cloud platforms
* Enterprise infrastructure
* Banking/regulated systems
* Backend services

Avoid certification-style memorisation and unnecessary vendor-specific syntax.

Do not include:

* Interview questions or answers
* Mock interviews
* Interview do/don’t advice
* Revision checklists
* Daily checklists
* DSA
* Coding exercises
* Java preparation
* React/frontend preparation

The goal is to become a fundamentally stronger Lead/VP-level engineer whose knowledge remains useful beyond this specific role.

---
```
# DAY1 — Networking Foundations for Software and Platform Engineers

Act as a senior networking, cloud, backend, and distributed-systems mentor.

Today is Day 1.

## Goal

Build networking fundamentals from first principles so I can reason correctly about application communication, microservices, Kubernetes, cloud networking, enterprise networking, and network automation.

Do not assume that I am a network specialist.

---

## 1. What a computer network actually does

Explain:

* Host
* Client
* Server
* Network interface/NIC
* MAC address
* IP address
* Port
* Socket
* Packet
* Ethernet frame
* Connection
* Protocol
* Link
* Hop

Explain:

* Bandwidth
* Throughput
* Latency
* Jitter
* Packet loss

Clearly differentiate concepts that are commonly confused.

Use:

Browser → API → backend → database

to explain how communication happens across a network.

---

## 2. OSI and TCP/IP models

Explain the layers conceptually rather than as memorisation.

Cover:

* Physical
* Data link
* Network
* Transport
* Application

Place these correctly:

* Ethernet
* MAC
* ARP
* IP
* ICMP
* TCP
* UDP
* DNS
* HTTP
* HTTPS/TLS

Explain:

* Encapsulation
* Decapsulation
* Headers
* Payload

Include a concise ASCII packet-flow diagram.

---

## 3. Layer 2 networking

Explain:

* Ethernet
* Ethernet frames
* MAC addresses
* Switches
* MAC/CAM tables
* Unicast
* Broadcast
* Broadcast domains
* ARP
* ARP cache

Explain VLANs:

* Why VLANs exist
* Network segmentation
* Access ports
* Trunk ports
* 802.1Q concept
* VLAN IDs

Explain Layer-2 loops and why mechanisms such as STP exist at a conceptual level.

Use an office or data-centre example.

---

## 4. Layer 3 networking

Explain:

* IPv4 addressing
* Network portion vs host portion
* Subnet
* Subnet mask
* CIDR
* Default gateway
* Router
* Routing table
* Next hop
* Longest-prefix matching
* Default route

Use practical examples of:

* /16
* /24
* /30
* /32

Explain subnetting as an architecture concept rather than an exam calculation exercise.

Connect subnet design to:

* Enterprise networks
* Cloud VPC/VNet design
* Kubernetes
* Security segmentation

---

## 5. ICMP

Explain:

* What ICMP is
* Why networks need it
* Echo request/reply
* Destination unreachable
* Time exceeded

Explain conceptually how tools such as ping and traceroute use network behaviour without turning this into command memorisation.

---

## 6. TCP

Explain:

* Connection-oriented communication
* Three-way handshake
* Sequence numbers
* Acknowledgements
* Retransmission
* Ordering
* Flow control
* Congestion control at a conceptual level
* Connection close

Explain why backend/platform engineers care about:

* Connect timeout
* Read timeout
* Idle timeout
* Connection pooling
* Retries
* Broken connections

---

## 7. UDP

Explain:

* Connectionless communication
* Lack of built-in retransmission/ordering
* Lower overhead

Compare TCP and UDP.

Give examples of situations where UDP is useful.

---

## 8. MTU, MSS and fragmentation

Explain:

* MTU
* Why MTU exists
* Packet fragmentation concept
* Path MTU
* TCP MSS
* Problems caused by MTU mismatches

Connect this to:

* VPNs
* Overlays
* VXLAN
* Cloud networks

Keep packet-header details minimal.

---

## 9. DNS

Explain:

* Domain names
* DNS resolver
* Recursive resolver
* Root servers
* TLD servers
* Authoritative DNS

Cover:

* A
* AAAA
* CNAME
* TTL
* DNS caching

Show what happens when an application accesses:

`api.example.com`

Explain production issues caused by:

* Incorrect DNS
* Stale cache
* DNS outage
* Excessively long or short TTLs

---

## 10. DHCP

Explain:

* Why DHCP exists
* Dynamic IP allocation
* Address leases
* Gateway information
* DNS information

Explain its role in enterprise networks.

---

## 11. NAT

Explain:

* Private vs public IP addresses
* NAT
* SNAT
* DNAT
* Port address translation at a conceptual level

Connect NAT to:

* Enterprise internet connectivity
* Cloud networks
* Kubernetes
* Firewalls

---

## 12. Firewalls and ACL concepts

Explain:

* Network firewall
* Stateful firewall
* Stateless filtering
* Access-control lists
* Source
* Destination
* Protocol
* Port
* Ingress
* Egress

Explain:

* Network segmentation
* Security zones
* DMZ
* East-west vs north-south traffic

---

## 13. TLS from a network/application perspective

Explain:

* Plain HTTP vs HTTPS
* TLS purpose
* Encryption in transit
* Certificates
* Server identity
* High-level TLS handshake

Do not go deep into cryptographic algorithms.

---

## 14. Load balancers and proxies

Explain:

* Forward proxy
* Reverse proxy
* Load balancer
* Layer 4 load balancing
* Layer 7 load balancing
* Health checks
* TLS termination
* Session persistence
* Connection distribution

Connect this to microservices and Kubernetes.

---

## 15. QoS basics

Explain:

* Why all network traffic cannot always be treated equally
* Classification
* Prioritisation
* Queuing
* Shaping
* Policing

Use voice/video/business-critical traffic examples.

Keep detailed algorithms out.

---

## 16. LAN, WLAN, WAN, Internet and intranet

Clearly explain:

* LAN
* WLAN
* WAN
* Internet
* Intranet

Show how an enterprise might connect:

Office
→ WAN
→ data centre
→ cloud
→ Internet.

Include an ASCII diagram.

---

## 17. Physical networking vs cloud networking

Compare:

Physical:

* Switch
* Router
* Firewall
* Physical link

Cloud:

* VPC/VNet
* Subnet
* Route table
* Security group
* Network ACL
* Internet/NAT gateway
* Cloud load balancer

Explain which underlying networking principles remain unchanged.

---

## 18. Network failure reasoning

Teach how to reason conceptually about:

* Host failure
* Link failure
* Switch failure
* Router failure
* DNS failure
* Firewall blocking
* Routing problem
* Packet loss
* High latency
* MTU issue
* Connection timeout
* Service listening on wrong port

Use layered reasoning rather than troubleshooting-command lists.

---

## ASCII diagrams

Include diagrams for:

1. Application request across network layers
2. Basic switch/router/subnet topology
3. Enterprise office → data centre → cloud connectivity

Finish by tying Layer 2, Layer 3, transport, DNS, security and application communication together into one coherent mental model.

---

```
```
# DAY2 — Routing, Data-Centre Networking, VXLAN/EVPN, WAN and SD-WAN

Act as a senior enterprise, cloud, and data-centre network architect.

Today is Day 2.

## Goal

Understand how modern enterprise and data-centre networks are constructed and why technologies such as BGP, leaf-spine, VRF, MPLS, VXLAN, EVPN and SD-WAN exist.

Teach every technology through:

Problem → earlier solution → limitation → modern solution.

---

## 1. Routing fundamentals

Explain:

* Routing
* Routing table
* Route
* Prefix
* Next hop
* Metric
* Administrative preference concept
* Default route
* Static route
* Dynamic route
* Route convergence

Explain what happens when multiple routes could match a destination.

---

## 2. Dynamic routing

Explain why dynamic routing protocols exist.

Compare conceptually:

* OSPF
* BGP

Cover:

* Neighbour/peer
* Route advertisement
* Route learning
* Route withdrawal
* Path selection
* Convergence

Do not teach configuration commands.

---

## 3. OSPF

Explain:

* Purpose
* Link-state concept
* Internal routing
* Topology awareness
* Shortest-path calculation concept

Explain where OSPF is typically useful.

---

## 4. BGP

Explain:

* Autonomous System
* BGP peers
* eBGP
* iBGP
* Path advertisement
* Policy-driven routing
* Path attributes conceptually

Explain why BGP is important in:

* Internet routing
* Large enterprise networks
* Data-centre fabrics
* EVPN
* Cloud networking

---

## 5. ECMP and fast failure detection

Explain:

* Equal-Cost Multi-Path routing
* Using multiple network paths
* Load distribution
* Resilience

Explain BFD conceptually:

* Fast detection of failed network paths

Avoid protocol packet details.

---

## 6. Traditional data-centre architecture

Explain:

* Access
* Aggregation/distribution
* Core

Explain scaling and east-west traffic challenges.

---

## 7. Leaf-spine architecture

Explain:

* Leaf switches
* Spine switches
* East-west traffic
* North-south traffic
* ECMP
* Predictable hop count
* Horizontal scaling

Include an ASCII diagram.

Explain why leaf-spine became common in modern data centres.

---

## 8. Control plane, data plane and management plane

Clearly differentiate:

### Control plane

Learns topology and determines forwarding information.

### Data plane

Actually forwards packets.

### Management plane

Allows configuration, monitoring and administration.

Connect this distinction to network automation.

---

## 9. VRF

Explain:

* Virtual Routing and Forwarding
* Multiple isolated routing tables
* Tenant/network segmentation

Explain why VRFs are useful in:

* Enterprises
* Service providers
* Multi-tenant data centres

---

## 10. MPLS fundamentals

Explain at a high level:

* Why MPLS exists
* Label-based forwarding
* Enterprise/service-provider WAN use
* MPLS VPN concept

Do not teach label-stack internals.

Connect MPLS to traditional enterprise WANs.

---

## 11. Underlay and overlay networks

Explain deeply:

### Underlay

Physical/IP connectivity.

### Overlay

Logical connectivity built over that infrastructure.

Explain:

* Why separation is useful
* Operational benefits
* Scaling benefits

Use both analogy and technical example.

---

## 12. VLAN scaling limitations

Explain:

* VLAN segmentation
* VLAN ID space
* Large Layer-2 domains
* Broadcast/flooding
* Mobility
* Multi-tenancy
* Data-centre scale

Use these limitations to introduce VXLAN.

---

## 13. VXLAN

Explain:

* Why VXLAN exists
* VXLAN Network Identifier / VNI
* VTEP
* Tunnel
* Encapsulation
* Overlay
* IP underlay
* Layer-2-over-Layer-3 concept
* Multi-tenancy

Explain how VXLAN increases logical network scale.

Include an ASCII VTEP-to-VTEP diagram.

---

## 14. EVPN

Explain:

* Why an overlay needs endpoint reachability information
* EVPN as a control-plane approach
* MAC/IP advertisement
* BGP EVPN
* Reduced dependency on flooding

Keep individual EVPN route types high-level.

---

## 15. VXLAN + EVPN

Clearly differentiate:

VXLAN = data-plane encapsulation

EVPN = control-plane distribution of reachability information

Explain how they work together.

Walk through communication between workloads attached to different leaf switches.

Include an ASCII architecture.

---

## 16. Anycast concept

Explain:

* Multiple systems advertising/reaching the same logical address
* Traffic reaching an appropriate nearby/available instance

Give data-centre or DNS examples.

Keep routing internals high level.

---

## 17. WAN fundamentals

Explain:

* Branch connectivity
* Data-centre connectivity
* Long-distance network links
* Private circuits
* MPLS WAN
* Internet-based connectivity
* VPNs
* Redundant paths

---

## 18. VPN concepts

Explain conceptually:

* Site-to-site VPN
* Remote-access VPN
* Encrypted tunnel

Explain why overlays/tunnels are common across untrusted networks.

---

## 19. SD-WAN

Explain:

* Problems with traditional WAN management
* Centralised control
* Policy
* Application awareness
* Multiple transport options
* Dynamic path selection
* Central controller
* Resilience

Compare:

Traditional WAN vs SD-WAN.

Include an ASCII diagram.

---

## 20. WLAN fundamentals

Explain:

* Access point
* SSID
* Wireless controller
* Authentication
* Roaming
* Enterprise WLAN architecture

Keep radio-frequency theory minimal.

---

## 21. High availability

Explain:

* Device redundancy
* Link redundancy
* Multi-path routing
* Active/active
* Active/passive
* Failover
* Convergence
* ECMP

Explain the trade-off between greater resilience and increased complexity.

---

## 22. Hybrid and multi-cloud networking

Explain how an enterprise might connect:

* Offices
* Private data centres
* AWS
* Azure
* GCP
* SaaS
* Internet-facing services

Cover conceptually:

* Private connectivity
* Site-to-site VPN
* Dedicated cloud links
* Routing
* Segmentation
* Security boundaries
* Centralised vs distributed connectivity

Include one coherent ASCII enterprise architecture.

Finish by showing how routing, BGP, VRFs, MPLS, overlays, VXLAN/EVPN and SD-WAN fit into one mental model.

---

```
```
# DAY3 — Network Automation, APIs, Orchestration and Infrastructure as Code

Act as a senior network automation, distributed-systems, and infrastructure-platform architect.

Today is Day 3.

## Goal

Understand how large network estates are automated safely and reliably using software-engineering, distributed-system and declarative-infrastructure principles.

Treat network automation as a platform-engineering discipline, not merely scripting devices.

---

## 1. Evolution of network automation

Explain progression:

Manual CLI
→ scripts
→ reusable automation
→ workflow orchestration
→ declarative automation
→ policy/intent-driven automation
→ closed-loop automation.

Explain what problems each stage solves and what new complexity it introduces.

---

## 2. Core automation architecture

Explain components such as:

* Northbound API
* Authentication/authorization
* Inventory
* Source of truth
* IPAM
* CMDB integration
* Configuration repository
* Policy engine
* Workflow engine
* Scheduler
* Durable job queue
* Worker fleet
* Device adapters
* Controllers
* Audit store
* Telemetry pipeline

Include a detailed ASCII architecture.

---

## 3. Inventory, IPAM, CMDB and source of truth

Explain:

* Device inventory
* Sites
* Interfaces
* IP addresses
* Networks/subnets
* Ownership
* Software versions
* Device capabilities
* Topology
* Configuration intent

Explain:

* What makes a system authoritative
* Why duplicate/conflicting sources create risk
* Synchronisation between systems

---

## 4. Desired state and actual state

Explain:

* Declarative configuration
* Desired state
* Observed state
* Drift
* Reconciliation
* Convergence

Connect this to:

* Kubernetes controllers
* Infrastructure as Code
* Network automation

Include an ASCII reconciliation loop.

---

## 5. Idempotency

Explain idempotency deeply.

Compare:

"Ensure VLAN 100 exists"

with

"Create VLAN 100."

Explain importance for:

* Retries
* Workflow restarts
* Partial failure
* Automation recovery
* Repeated requests

---

## 6. Network-management interfaces

Compare conceptually:

* SSH/CLI
* SNMP
* NETCONF
* RESTCONF
* REST APIs
* gNMI

For each explain:

* Purpose
* Configuration vs telemetry use
* Structured vs unstructured interaction
* Strengths
* Limitations

---

## 7. Model-driven networking

Explain:

* Why structured data models matter
* YANG
* OpenConfig at a conceptual level
* Schema validation
* Device capability models

Explain how YANG relates to:

* NETCONF
* RESTCONF

and how OpenConfig/gNMI are used in modern environments.

---

## 8. Configuration templating

Explain:

* Template
* Variables
* Reusable configuration
* Environment/site-specific parameters

Explain dangers:

* Invalid assumptions
* Template drift
* Vendor differences
* Inadequate validation

---

## 9. Infrastructure as Code

Explain:

* Declarative infrastructure
* Version control
* Reproducibility
* Review
* Change history
* Automated validation

Connect IaC principles to networking.

---

## 10. GitOps

Explain:

* Git as desired-state source
* Pull-request-based change
* Reconciliation
* Automated deployment

Explain strengths and limitations of GitOps for network infrastructure.

---

## 11. Policy as Code

Explain:

* Expressing governance/security rules in machine-evaluable form
* Automated policy validation
* Guardrails
* Consistent enforcement

Give network-change examples.

---

## 12. Workflow orchestration

Design the lifecycle:

Request
→ validate
→ authorise
→ determine scope
→ pre-check
→ generate intended change
→ execute
→ verify
→ record result.

Explain:

* Workflow
* Step
* Dependency
* State
* Retry
* Compensation
* Pause/resume

Include an ASCII workflow.

---

## 13. Workflow state machines

Explain job states such as:

Pending
Running
Partially completed
Succeeded
Failed
Rolling back
Cancelled.

Explain why explicit state modelling is important in long-running automation.

---

## 14. Asynchronous job execution

Explain why network operations usually should not remain tied to an HTTP request.

Cover:

* Job ID
* Queue
* Worker
* Durable execution
* Status API
* Polling
* Events/callbacks

---

## 15. Queues and backpressure

Explain:

* Producer
* Consumer
* Queue depth
* Worker fleet
* Concurrency
* Rate limiting
* Backpressure

Explain what happens when incoming work exceeds processing capacity.

---

## 16. Failure handling

Explain:

* Retryable failure
* Permanent failure
* Timeout
* Device unavailable
* Partial success
* Worker crash
* Dependency outage
* Stale data

Explain:

* Exponential backoff
* Jitter
* Dead-letter handling
* Manual escalation
* Compensation
* Rollback

---

## 17. Exactly-once and deduplication

Explain why "exactly once" is difficult in distributed systems.

Teach practical approaches:

* At-least-once processing
* Idempotent operations
* Unique operation IDs
* Deduplication

Use network-change examples.

---

## 18. Concurrency and conflicting changes

Explain when two workflows touch the same device/resource.

Cover:

* Locks
* Leases
* Optimistic concurrency
* Version checking
* Compare-and-set idea
* Resource ownership

Explain trade-offs.

---

## 19. Transactions and compensation

Explain why a distributed network change across hundreds of devices cannot usually behave like one ACID database transaction.

Explain:

* Partial completion
* Compensating action
* Rollback
* Forward recovery

Connect this to saga-style thinking conceptually.

---

## 20. Safe rollout

Explain:

* Dry run
* Pre-check
* Canary
* Batch
* Progressive rollout
* Blast-radius limits
* Pause/resume
* Maintenance windows
* Automated rollback

---

## 21. Validation

### Pre-change

* Reachability
* Current state
* Device capability
* Dependency state
* Policy compliance
* Capacity

### Post-change

* Intended config applied
* Connectivity remains healthy
* Expected routes/state present
* Telemetry healthy

---

## 22. Topology and dependency awareness

Explain why changing one device can affect:

* Adjacent switches
* Routing peers
* Sites
* Applications
* Redundant paths

Explain how topology data improves safe automation.

---

## 23. Event-driven automation

Explain:

* Polling
* Events
* Webhooks
* Message brokers
* Streaming telemetry

Explain when reactive automation is useful.

---

## 24. Streaming telemetry

Explain:

* Traditional polling vs streamed state updates
* Near-real-time telemetry
* Metrics/state subscriptions
* gNMI/OpenConfig relationship conceptually

---

## 25. Closed-loop automation

Explain:

Observe
→ detect deviation
→ decide
→ change
→ verify
→ continue observing.

Discuss benefits and risks of autonomous remediation.

---

## 26. API architecture for automation

Explain:

* Resource-oriented APIs
* Synchronous vs asynchronous APIs
* Job endpoints
* Idempotency keys
* Pagination
* Filtering
* API versioning
* Error models
* Authentication/authorization

No code required.

---

## 27. Secrets and privileged access

Explain handling of:

* Device credentials
* API credentials
* SSH keys
* Certificates

Cover:

* Central secret stores
* Rotation
* Short-lived credentials
* Least privilege
* Auditability

---

## 28. Audit trail

Every infrastructure action should identify:

* Who
* What
* When
* Why
* Previous state
* Intended state
* Systems/devices affected
* Approval
* Result

Finish with a complete architecture for a safe enterprise network-automation platform.

---

```
```
# DAY4 — Kubernetes, Cloud, Distributed Platforms, CI/CD and Data

Act as a senior cloud-platform, Kubernetes, DevOps, and distributed-systems architect.

Today is Day 4.

## Goal

Understand how a highly available network-automation platform is built, deployed, scaled and operated across Kubernetes, private infrastructure and public cloud.

---

## 1. Runtime evolution

Explain:

Bare metal
→ virtual machines
→ containers.

Cover:

* Hypervisor
* VM
* Container
* Image
* Container runtime

Compare isolation, density, portability and operational complexity.

---

## 2. Kubernetes architecture

Explain:

### Control plane

* API server
* Scheduler
* Controller manager
* etcd

### Worker

* Node
* Kubelet
* Container runtime
* Pod

Include an ASCII architecture.

---

## 3. Kubernetes declarative model

Explain:

Desired state
→ API
→ controller
→ reconciliation
→ actual state.

Connect this directly to Day 3 network-automation reconciliation.

---

## 4. Kubernetes workloads

Explain:

* Pod
* ReplicaSet
* Deployment
* StatefulSet
* DaemonSet
* Job
* CronJob

Map these to:

* API service
* Network worker
* Telemetry collector
* Scheduled discovery
* Stateful infrastructure

---

## 5. Kubernetes networking

Explain:

* Pod networking
* Pod IP
* CNI concept
* Service
* ClusterIP
* NodePort concept
* LoadBalancer
* Ingress
* Egress
* DNS/service discovery
* NetworkPolicy

Connect these concepts to networking fundamentals from Days 1–2.

---

## 6. Kubernetes controllers and operators

Explain:

* Controller pattern
* Custom Resource Definition
* Operator

Explain why operators are useful for automating complex lifecycle management.

---

## 7. Configuration and secrets

Explain:

* ConfigMap
* Kubernetes Secret
* External secret manager
* Credential rotation
* Configuration separation

Explain why infrastructure platforms have high secret-management requirements.

---

## 8. Resource management and scheduling

Explain:

* CPU request
* CPU limit
* Memory request
* Memory limit
* Scheduling
* Resource pressure
* Eviction concept
* HPA

---

## 9. Health and lifecycle

Explain:

* Startup probe
* Readiness probe
* Liveness probe
* Graceful shutdown
* Rolling restart
* Pod disruption

---

## 10. Persistent storage

Explain:

* Stateless workloads
* Stateful workloads
* Persistent volume concept
* Storage class concept

Explain which network-automation components should remain stateless and which require durable state.

---

## 11. High availability

Explain HA for:

* API
* Workflow engine
* Workers
* Queue
* Database
* Cache
* Kubernetes control plane

Cover:

* Redundancy
* Replication
* Failure domains
* Availability zones

---

## 12. Distributed-system foundations

Explain:

* Stateless vs stateful
* Horizontal scaling
* Replication
* Partitioning
* Strong consistency
* Eventual consistency
* Durable messaging
* Distributed locking
* Leader election concept
* Failure isolation

Tie every concept to a practical platform example.

---

## 13. Data-store choices

Explain appropriate use of:

### Relational database

Inventory, workflows, audit metadata.

### NoSQL/key-value

Flexible/high-scale state where appropriate.

### Cache

Frequently accessed/temporary data.

### Object storage

Large immutable files/config snapshots.

### Search/index platform

Fast log/audit/document search.

Explain trade-offs rather than declaring one universally best.

---

## 14. Database engineering

Cover:

* Transactions
* Isolation concept
* Indexes
* Connection pools
* Optimistic locking
* Schema migrations
* Query scalability
* Pagination

---

## 15. Caching

Explain:

* Cache-aside
* TTL
* Invalidation
* Stale data
* Cache stampede concept

Explain what should and should not be cached in infrastructure automation.

---

## 16. CI/CD fundamentals

Explain:

Commit
→ build
→ test
→ scan
→ package
→ publish artifact
→ deploy
→ validate
→ promote.

Include an ASCII pipeline.

Explain principles common to:

* GitHub Actions
* Jenkins
* GitLab CI
* Tekton

without tool-specific syntax.

---

## 17. Software artifact management

Explain:

* Container registry
* Artifact immutability
* Versioning
* Provenance
* Environment promotion

---

## 18. Deployment strategies

Explain:

* Rolling
* Blue/green
* Canary
* Progressive delivery
* Rollback

Clearly distinguish:

Application deployment

from

Network configuration rollout.

---

## 19. Testing architecture

Explain:

* Unit
* Integration
* Component
* Contract
* End-to-end
* Infrastructure testing
* Failure testing
* Network-device simulators/mocks

Explain what each type proves.

---

## 20. TDD as an engineering discipline

Explain:

* Test first
* Small design feedback loops
* Behaviour specification
* Regression protection

Focus on design value rather than coding exercises.

---

## 21. Infrastructure as Code in platform deployment

Explain how IaC manages:

* Networks
* Kubernetes clusters
* Cloud resources
* Permissions
* Storage
* Databases

Connect to versioning and repeatability.

---

## 22. Public, private, hybrid and multi-cloud

Clearly explain:

* Public cloud
* Private cloud
* On-premises
* Hybrid cloud
* Multi-cloud

Explain why banks commonly operate hybrid environments.

---

## 23. Cloud conceptual mapping

Compare common constructs across AWS/Azure/GCP:

* Virtual network
* Subnet
* Compute
* Kubernetes
* IAM
* Object storage
* Load balancer
* Monitoring

Focus on portable architecture concepts.

---

## 24. Performance engineering

Explain:

* Latency
* Throughput
* CPU-bound
* I/O-bound
* Bottleneck
* Profiling
* Connection pooling
* Caching
* Batching
* Pagination
* Lazy loading
* Rate limiting
* Backpressure

Use network inventory/automation examples.

---

## 25. Data engineering fundamentals

Explain:

* ETL
* ELT
* Batch
* Streaming
* Data lake
* Data warehouse
* Operational database vs analytical database

Show:

Network devices
→ telemetry ingestion
→ raw storage
→ transform
→ warehouse
→ analytics.

Mention conceptually:

* Redshift
* BigQuery
* Snowflake

without product-specific detail.

---

## 26. Schema evolution and data quality

Explain:

* Changing event schemas
* Backward compatibility
* Validation
* Missing values
* Duplicate events
* Data-quality monitoring

Finish with one complete architecture for a highly available Kubernetes-based global network automation platform.

---

```
```
# DAY5 — SRE, Observability, Security, Risk, Controls and Resilience

Act as a senior SRE, security architect, technology-risk architect and platform-reliability engineer.

Today is Day 5.

## Goal

Understand how critical infrastructure platforms are made reliable, observable, secure, recoverable and governable.

---

## 1. Reliability vocabulary

Clearly differentiate:

* Availability
* Reliability
* Resilience
* Durability
* Fault tolerance
* Recoverability

Use practical examples.

---

## 2. Failure domains and blast radius

Explain failures at:

* Process
* Pod
* Node
* Cluster
* Database
* Queue
* Network
* Device
* Data centre
* Cloud region
* External dependency

Explain blast radius and failure containment.

---

## 3. SRE fundamentals

Explain:

* SLI
* SLO
* SLA
* Error budget

Use simple numerical examples where useful.

Explain why aiming for 100% availability can create poor engineering decisions.

---

## 4. Golden signals and service health

Explain:

* Latency
* Traffic
* Errors
* Saturation

Also introduce RED and USE approaches conceptually.

Explain when each mental model is useful.

---

## 5. Monitoring vs observability

Clearly explain the difference.

Then teach:

* Logs
* Metrics
* Traces

Include an ASCII telemetry flow.

---

## 6. Structured logging

Explain:

* Structured fields
* Severity
* Timestamp
* Correlation ID
* Trace ID
* Job/workflow ID
* Device ID
* Context propagation
* Redaction

---

## 7. Metrics

Explain:

* Counter
* Gauge
* Histogram
* Rate
* Percentile

Use metrics such as:

* Request rate
* API latency
* Queue depth
* Worker utilisation
* Automation success rate
* Device failure rate
* Rollback rate
* Drift count

---

## 8. Distributed tracing

Explain:

* Trace
* Span
* Parent/child span
* Trace context

Show a change request passing through:

API
→ workflow
→ queue
→ worker
→ device.

---

## 9. Observability ecosystem

Explain conceptual roles of:

* Prometheus
* Grafana
* Elasticsearch
* Logstash
* Kibana
* OpenTelemetry

Focus on integration rather than installation.

---

## 10. Alerting

Explain:

* Symptom-based alerts
* Thresholds
* Error-rate alerts
* Saturation alerts
* Deduplication
* Alert severity
* Alert fatigue
* Actionability

---

## 11. Incident lifecycle

Explain:

Detect
→ triage
→ contain
→ mitigate
→ recover
→ analyse
→ improve.

Cover:

* MTTR
* Root-cause analysis
* Post-incident review
* Corrective actions

---

## 12. Resilience patterns

Explain:

* Timeout
* Retry
* Exponential backoff
* Jitter
* Circuit breaker
* Bulkhead
* Rate limiter
* Backpressure
* Graceful degradation

Explain how retries can amplify an outage.

---

## 13. Capacity and saturation

Explain:

* Resource headroom
* Queue growth
* Connection limits
* Worker saturation
* Database saturation

Connect capacity problems to reliability.

---

## 14. Failure testing

Explain conceptually:

* Fault injection
* Chaos engineering
* Dependency failure simulation
* Recovery validation

Explain why controlled failure testing improves confidence.

---

## 15. Security principles

Explain:

* Confidentiality
* Integrity
* Availability
* Authentication
* Authorization
* Audit/accountability
* Least privilege
* Defence in depth
* Zero trust

---

## 16. Threat modelling

Explain:

* Asset
* Threat
* Attack surface
* Trust boundary
* Threat actor
* Mitigation

Use a network-automation platform example.

Introduce STRIDE only at a high level if useful.

---

## 17. OAuth2, OIDC and tokens

Explain:

OAuth2:
Authorisation delegation.

OIDC:
Authentication/identity layer.

Cover:

* Access token
* Refresh token
* Scope
* JWT concept

Avoid frontend implementation detail.

---

## 18. PKI, certificates and mTLS

Explain:

* Public/private key concept
* Certificate
* Certificate authority
* Trust chain
* TLS
* Mutual TLS
* Certificate rotation

Connect this to service-to-service communication and network devices.

---

## 19. Identity for machines

Explain:

* Service accounts
* Workload identity
* Short-lived credentials
* API keys
* Certificates

Explain why human credentials should not be embedded in automation.

---

## 20. Secure coding

Explain:

* Input validation
* SQL injection
* Command injection
* SSRF
* Path traversal
* XSS concept
* CSRF concept
* Secrets leakage
* Dependency vulnerabilities

Prioritise backend/infrastructure implications.

---

## 21. Kubernetes security

Explain:

* RBAC
* Service accounts
* NetworkPolicy
* Pod security
* Secrets
* Admission control
* Image security
* Least privilege

---

## 22. Software supply-chain security

Explain:

* Dependency scanning
* Image scanning
* SAST
* DAST concept
* SBOM
* Artifact signing
* Provenance
* Trusted registries

Explain why CI/CD itself is a security boundary.

---

## 23. Vulnerability management

Explain lifecycle:

Discover
→ assess severity
→ prioritise
→ remediate
→ verify
→ track exceptions.

---

## 24. Technology and operational risk

Explain:

Technology risk = possibility that technology failure, misuse, vulnerability or uncontrolled change harms the organisation.

Cover:

* Availability risk
* Cybersecurity risk
* Data risk
* Change risk
* Operational risk
* Third-party risk

---

## 25. Risk assessment

Explain conceptually:

* Likelihood
* Impact
* Inherent risk
* Mitigation
* Residual risk

Avoid excessive formal risk mathematics.

---

## 26. Controls

Explain:

### Preventive

Stop undesirable events.

### Detective

Discover undesirable events.

### Corrective

Restore/recover after events.

Use network automation examples.

---

## 27. Control design and effectiveness

Explain the difference between:

Having a control

and

Having an effective control.

Cover:

* Ownership
* Evidence
* Frequency
* Automation
* Exceptions

---

## 28. Change governance

Explain:

* Change request
* Peer review
* Risk classification
* Approval
* Segregation of duties
* Maintenance window
* Emergency change concept
* Validation
* Rollback
* Evidence

Explain how strong controls can coexist with fast engineering.

---

## 29. Auditability

Explain why critical actions require:

* Identity
* Timestamp
* Reason
* Approval
* Old state
* New state
* Execution outcome
* Evidence

---

## 30. Data protection

Explain:

* Data classification
* Encryption in transit
* Encryption at rest
* Key management
* Secret management
* Retention
* Redaction

---

## 31. Business continuity and disaster recovery

Explain:

* High availability vs disaster recovery
* Business continuity
* Backup
* Restore
* RTO
* RPO
* Regional failure
* Recovery procedures
* Recovery testing

---

## 32. Integrated safe-change architecture

Build one ASCII workflow:

Request
→ authenticate
→ authorise
→ validate
→ policy/control check
→ approve if required
→ execute progressively
→ observe
→ verify
→ audit
→ rollback/recover when necessary.

Finish by connecting reliability, security, observability and controls into one engineering model rather than treating them as separate disciplines.

---

```
```
# DAY6 — Lead/VP Engineering: Architecture, Strategy, Governance and Technical Leadership

Act as an experienced VP Engineering, Principal/Staff Engineer and enterprise platform architect.

Today is Day 6.

## Goal

Teach the engineering thinking needed to operate effectively at Lead/VP level: defining problems, making architectural decisions, setting technical direction, managing risk, aligning teams and owning platforms over many years.

This is a technical-leadership lesson, not behavioural interview preparation.

---

## 1. Engineering scope progression

Explain progression from:

Code
→ component
→ service
→ system
→ platform
→ organisation
→ enterprise.

Explain how responsibility changes as scope increases.

---

## 2. Lead/Staff/VP technical thinking

Contrast:

"How should I implement this?"

with:

* What problem should we solve?
* Who are the users?
* What constraints exist?
* Which risks matter?
* Which architecture fits?
* Who will operate it?
* How will it evolve?
* What does it cost?

---

## 3. Problem framing

Teach how to identify:

* Business problem
* User/operator problem
* Technical problem
* Constraints
* Dependencies
* Assumptions
* Unknowns

Explain why weak problem framing produces technically elegant but useless systems.

---

## 4. Requirements

Explain:

### Functional requirements

What the system does.

### Non-functional requirements

* Availability
* Scalability
* Security
* Performance
* Reliability
* Maintainability
* Operability
* Observability
* Auditability
* Cost
* Recoverability

Explain how NFRs drive architecture.

---

## 5. Technical strategy

Explain:

* Current state
* Desired state
* Guiding principles
* Capability gaps
* Constraints
* Architectural direction
* Migration path
* Investment priorities

Explain why technical strategy is not simply a technology list.

---

## 6. Strategy vs architecture vs roadmap

Clearly differentiate:

* Technical strategy
* Architecture
* Roadmap
* Project plan

Explain how they connect.

---

## 7. Architecture decision-making

Teach a structured way to evaluate alternatives using:

* Simplicity
* Reliability
* Scalability
* Security
* Performance
* Operability
* Team capability
* Cost
* Migration complexity
* Vendor dependency
* Reversibility

---

## 8. Architectural trade-offs

Use examples:

* Sync vs async
* SQL vs NoSQL
* Monolith vs microservices
* Build vs buy
* Managed vs self-managed
* Strong vs eventual consistency
* Centralised vs distributed control
* Fast change vs controlled change

Explain why there is rarely a universally correct architecture.

---

## 9. Architecture principles

Explain:

* High cohesion
* Loose coupling
* Encapsulation
* Clear ownership
* Stable interfaces
* Separation of concerns
* Failure isolation
* Idempotency
* Automation by default
* Security by design
* Observability by design

---

## 10. Domain and service boundaries

Explain:

* Bounded responsibility
* API ownership
* Data ownership
* Dependency direction
* Avoiding shared-database coupling

Use a platform example.

---

## 11. Evolutionary architecture

Explain:

* Incremental evolution
* Backward compatibility
* Versioning
* Strangler pattern
* Migration
* Deprecation
* Avoiding big-bang rewrites

---

## 12. Architecture runway

Explain the concept of creating enough foundational capability for future delivery without over-engineering everything upfront.

---

## 13. Platform engineering

Explain how a platform differs from a normal application.

Cover:

* Internal customers
* Self-service
* APIs
* Golden paths
* Reusable capabilities
* Standardisation
* Guardrails
* Developer/operator experience
* Product mindset

Connect this to network automation.

---

## 14. Build vs buy

Evaluate:

* Strategic differentiation
* Time to market
* Total cost
* Vendor maturity
* Integration
* Compliance
* Operational ownership
* Lock-in
* Exit strategy

---

## 15. Technical debt

Explain:

* Intentional debt
* Accidental debt
* Debt interest
* Delivery impact
* Risk
* Refactoring
* Modernisation

Explain when accepting technical debt can be rational.

---

## 16. Architecture governance

Explain healthy governance using:

* Principles
* Standards
* Architecture reviews
* Guardrails
* Exceptions
* Ownership
* Decision history

Explain how governance differs from bureaucracy.

---

## 17. Architecture Decision Records

Explain ADR structure:

* Context
* Decision
* Alternatives
* Consequences

Explain why long-lived systems benefit from decision history.

---

## 18. Standards and golden paths

Explain standards around:

* APIs
* Logging
* Security
* Deployment
* Observability
* Testing
* Reliability

Explain when standardisation improves productivity and when it can constrain innovation.

---

## 19. Risk-based engineering

Explain conceptually:

Risk ≈ likelihood × impact.

Teach:

* Identify risk
* Reduce likelihood
* Reduce impact
* Limit blast radius
* Detect failure
* Recover

Use network automation examples.

---

## 20. Engineering operating model

Explain:

* Ownership
* Decision rights
* Platform team
* Product/application teams
* SRE/operations
* Security
* Network engineering
* Governance

Explain how these groups collaborate without creating unclear responsibility.

---

## 21. RACI concept

Explain:

* Responsible
* Accountable
* Consulted
* Informed

Use it only as a lightweight responsibility model.

---

## 22. Cross-functional platform delivery

Explain dependencies across:

* Software engineering
* Network engineering
* Cloud
* SRE
* Security
* Data
* Operations
* Risk/governance

Explain interface ownership and dependency management.

---

## 23. Stakeholder thinking

Explain different priorities of:

* Engineers
* Architects
* Operations
* Security
* Risk
* Product
* Finance
* Business leadership

Explain how technical decisions affect each.

---

## 24. Influencing without direct authority

Explain:

* Credibility
* Evidence
* Shared outcomes
* Understanding incentives
* Technical negotiation
* Resolving disagreements
* Decision transparency

Keep this grounded in engineering work.

---

## 25. Communicating technical complexity

Take one network-automation reliability issue and show how it would be communicated differently to:

* Engineer
* Architect
* Operations
* Security/risk
* Senior business leader

---

## 26. Engineering quality as a system

Explain how leaders create quality through:

* Automated testing
* Code review
* Architecture review
* Documentation
* Standards
* CI/CD
* Observability
* Ownership
* Incident learning

Explain why quality should not depend on individual heroics.

---

## 27. Growing engineers

Explain:

* Delegation
* Technical coaching
* Design reviews
* Giving ownership
* Constructive feedback
* Knowledge sharing
* Developing specialists

Focus on engineering capability.

---

## 28. Long-term platform ownership

Explain responsibilities across:

* Build
* Deployment
* Operations
* Reliability
* Security
* Capacity
* Cost
* Upgrades
* Migration
* Deprecation
* End-of-life

---

## 29. Roadmapping and prioritisation

Explain how leaders balance:

* Business delivery
* Reliability
* Security
* Technical debt
* Platform improvements
* Migration
* Operational work

Explain why everything cannot be priority one.

---

## 30. Engineering economics

Explain:

* Engineering effort
* Infrastructure cost
* Operational cost
* Cost of complexity
* Cost of failure
* Total cost of ownership

Introduce:

* CapEx
* OpEx
* Cloud-cost awareness
* FinOps concept

at a practical level.

---

## 31. Capacity planning

Explain:

* Growth assumptions
* Peak demand
* Device count
* API traffic
* Automation-job volume
* Telemetry volume
* Storage growth
* Worker capacity

Connect forecasting assumptions to architecture.

---

## 32. Vendor and third-party engineering

Explain:

* Vendor dependency
* Supportability
* SLA
* Integration
* Security
* Data ownership
* Lock-in
* Exit strategy
* Third-party risk

Especially consider regulated enterprises.

---

## 33. Conway's Law

Explain how organisational communication structures influence software/system architecture.

Connect:

Team boundaries
→ ownership
→ service boundaries
→ communication patterns.

---

## 34. Regulated-enterprise architecture

Explain additional requirements around:

* Auditability
* Security
* Operational resilience
* Data protection
* Change governance
* Business continuity
* Third-party risk
* Evidence
* Accountability

---

## 35. Measuring platform success

Explain appropriate outcome measures such as:

* Adoption
* Reliability
* Deployment/change lead time
* Automation coverage
* Failure rate
* Recovery time
* Developer/operator productivity
* Cost efficiency

Explain why metrics should reflect outcomes, not vanity.

---

## 36. Final integrated case study

Finish with a detailed case study:

"Define the long-term architecture and engineering operating model for a global network automation platform."

Walk through:

Business need
→ users
→ requirements
→ NFRs
→ architecture
→ network integration
→ API/platform design
→ Kubernetes/cloud
→ data
→ security
→ reliability
→ controls
→ CI/CD
→ observability
→ ownership
→ operating model
→ cost
→ scaling
→ migration
→ long-term evolution.

Include one comprehensive but readable ASCII architecture.

Finish with a concise synthesis explaining how a strong Lead/VP engineer connects:

Technology

* architecture
* reliability
* security
* risk
* economics
* people
* long-term strategy

into one coherent engineering discipline.
```

```
# DAY 7 — Industry Capstone: Build and Operate a Global Network Automation Platform

Act as an experienced VP Engineering, Principal/Staff Engineer, enterprise platform architect, network-automation architect, SRE leader, security architect, and technology-risk leader working in a large global regulated bank.

Today is Day 7.

## Goal

Teach me the **complete real-world lifecycle of one major enterprise engineering initiative** by developing a realistic industry case study from beginning to end.

The case study should be inspired by the responsibilities of a Lead Software Engineer / VP working on global network automation in a Tier-1 bank such as Barclays.

Do NOT claim that the architecture represents Barclays' actual internal systems.

Instead, construct a realistic hypothetical scenario such as:

> "A global bank needs to replace fragmented manual and script-based network operations with a secure, highly available, auditable Network Automation Platform capable of managing tens of thousands of network devices across data centres, offices, private cloud, AWS/Azure/GCP and WAN/SD-WAN environments."

The purpose is to understand how a VP/Lead Engineer takes a large initiative through:

Business problem
→ requirements
→ discovery
→ architecture
→ detailed design
→ risk/security
→ implementation strategy
→ testing
→ deployment
→ production operation
→ incidents
→ improvement
→ scaling
→ long-term platform evolution.

This should read like a **real engineering project story**, not a textbook chapter and not an interview-preparation exercise.

---

# 1. Establish the Business Scenario

Create a realistic enterprise background.

The fictional bank should have:

* Multiple global data centres
* Large office/branch estate
* Private cloud
* AWS/Azure/GCP presence
* LAN/WLAN
* WAN/SD-WAN
* VXLAN/EVPN-based data-centre networks where appropriate
* Firewalls and network-security infrastructure
* Multiple network vendors
* Thousands or tens of thousands of devices
* Existing manual processes and legacy automation
* Strict availability requirements
* Regulatory and audit obligations
* Multiple engineering and operations teams

Explain how network changes are currently performed.

Show problems such as:

* Manual CLI changes
* Team-specific scripts
* Configuration drift
* Slow provisioning
* Inconsistent processes
* Human mistakes
* Poor audit evidence
* Limited standardisation
* Difficult rollback
* Fragmented inventory
* Conflicting sources of truth
* Limited visibility into change success
* Network incidents caused by change

Explain the business consequences.

Examples:

* Slow delivery of business services
* Increased operational cost
* Outages
* Security risk
* Audit difficulty
* Poor developer/operator experience
* Difficulty scaling cloud and data-centre infrastructure

---

# 2. Define the Actual Problem Before Designing Anything

Show how a Lead/VP Engineer separates:

### Business problems

### Network/operator problems

### Platform/software problems

### Security problems

### Risk/control problems

### Organisational problems

Identify:

* Assumptions
* Constraints
* Dependencies
* Unknowns
* Existing systems
* Legacy dependencies

Explain why jumping immediately to technology choices would be dangerous.

---

# 3. Identify Users and Stakeholders

Create realistic stakeholders such as:

* Network engineers
* Network operations
* Software/platform engineers
* SRE
* Cloud teams
* Security
* Cybersecurity
* Technology risk
* Change-management/governance teams
* Application teams
* Service owners
* Architecture
* Data/analytics teams
* Senior technology leadership
* Business leadership
* Vendors

Explain what each group cares about.

Show where their priorities conflict.

For example:

Network operations may prioritise safety.

Development teams may prioritise delivery speed.

Security may prioritise least privilege.

Business teams may prioritise faster provisioning.

Risk may prioritise evidence and controls.

Architecture may prioritise long-term standardisation.

Explain how the platform must balance these concerns.

---

# 4. Define Product and Platform Vision

Create a concise platform vision.

For example:

> Provide a secure, policy-driven, self-service automation platform that allows authorised teams to make validated network changes safely, consistently and audibly across the global network.

Then derive key capabilities.

Examples:

* Network inventory
* Source of truth
* IPAM integration
* CMDB integration
* Configuration management
* Discovery
* Compliance
* Change automation
* Workflow orchestration
* Policy validation
* Approval workflows
* Device communication
* Configuration backup
* Drift detection
* Automated remediation
* Telemetry
* Audit
* Reporting
* Self-service API
* Operator UI conceptually
* Integration APIs

Explain which capabilities belong in the first release and which can come later.

Teach the concept of:

MVP
→ production platform
→ mature platform.

---

# 5. Functional Requirements

Develop realistic functional requirements.

Examples:

* Discover network devices
* Maintain device inventory
* Read current configuration/state
* Create intended configuration
* Validate changes
* Submit change requests
* Run pre-checks
* Determine impacted devices
* Require approvals where policy demands them
* Execute changes asynchronously
* Track long-running jobs
* Support cancellation where safe
* Verify results
* Roll back failures
* Detect drift
* Store audit records
* Produce operational telemetry
* Provide APIs
* Integrate with enterprise systems

Explain how requirements are prioritised.

---

# 6. Non-Functional Requirements

Define realistic NFRs for a global bank.

Cover:

* Availability
* Reliability
* Scalability
* Performance
* Security
* Auditability
* Maintainability
* Observability
* Recoverability
* Disaster recovery
* Data durability
* Operability
* Extensibility
* Multi-vendor support
* Backward compatibility
* Compliance
* Cost

Use realistic illustrative targets where useful, while clearly identifying them as hypothetical.

Explain how NFRs affect architectural choices.

---

# 7. Domain Model

Define important platform entities.

For example:

* Device
* Site
* Interface
* Network
* Subnet
* VLAN
* VRF
* Configuration
* DesiredState
* ObservedState
* ChangeRequest
* Workflow
* Job
* Task
* Policy
* Approval
* Credential reference
* AuditEvent
* TelemetryEvent

Explain relationships between them.

Provide a simple ASCII domain model.

Do not write implementation code.

---

# 8. Source of Truth Architecture

Design the approach for:

* Device inventory
* IP addressing
* Network topology
* Device ownership
* Configuration intent
* CMDB information
* Device-discovered state

Explain:

Authoritative data
vs
Observed data.

Discuss what happens if:

CMDB says one thing
but
network discovery says another.

Explain reconciliation and data ownership.

---

# 9. High-Level Architecture

Design the complete platform.

Include components such as:

* API gateway
* Authentication
* Authorization
* Network Automation API
* Inventory service
* Source-of-truth integration
* Policy engine
* Workflow/orchestration engine
* Scheduler
* Durable queue/event bus
* Worker fleet
* Vendor/device adapters
* Network controllers
* Configuration/version repository
* Relational database
* Cache
* Object storage
* Audit store
* Telemetry pipeline
* Observability platform
* Secrets platform
* Notification/event integration
* Data/analytics pipeline

Show one comprehensive ASCII architecture.

Clearly identify:

### Control plane

### Execution plane

### Data plane/network devices

### Observability plane

### Security/control plane

Explain request and data flow.

---

# 10. End-to-End Change Flow

Pick one realistic example:

> "Deploy a routing-policy update to 2,000 network devices across several sites."

Walk through the complete lifecycle:

Business/service request
→ API request
→ authentication
→ authorization
→ schema validation
→ inventory lookup
→ topology/dependency analysis
→ policy validation
→ risk classification
→ approval decision
→ desired-state generation
→ pre-change validation
→ workflow creation
→ queueing
→ worker allocation
→ device communication
→ progressive rollout
→ post-change verification
→ telemetry validation
→ success/failure decision
→ audit evidence
→ notification.

Include a detailed ASCII sequence/workflow diagram.

This should become the central story that later sections build upon.

---

# 11. Device Integration Strategy

Explain communication with heterogeneous network infrastructure.

Compare:

* SSH/CLI
* NETCONF
* RESTCONF
* REST APIs
* gNMI
* SNMP
* Controllers/vendor APIs

Explain the adapter abstraction.

For example:

Automation Workflow
→ common device interface
→ Cisco adapter / Juniper adapter / controller adapter / cloud adapter.

Explain why vendor-specific behaviour should not spread throughout the platform.

Discuss:

* Device capabilities
* Version differences
* Unsupported features
* Schema/model differences

---

# 12. Model-Driven Networking

Show how:

* YANG
* OpenConfig
* NETCONF
* RESTCONF
* gNMI

could fit into the platform.

Explain why structured models improve:

* Validation
* Portability
* Automation safety
* Telemetry

Also explain why real enterprises may still need CLI/device-specific adapters.

---

# 13. Desired-State and Reconciliation Architecture

Show:

Desired state
→ observed state
→ compare
→ determine drift
→ reconcile
→ verify.

Connect this to Kubernetes reconciliation.

Explain:

* Safe automatic reconciliation
* Cases requiring human approval
* Cases where automatic remediation would be too risky

Include an ASCII loop.

---

# 14. Workflow and Distributed-System Design

Explain why network changes should be modelled as durable workflows.

Use states such as:

Pending
→ Validating
→ Awaiting Approval
→ Scheduled
→ Running
→ Verifying
→ Succeeded

and failure paths such as:

Failed
→ Rolling Back
→ Rolled Back

or:

Needs Manual Intervention.

Explain:

* State machines
* Durable execution
* Job IDs
* Task IDs
* Workflow recovery
* Worker failure
* Retry
* Compensation
* Cancellation
* Timeouts

---

# 15. Queue and Worker Architecture

Explain:

* Producer
* Durable queue
* Consumer
* Worker fleet
* Queue partitions/topics conceptually
* Device affinity if necessary
* Priority
* Backpressure
* Concurrency controls

Explain how the design scales from:

100 devices
to
10,000+ devices.

Discuss why unlimited concurrency could destroy network stability.

---

# 16. Idempotency and Delivery Semantics

Explain:

* At-least-once execution
* Duplicate delivery
* Idempotent operations
* Deduplication
* Operation IDs

Show how retries are made safe.

Explain why exactly-once execution is difficult.

Use real network-change examples.

---

# 17. Concurrency and Conflicting Changes

Create a realistic problem:

Two workflows attempt to update the same router simultaneously.

Explain possible solutions:

* Device lock
* Resource lock
* Lease
* Optimistic concurrency
* State version
* Conflict detection

Discuss trade-offs.

---

# 18. Partial Failure

Create a realistic scenario:

A change targets 1,000 devices.

* 850 succeed
* 100 are unreachable
* 30 reject configuration
* 20 fail post-validation

Explain how the system should behave.

Discuss:

* Retry
* Stop-the-line decision
* Rollback
* Forward recovery
* Manual intervention
* Dependency awareness
* Partial status
* Audit evidence

Explain why distributed infrastructure changes are not equivalent to one database transaction.

---

# 19. Safe Rollout Strategy

Design:

Dry run
→ canary
→ small batch
→ verify
→ larger batch
→ full rollout.

Explain:

* Blast radius
* Failure threshold
* Automatic pause
* Maintenance window
* Regional/site batching
* Device-role batching
* Rollback criteria

Explain how network topology changes rollout strategy.

---

# 20. Pre-Change Validation

Include:

* Device reachability
* Current state
* Configuration version
* Available capacity
* Redundancy health
* Routing peer health
* Device software compatibility
* Dependency checks
* Policy compliance
* Maintenance-window validation

Explain why "configuration is syntactically valid" is not sufficient.

---

# 21. Post-Change Verification

Verify:

* Intended configuration exists
* Routing relationships are healthy
* Expected routes exist
* Connectivity remains available
* Critical application paths remain healthy
* Error metrics have not increased
* Device telemetry is normal

Explain how automated verification increases confidence.

---

# 22. Security Architecture

Perform a practical threat-oriented design.

Cover:

### Human identity

* Enterprise SSO
* OIDC
* MFA concept
* RBAC

### Machine identity

* Service accounts
* Workload identity
* mTLS
* Short-lived credentials

### Device access

* Privileged credentials
* Vault/secret manager
* Certificate/key rotation

### Platform protections

* Network segmentation
* Least privilege
* API security
* Input validation
* Encryption
* Secrets management

Include trust boundaries in an ASCII security view.

---

# 23. Authorization Model

Design role examples such as:

* Read-only operator
* Network engineer
* Change requester
* Approver
* Platform administrator
* Security auditor

Explain:

RBAC

and where more contextual policy may be required.

For example:

A user may modify devices only in their region or service domain.

---

# 24. Risk Assessment

Identify major risks such as:

* Global misconfiguration
* Credential compromise
* Incorrect source-of-truth data
* Broken automation logic
* Queue overload
* Device/vendor incompatibility
* Network partition
* Failed rollback
* Insider misuse
* Platform outage
* Database corruption
* Third-party dependency failure

For each major category explain:

Risk
→ consequence
→ mitigation
→ remaining/residual risk.

Keep focus on engineering decisions rather than formal paperwork.

---

# 25. Preventive, Detective and Corrective Controls

Use the same platform to illustrate:

### Preventive controls

Examples:

* RBAC
* Peer review
* Policy validation
* Schema validation
* Change approval
* Canary rollout
* Concurrency limits

### Detective controls

Examples:

* Drift detection
* Alerts
* Audit review
* Post-change validation
* Security monitoring

### Corrective controls

Examples:

* Automated rollback
* Restore
* Credential rotation
* Incident procedures

Explain how controls become part of architecture rather than an external bureaucracy.

---

# 26. Segregation of Duties and Audit

Explain:

* Requester
* Approver
* Executor

and when separation matters.

Design an audit record capable of answering:

Who changed what?
Why?
When?
Which policy allowed it?
Who approved it?
What was the previous state?
What was executed?
What happened afterward?

---

# 27. Kubernetes Deployment Architecture

Deploy appropriate platform components on Kubernetes.

Map:

* APIs → Deployments
* Workers → Deployments
* Telemetry agents → DaemonSets where appropriate
* Scheduled discovery → CronJobs
* Stateful dependencies → managed/external services or appropriate StatefulSets depending on architecture

Explain:

* Services
* Ingress
* CNI
* NetworkPolicy
* ConfigMaps
* Secrets
* HPA
* Requests/limits
* Readiness/liveness
* Pod disruption
* Multi-AZ deployment

Include an ASCII Kubernetes deployment view.

---

# 28. Public/Private/Hybrid Cloud Decision

Assume the bank operates:

* On-premises/private DC
* Private cloud
* Public cloud

Discuss where automation components might run.

Explain considerations:

* Device reachability
* Security
* Latency
* Data sovereignty
* Resilience
* Cost
* Existing platform standards
* Connectivity dependencies

Avoid assuming "cloud is always best."

---

# 29. Data Architecture

Map data to suitable stores.

Examples:

### Relational DB

* Inventory metadata
* Workflows
* Jobs
* Approvals

### Cache

* Frequently accessed state

### Object storage

* Configuration snapshots
* Large artifacts

### Search platform

* Logs/audit search

### Analytics platform

* Long-term telemetry
* Operational trends
* Risk reporting

Explain why one database should not necessarily handle every workload.

---

# 30. Telemetry and Data Pipeline

Design:

Network devices
→ telemetry collectors
→ event/stream layer
→ operational monitoring
→ raw storage
→ transformation
→ analytical warehouse
→ dashboards/analytics.

Explain:

* Streaming vs batch
* Data quality
* Schema evolution
* Duplicate events
* Retention

Mention Redshift/BigQuery/Snowflake only as possible warehouse examples.

---

# 31. Observability Architecture

Define:

### Logs

### Metrics

### Traces

For the platform.

Define useful metrics such as:

* API latency
* Request rate
* Workflow duration
* Queue depth
* Worker utilisation
* Device connectivity failures
* Change success rate
* Post-check failure rate
* Rollback rate
* Drift count

Include correlation between:

API request ID
→ workflow ID
→ task ID
→ device ID
→ trace ID.

---

# 32. SLI/SLO Design

Define realistic hypothetical SLIs/SLOs for:

* API availability
* Workflow reliability
* Job-processing latency
* Telemetry ingestion
* Automation success

Explain why the platform cannot promise that every external network device is always available.

Separate:

Platform health

from

Device/network dependency health.

---

# 33. Alerting

Design alerts around symptoms rather than every internal event.

Explain:

* Severity
* Actionability
* Deduplication
* Alert fatigue

Show examples of good platform alerts.

---

# 34. CI/CD Architecture

Design:

Developer change
→ pull request
→ peer review
→ unit tests
→ integration tests
→ security/static analysis
→ dependency scan
→ container build
→ image scan
→ signing/provenance
→ registry
→ non-production deployment
→ automated validation
→ production promotion.

Include an ASCII pipeline.

---

# 35. Testing Strategy

Explain how to test the platform at multiple levels.

### Unit testing

### Integration testing

### Contract testing

### Workflow testing

### Device-adapter testing

### Network simulators/mocks

### End-to-end testing

### Failure testing

### Performance testing

### Security testing

### Disaster-recovery testing

Explain what each layer proves.

---

# 36. Production Release Strategy

Design the first production rollout.

Do not deploy globally immediately.

Explain progression such as:

Lab
→ development
→ test environment
→ limited production devices
→ one site/domain
→ broader rollout
→ global adoption.

Explain exit criteria based on evidence rather than dates alone.

---

# 37. Migration from Legacy Automation

Assume existing teams already have:

* Scripts
* Jenkins jobs
* Manual CLI procedures
* Vendor-specific tooling

Design a migration strategy.

Cover:

* Coexistence
* API adapters
* Gradual onboarding
* Capability parity
* Training
* Deprecation
* Avoiding big-bang replacement

Connect this to evolutionary architecture.

---

# 38. Production Incident Story

Create one detailed realistic incident.

Example:

A routing-policy automation release passes initial validation but causes unexpected route withdrawals in one region.

Walk through:

Detection
→ alert
→ incident declaration
→ containment
→ automation pause
→ rollback
→ network recovery
→ stakeholder communication
→ root-cause analysis.

Explain:

* Technical root cause
* Process/control contributors
* Why existing protections failed

Do not make the lesson simplistic.

---

# 39. Post-Incident Improvement

Show improvements after the incident.

Examples:

* Stronger pre-checks
* Topology-aware validation
* New canary rules
* Better change thresholds
* New telemetry
* Safer rollback
* Additional automated tests
* Improved policy checks

Explain how mature organisations convert incidents into engineering improvements.

---

# 40. Disaster-Recovery Scenario

Assume a primary hosting region/data centre becomes unavailable.

Explain:

* What continues working?
* What pauses?
* Where durable workflow state exists
* How the platform recovers
* RTO
* RPO
* Queue recovery
* Database recovery
* Secrets/certificate availability
* Preventing duplicate execution after failover

Explain why blindly resuming infrastructure changes after DR can be dangerous.

---

# 41. Capacity Planning

Assume growth from:

10,000
to
50,000 devices.

Estimate conceptually what changes.

Consider:

* API traffic
* Discovery jobs
* Concurrent changes
* Queue size
* Worker count
* Device limits
* Telemetry volume
* Database growth
* Audit retention
* Network connectivity

Explain which components scale horizontally and which become architectural bottlenecks.

---

# 42. Performance Optimisation

Create realistic performance issues.

Examples:

* Inventory API becomes slow
* Queue backlog grows
* Database queries degrade
* Device sessions consume too many resources
* Telemetry ingestion overwhelms storage

Explain possible solutions:

* Indexing
* Pagination
* Caching
* Batching
* Connection pooling
* Partitioning
* Horizontal scaling
* Backpressure
* Rate limiting

Always explain trade-offs.

---

# 43. Cost and Engineering Economics

Discuss:

* Compute
* Storage
* Telemetry retention
* Licences
* Network connectivity
* Engineering labour
* Operational support
* Vendor cost

Explain:

Total Cost of Ownership.

Show why the cheapest infrastructure component does not necessarily create the lowest total cost.

---

# 44. Build vs Buy Decisions

Choose several capabilities and reason about them.

Examples:

Build:

* Bank-specific network workflows
* Policy/integration layer

Potentially buy/use managed solutions for:

* Databases
* Observability
* Secrets
* Workflow technology
* Device controllers

Explain:

* Strategic differentiation
* Time
* Cost
* Supportability
* Lock-in
* Security
* Exit strategy

---

# 45. Team and Ownership Model

Design an operating model.

Possible groups:

* Network Automation Platform team
* Network-domain engineering teams
* SRE
* Security
* Cloud/platform
* Data
* Operations

Explain:

* Who owns the platform?
* Who owns network intent?
* Who owns individual automation workflows?
* Who responds to platform incidents?
* Who responds to device/network incidents?
* Who approves standards?

Avoid unclear shared ownership.

---

# 46. Platform as an Internal Product

Explain:

* Internal customers
* Self-service
* Documentation
* APIs
* Golden paths
* Reusable workflows
* Standardised integrations
* Guardrails
* Developer/operator experience

Explain how adoption is earned rather than forced.

---

# 47. Platform Success Metrics

Define meaningful metrics such as:

* Percentage of network changes automated
* Change lead time
* Change success rate
* Manual intervention rate
* Rollback rate
* Configuration drift
* Mean recovery time
* Platform availability
* Number of supported device families
* Operator productivity
* Adoption
* Cost per automated change

Distinguish outcome metrics from vanity metrics.

---

# 48. Technical Debt and Modernisation

After several years, introduce realistic issues:

* Old device adapters
* Deprecated APIs
* Growing database
* Duplicate workflows
* Legacy authentication
* Inconsistent schemas
* Vendor dependency

Explain how a VP/Lead Engineer prioritises modernisation without stopping business delivery.

---

# 49. Architecture Evolution Over Several Years

Show a realistic evolution.

### Stage 1

Basic orchestration and inventory.

### Stage 2

Standard APIs, multi-vendor adapters and stronger controls.

### Stage 3

Desired-state automation and drift detection.

### Stage 4

Policy-driven automation.

### Stage 5

Selective closed-loop remediation.

Explain why jumping directly to full autonomy would be risky.

---

# 50. Closed-Loop Automation

Build:

Telemetry
→ anomaly/deviation detection
→ decision
→ policy validation
→ automated remediation
→ verification.

Explain which changes could safely become autonomous.

Explain which changes should still require humans.

Discuss:

* Confidence
* Blast radius
* Explainability
* Safeguards
* Kill switch
* Audit

---

# 51. Architecture Governance

Explain:

* Architecture principles
* Technology standards
* ADRs
* API standards
* Security standards
* Exceptions
* Deprecation policies

Explain how governance enables consistency without becoming bureaucracy.

---

# 52. Major Architecture Decisions

Create several Architecture Decision Records conceptually.

Examples:

### Decision

Use asynchronous workflow execution rather than synchronous device changes.

### Decision

Separate desired state from observed state.

### Decision

Use vendor-adapter abstraction.

### Decision

Use progressive rollout as default.

### Decision

Use central identity and secrets platform.

For each give:

Context
→ options
→ decision
→ consequences.

---

# 53. VP-Level Decision Trade-Offs

Throughout the case study explicitly surface decisions involving:

* Speed vs safety
* Standardisation vs flexibility
* Build vs buy
* Centralisation vs team autonomy
* Availability vs cost
* Automation vs human control
* Strong consistency vs scalability
* Immediate delivery vs technical debt
* Platform capability vs product complexity

Explain why the selected answer may change as scale and maturity change.

---

# 54. Communication Across Different Audiences

Take one major architecture decision and explain how its communication differs for:

### Engineers

Technical details and constraints.

### Network operators

Operational workflow and safety.

### Security/risk teams

Threats and controls.

### Finance

Cost and economic impact.

### Senior leadership

Business outcome, risk and investment.

This is engineering leadership, not interview coaching.

---

# 55. Multi-Year Technical Roadmap

Create a realistic roadmap covering:

* Foundation
* Core automation
* Scale
* Standardisation
* Self-service
* Observability
* Policy-driven operation
* Selective closed-loop automation
* Legacy retirement

Explain dependencies between capabilities.

Avoid fake precision around dates.

---

# 56. Complete Project Story

Finish by retelling the entire case as one coherent engineering narrative.

Structure the narrative:

Initial business problem
→ discovery
→ requirements
→ design principles
→ architecture
→ important trade-offs
→ platform implementation
→ security and controls
→ network integration
→ CI/CD
→ testing
→ initial production rollout
→ adoption
→ production incident
→ lessons
→ scaling
→ governance
→ cost
→ organisational ownership
→ multi-year evolution.

The final narrative should feel like following one real enterprise system through its complete lifecycle.

---

# 57. Final End-to-End Architecture

Provide one final comprehensive but readable ASCII architecture showing:

Users / systems
│
▼
API / Self Service
│
Authentication + Authorization
│
Policy / Risk Controls
│
Workflow Orchestrator
│
Durable Queue
│
Worker Fleet
│
Device/Controller Adapters
│
Global Network

and supporting components:

* Inventory
* Source of Truth
* CMDB/IPAM
* Database
* Configuration repository
* Cache
* Secrets
* Audit
* Telemetry
* Observability
* Analytics
* CI/CD

Also indicate conceptually:

Data centre
Private cloud
Public cloud
WAN/SD-WAN
LAN/WLAN.

---

# 58. Final Lifecycle Flow

End with one concise ASCII lifecycle that connects everything:

Business Need
↓
Problem Framing
↓
Requirements + NFRs
↓
Risk / Constraints
↓
Architecture Options
↓
Architecture Decision
↓
Detailed Design
↓
Security + Controls
↓
Implementation
↓
Testing
↓
CI/CD
↓
Controlled Production Rollout
↓
Observability
↓
Operations
↓
Incident / Learning
↓
Improvement
↓
Scale
↓
Modernisation
↓
Long-Term Strategy

Explain how the responsibility of a Lead/VP Engineer spans this entire lifecycle rather than ending when development is complete.

---

# Teaching Requirements

Keep this Day 7 significantly more **story-driven and interconnected** than Days 1–6.

Do not teach every concept again from scratch.

Instead, reuse concepts from previous days and show how they interact in a real project.

Whenever an important architecture decision appears, explain:

Problem
→ constraints
→ available options
→ selected approach
→ why
→ trade-offs
→ failure implications.

Whenever an important production issue appears, explain:

What happened
→ why it happened
→ blast radius
→ detection
→ containment
→ recovery
→ permanent improvement.

Whenever a VP-level decision appears, connect:

Technical consequence

* operational consequence
* security/risk consequence
* business consequence
* long-term consequence.

Use simple language first, then move to Staff/Principal/VP-level depth.

Prefer realism over theoretical perfection.

Show that real enterprise systems contain:

* Legacy technology
* Organisational constraints
* Partial migrations
* Multiple vendors
* Conflicting requirements
* Failure
* Technical debt
* Budget limits
* Risk constraints

Do not present architecture as if unlimited money, people or time are available.

---

# Important Exclusions

Do NOT include:

* Interview questions
* Interview answers
* Mock interviews
* STAR stories
* Interview do/don’t advice
* Revision checklist
* Daily checklist
* DSA
* Coding exercises
* Java
* React/frontend preparation

This Day 7 is an **industry engineering capstone**.

Its purpose is to teach how an experienced Lead/Staff/Principal/VP Engineer understands, designs, delivers, operates, governs and evolves a mission-critical enterprise platform throughout its complete lifecycle.
```