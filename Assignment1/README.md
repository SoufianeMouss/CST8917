# Soufiane Mouss – Student 041182427  
**CST8917 – Serverless Applications**  
**Assignment 1: Serverless Computing – Critical Analysis**  

---

# Part 1: Paper Summary

## Main Argument

In *“Serverless Computing: One Step Forward, Two Steps Back”* (Hellerstein et al., 2019), the authors argue that first-generation serverless platforms, particularly Functions-as-a-Service (FaaS), represent meaningful progress in cloud computing but simultaneously reintroduce major limitations that cloud systems had previously overcome.

The “one step forward” refers to operational simplicity, automatic scaling, and pay-per-use billing. Developers no longer manage servers, capacity planning, or cluster orchestration. The “two steps back” refers to severe constraints imposed on execution time, networking, state management, and hardware access, which make serverless unsuitable for high-performance data processing and distributed systems innovation.

The authors claim that while FaaS is well-suited for event-driven, embarrassingly parallel tasks, it is fundamentally restrictive for stateful, data-intensive, and latency-sensitive applications.

---

## Key Limitations Identified

### 1. Execution Time Constraints

Early FaaS platforms imposed strict execution time limits (e.g., minutes per invocation). This makes them unsuitable for long-running analytics jobs, machine learning training, or complex distributed coordination workflows.

### 2. Communication and Network Limitations

FaaS platforms restrict direct function-to-function communication. Functions are not directly addressable and must communicate via storage services (e.g., object storage or queues). This creates I/O bottlenecks and significantly increases latency.

The authors argue that this design forces unnecessary serialization and deserialization overhead and prevents efficient distributed communication patterns.

### 3. The “Data Shipping” Anti-Pattern

Instead of moving computation close to data, FaaS encourages moving large volumes of data to stateless compute functions. This “data shipping” model is inefficient and costly, especially for big data and machine learning workloads.

The authors emphasize that high-performance systems traditionally move code to data, not data to code.

### 4. Limited Hardware Access

First-generation FaaS offerings did not allow access to GPUs or specialized hardware. This limits their usefulness for machine learning, scientific computing, and high-performance workloads.

### 5. Challenges for Distributed and Stateful Workloads

Because functions are stateless and short-lived, implementing distributed coordination (leader election, locking, consensus) becomes difficult. The authors argue that this discourages systems research and innovation within serverless environments.

---

## Proposed Future Directions

The authors propose a new cloud programming model with:

1. **Fluid code and data placement** – Allow computation to move to where the data resides.
2. **Support for heterogeneous hardware** – Including GPUs and specialized accelerators.
3. **Long-running, addressable virtual agents** – Instead of short-lived stateless functions.
4. **Support for disorderly/asynchronous programming models**.
5. **SLO-aware APIs and pricing models**.

They envision a more flexible, research-friendly cloud platform that preserves serverless simplicity without imposing restrictive execution constraints.

---

# Part 2: Azure Durable Functions Deep Dive

## 1. Orchestration Model

Azure Durable Functions extends Azure Functions by introducing orchestrator, activity, and client functions.

- **Client functions** start orchestrations.
- **Orchestrator functions** define workflows.
- **Activity functions** perform actual work.

Unlike basic FaaS, orchestrators coordinate multiple activities in sequence or parallel using normal programming constructs (loops, conditionals, error handling). This adds structured workflow control absent in traditional stateless functions.

This directly addresses the paper’s criticism that FaaS lacks support for complex distributed coordination.

---

## 2. State Management

Durable Functions use the **event sourcing pattern**. Every orchestration action is stored in persistent storage. When an orchestrator restarts, it replays execution history to reconstruct state.

This overcomes the stateless limitation identified in the paper. Orchestrations are durable and can survive crashes, restarts, and scaling events.

However, state is stored in external storage, meaning state management still depends on storage intermediaries.

---

## 3. Execution Timeouts

Orchestrator functions can run for days, months, or even indefinitely because their execution progress is checkpointed.

However, **activity functions remain subject to standard Azure Functions timeouts** (e.g., 10 minutes on the Consumption plan). Therefore, Durable Functions bypass timeout limitations at the workflow level but not at the individual compute level.

This partially addresses execution constraints but does not eliminate platform limits entirely.

---

## 4. Communication Between Functions

Orchestrator and activity functions communicate via queue messages stored in Azure Storage.

This still relies on storage intermediaries rather than direct networking. While the framework abstracts this complexity, the underlying architecture remains storage-based.

Thus, Durable Functions improve developer experience but do not fundamentally remove the I/O bottleneck described in the paper.

---

## 5. Parallel Execution (Fan-Out/Fan-In)

Durable Functions natively support fan-out/fan-in patterns using task aggregation APIs.

Multiple activity functions can execute in parallel, and the orchestrator automatically checkpoints and aggregates results.

This significantly improves distributed workflow coordination compared to raw FaaS. It reduces manual queue tracking and simplifies parallelism.

This capability directly addresses the paper’s concerns about difficulty implementing distributed workflows in FaaS.

---

# Part 3: Critical Evaluation

## Limitations That Remain Unresolved

### 1. Storage-Based Communication

Durable Functions still rely on Azure Storage queues and tables for orchestration history and messaging. This means communication latency and serialization overhead remain inherent to the design.

The paper criticizes FaaS for lacking direct function addressability and forcing communication through storage intermediaries. Durable Functions do not eliminate this architectural constraint—they abstract it.

### 2. Limited Hardware and Infrastructure Control

Durable Functions run on Azure Functions infrastructure. They do not provide native GPU access in the Consumption model or enable custom hardware control.

The paper emphasizes heterogeneous hardware support as a future requirement. Durable Functions do not solve this problem.

---

## My Verdict

Azure Durable Functions represent significant progress compared to first-generation FaaS platforms. They introduce:

- Durable state
- Long-running workflows
- Structured orchestration
- Built-in parallel patterns
- Fault tolerance via event sourcing

From a developer perspective, they meaningfully reduce complexity and enable stateful serverless applications.

However, they do not fundamentally change the underlying execution model. Communication still depends on storage. Activity functions still inherit timeout and infrastructure constraints. Hardware abstraction remains rigid.

Therefore, Durable Functions represent an **evolutionary improvement**, not the revolutionary shift envisioned by Hellerstein et al.

They successfully address developer ergonomics and workflow coordination but do not fully solve the deeper architectural limitations of serverless computing identified in the paper.

---

# References

Hellerstein, J. M., et al. (2019). *Serverless Computing: One Step Forward, Two Steps Back*. CIDR.  
https://www.cidrdb.org/cidr2019/papers/p119-hellerstein-cidr19.pdf

Microsoft Learn – Durable Functions Overview  
https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview

Microsoft Learn – Durable Orchestrations  
https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-orchestrations

Microsoft Learn – Performance and Scale in Durable Functions  
https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-perf-and-scale

---

# AI Disclosure Statemen
ChatGPT was used to assist with structuring the analysis, summarizing sections of the research paper.
