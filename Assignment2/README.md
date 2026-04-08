# CST8917 – Assignment 2: Serverless Service Alternatives Report


## Quick Reference

| Azure Service | AWS Equivalent | GCP Equivalent |
|---|---|---|
| Azure Functions | AWS Lambda | Cloud Functions |
| Durable Functions | AWS Step Functions | GCP Workflows |
| Azure Logic Apps | AWS AppFlow + Step Functions | Application Integration |
| Azure Service Bus | Amazon SQS + SNS | Cloud Pub/Sub |
| Azure Event Grid | Amazon EventBridge | Eventarc |
| Azure Event Hubs | Amazon Kinesis Data Streams | Cloud Pub/Sub (Streaming) |

---

## 1. Azure Functions vs AWS Lambda vs GCP Cloud Functions

### Overview
All three are FaaS (Function-as-a-Service) platforms that run code in response to events without managing servers.

### Core Features

| Feature | Azure Functions | AWS Lambda | GCP Cloud Functions |
|---|---|---|---|
| **Languages** | C#, JS, Python, Java, PowerShell, Go | Node.js, Python, Java, Go, Ruby, .NET | Node.js, Python, Go, Java, Ruby, PHP |
| **Max Timeout** | 230s (Consumption); unlimited (Premium) | 15 minutes | 60 minutes (2nd gen) |
| **Triggers** | HTTP, Timer, Blob, Queue, Service Bus, Event Grid, Cosmos DB + declarative bindings | HTTP, S3, SQS, SNS, DynamoDB, EventBridge — SDK calls only | HTTP, Pub/Sub, Cloud Storage, Firestore, Eventarc |
| **Cold Start Fix** | Premium Plan (pre-warmed instances) | Provisioned Concurrency | Minimum instances |

### Integration Options
- **Azure Functions:** Azure DevOps, GitHub Actions, API Management, Logic Apps, Event Grid, Service Bus, Cosmos DB.
- **AWS Lambda:** API Gateway, S3, DynamoDB, SQS, Step Functions, CodePipeline, GitHub Actions.
- **GCP Cloud Functions:** Cloud Pub/Sub, Cloud Storage, Firebase, Cloud Run, Cloud Build.

### Monitoring & Observability

| | Azure Functions | AWS Lambda | GCP Cloud Functions |
|---|---|---|---|
| **Tool** | Application Insights + Azure Monitor | CloudWatch + X-Ray | Cloud Monitoring + Cloud Trace |
| **Logs** | Log Analytics | CloudWatch Logs | Cloud Logging |

### Pricing Model

| | Azure Functions | AWS Lambda | GCP Cloud Functions |
|---|---|---|---|
| **Free Tier** | 1M requests + 400K GB-s/month | 1M requests + 400K GB-s/month | 2M requests + 400K GB-s/month |
| **Per Request** | $0.20/million | $0.20/million | $0.40/million |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Azure Functions** | Declarative binding system reduces boilerplate; strong .NET support | Cold starts on Consumption plan; bindings have a learning curve |
| **AWS Lambda** | Most mature; largest community; Lambda Layers for shared dependencies | No native binding system; 15-min timeout limits long-running tasks |
| **GCP Cloud Functions** | Simplest to deploy; great for Firebase apps; generous free tier | Smaller trigger ecosystem; some enterprise features are newer |

---

## 2. Durable Functions vs AWS Step Functions vs GCP Workflows

### Overview
Stateful workflow orchestration services for chaining functions, fan-out/fan-in, and long-running processes.

### Core Features

| Feature | Durable Functions | AWS Step Functions | GCP Workflows |
|---|---|---|---|
| **Model** | Code-first (C#, Python, JS, Java) | JSON (Amazon States Language) | YAML-based |
| **Patterns** | Chaining, fan-out/fan-in, async HTTP, human interaction | Sequential, parallel, map, choice, callbacks | Sequential, parallel, conditional, subworkflows |
| **Max Duration** | Unlimited | Up to 1 year | Up to 1 year |
| **Visual Designer** | Limited | Full visual execution map | Basic view |

### Integration Options
- **Durable Functions:** Azure Functions ecosystem — Event Grid, Service Bus, HTTP, Cosmos DB, any Azure SDK.
- **Step Functions:** 200+ AWS services directly (Lambda, ECS, DynamoDB, SQS, Bedrock), EventBridge, API Gateway.
- **GCP Workflows:** GCP APIs, Cloud Run, Cloud Functions, any HTTP endpoint, Eventarc, Cloud Scheduler.

### Monitoring & Observability

| | Durable Functions | AWS Step Functions | GCP Workflows |
|---|---|---|---|
| **Tool** | Application Insights | CloudWatch + Step Functions console | Cloud Monitoring + Workflows console |
| **Execution History** | Azure Storage / App Insights | Visual execution map with live state | Executions console |

### Pricing Model

| | Durable Functions | AWS Step Functions | GCP Workflows |
|---|---|---|---|
| **Model** | Billed as Azure Functions — no extra cost layer | $0.025/1K state transitions (Standard) | $0.01/1K internal steps |
| **Free Tier** | Functions free tier applies | 4K transitions/month (Standard) | 5K steps/month |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Durable Functions** | Code-first is expressive and unit-testable; no extra billing layer | Replay-based model has non-determinism pitfalls; hard to visualize |
| **AWS Step Functions** | Best visual tooling; 200+ direct service integrations; mature | States Language JSON is verbose at scale; can get expensive |
| **GCP Workflows** | Simple YAML syntax; most cost-effective | Less expressive than code; smaller connector ecosystem |

---

## 3. Azure Logic Apps vs AWS AppFlow vs GCP Application Integration

### Overview
Low-code/no-code platforms for connecting SaaS apps, enterprise systems, and cloud services through visual workflow designers.

### Core Features

| Feature | Azure Logic Apps | AWS AppFlow | GCP Application Integration |
|---|---|---|---|
| **Connectors** | 400+ (Salesforce, SAP, Office 365, Dynamics, etc.) | 60+ (SaaS-to-AWS focused) | 65+ (GCP + enterprise SaaS) |
| **Triggers** | HTTP, Schedule, Service Bus, SaaS events | Schedule, on-demand, event-based | API, Pub/Sub, Scheduler, webhooks |
| **B2B / EDI** | Yes (AS2, X12, EDIFACT) | No | No |
| **Long-running** | Yes (stateful, multi-day) | Batch runs only | Yes (async) |

### Integration Options
- **Azure Logic Apps:** Microsoft ecosystem (Teams, SharePoint, Dynamics 365, Azure DevOps) + on-premises data gateway.
- **AWS AppFlow:** Moves SaaS data into AWS services — S3, Redshift, Salesforce, ServiceNow.
- **GCP Application Integration:** Apigee connectors, GCP services, enterprise SaaS via event triggers.

### Monitoring & Observability

| | Azure Logic Apps | AWS AppFlow | GCP Application Integration |
|---|---|---|---|
| **Tool** | Azure Monitor + visual run history per step | CloudWatch Logs | Cloud Logging |
| **Alerts** | Azure Alerts | CloudWatch Alarms | Cloud Alerting |

### Pricing Model

| | Azure Logic Apps | AWS AppFlow | GCP Application Integration |
|---|---|---|---|
| **Model** | ~$0.000025/action (Consumption) | ~$0.001–$0.10/flow run | Varies by connector tier |
| **Free Tier** | None | None | None |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Azure Logic Apps** | Most connectors (400+); only service with B2B/EDI support; stateful multi-day workflows | Costs can grow fast with high action volume; designer gets complex |
| **AWS AppFlow** | Great for bulk SaaS-to-AWS data movement; built-in field mapping | Not a general workflow tool; limited to data integration |
| **GCP Application Integration** | Modern designer; good for API-led integration with Apigee | Newer and less mature; smaller connector library |

---

## 4. Azure Service Bus vs Amazon SQS + SNS vs GCP Pub/Sub

### Overview
Managed messaging services for decoupled, asynchronous communication using queues and publish/subscribe patterns.

### Core Features

| Feature | Azure Service Bus | Amazon SQS + SNS | GCP Pub/Sub |
|---|---|---|---|
| **Queue + Pub/Sub** | Unified service | Two separate services | Unified service |
| **Message Size** | Up to 100 MB (Premium) | 256 KB | 10 MB |
| **Retention** | Up to 14 days | Up to 14 days | Up to 31 days |
| **Ordering** | Sessions (strict FIFO per key) | SQS FIFO queues | Ordering keys |
| **Transactions** | Yes | No | No |
| **Dead-letter** | Built-in per queue/subscription | Manual setup | Configurable dead-letter topic |
| **Protocol** | AMQP 1.0, HTTPS | HTTPS/REST | gRPC, HTTPS |

### Integration Options
- **Azure Service Bus:** Native trigger/binding in Azure Functions; Logic Apps, Event Grid, AKS, on-premises via Service Bus Relay.
- **Amazon SQS + SNS:** Lambda trigger, EC2, ECS, EventBridge; SQS Extended Client for large messages via S3.
- **GCP Pub/Sub:** Cloud Functions, Cloud Run, Dataflow, BigQuery subscriptions, Eventarc, Workflows.

### Monitoring & Observability

| | Azure Service Bus | Amazon SQS + SNS | GCP Pub/Sub |
|---|---|---|---|
| **Tool** | Azure Monitor (message count, DLQ depth) | CloudWatch (queue depth, age of message) | Cloud Monitoring (backlog, oldest message age) |
| **Logs** | Azure Diagnostic Logs → Log Analytics | CloudWatch Logs (via consumer) | Cloud Audit Logs |

### Pricing Model

| | Azure Service Bus | Amazon SQS | GCP Pub/Sub |
|---|---|---|---|
| **Free Tier** | None | 1M requests/month | 10 GB/month |
| **Per Operation** | From $0.05/million (Basic) | $0.40/million (Standard) | $0.04/GB after free tier |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Azure Service Bus** | Best enterprise features — sessions, transactions, AMQP 1.0, geo-DR | No free tier; more complex than simpler queue services |
| **Amazon SQS + SNS** | Most widely used; generous free tier; battle-tested at scale | Two separate services to connect; 256 KB message size limit |
| **GCP Pub/Sub** | Auto-scaling; no capacity planning; large 10 MB message size | No transaction support; no true global FIFO |

---

## 5. Azure Event Grid vs Amazon EventBridge vs GCP Eventarc

### Overview
Event routing services that filter and forward discrete events from cloud services, SaaS, or custom sources to downstream handlers.

### Core Features

| Feature | Azure Event Grid | Amazon EventBridge | GCP Eventarc |
|---|---|---|---|
| **Event Sources** | Azure services, custom topics, partner events | 150+ AWS services, 30+ SaaS partners, custom | 100+ GCP services, Pub/Sub, Cloud Audit Logs |
| **Schema** | CloudEvents 1.0 + Event Grid schema | EventBridge JSON | CloudEvents 1.0 |
| **Filtering** | Subject, event type, advanced filters | JSON pattern matching (content-based) | Event type, resource-based |
| **Event Replay** | No | Yes (from archive) | No |
| **Schema Registry** | Yes | Yes (with code binding generation) | No |
| **Targets** | Functions, Logic Apps, Service Bus, webhooks | Lambda, SQS, SNS, Step Functions, HTTP | Cloud Run, Cloud Functions (2nd gen) |

### Integration Options
- **Azure Event Grid:** Azure Functions, Logic Apps, Service Bus, Event Hubs, Azure Relay, webhooks — core of reactive Azure architecture.
- **Amazon EventBridge:** Lambda, Step Functions, SQS, SNS, Kinesis, API Gateway, 3rd-party SaaS via API Destinations.
- **GCP Eventarc:** Cloud Run, Cloud Functions (2nd gen), Cloud Audit Logs for compliance-driven automation.

### Monitoring & Observability

| | Azure Event Grid | Amazon EventBridge | GCP Eventarc |
|---|---|---|---|
| **Tool** | Azure Monitor (delivery count, failed deliveries) | CloudWatch (invocations, failed events) | Cloud Monitoring (trigger invocations) |
| **Failed Events** | DLQ + retry policies | DLQ via SQS | DLQ via Pub/Sub |

### Pricing Model

| | Azure Event Grid | Amazon EventBridge | GCP Eventarc |
|---|---|---|---|
| **Free Tier** | 100K operations/month | 14M events/month (from AWS services) | Billed via Pub/Sub + destination |
| **Per Event** | $0.60/million | $1.00/million (custom/partner) | $0.04/GB via Pub/Sub |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Azure Event Grid** | Deep Azure resource event integration; CloudEvents support; Event Grid Domains for multi-tenant | No event replay; less expressive filtering than EventBridge |
| **Amazon EventBridge** | Best content-based filtering; event replay from archive; schema registry with code generation | Highest per-event cost; can get complex at scale |
| **GCP Eventarc** | Native CloudEvents 1.0; good for audit-log-driven automation | Fewest target options; no replay or schema registry; still maturing |

---

## 6. Azure Event Hubs vs Amazon Kinesis vs GCP Pub/Sub (Streaming)

### Overview
High-throughput streaming platforms designed to ingest millions of events per second from telemetry, logs, and real-time data pipelines.

### Core Features

| Feature | Azure Event Hubs | Amazon Kinesis Data Streams | GCP Pub/Sub (Streaming) |
|---|---|---|---|
| **Kafka Compatible** | Yes | No | No |
| **Scaling Model** | Throughput Units / Processing Units | Manual shard management | Fully automatic |
| **Retention** | Up to 90 days | Up to 365 days | Up to 31 days |
| **Capture / Export** | Event Hubs Capture → Blob / ADLS | Kinesis Firehose → S3, Redshift | BigQuery subscription, Dataflow |
| **Stream Processing** | Stream Analytics, Databricks, Flink | Kinesis Analytics (Flink/SQL), Lambda | Dataflow (Apache Beam) |
| **Schema Registry** | Yes (Avro, JSON Schema) | AWS Glue Schema Registry | Basic Pub/Sub schemas |

### Integration Options
- **Azure Event Hubs:** Stream Analytics, Azure Databricks, Azure Synapse, Azure Functions, Kafka-compatible workloads.
- **Amazon Kinesis:** Kinesis Analytics, Lambda, Kinesis Firehose, AWS Glue, EMR, Redshift.
- **GCP Pub/Sub:** Dataflow, BigQuery streaming inserts, Dataproc (Spark), Looker Studio.

### Monitoring & Observability

| | Azure Event Hubs | Amazon Kinesis | GCP Pub/Sub |
|---|---|---|---|
| **Tool** | Azure Monitor (incoming bytes, throttled requests, offset lag) | CloudWatch (iterator age, incoming records) | Cloud Monitoring (backlog bytes, oldest message age) |
| **Schema Validation** | Azure Schema Registry | AWS Glue Schema Registry | Pub/Sub schema validation |

### Pricing Model

| | Azure Event Hubs | Amazon Kinesis | GCP Pub/Sub |
|---|---|---|---|
| **Model** | Per Throughput Unit/hour (Standard) | Per shard-hour + per PUT payload unit | Per GB of data |
| **Free Tier** | None | None | 10 GB/month |
| **Entry Cost** | ~$0.028/throughput unit/hour | $0.015/shard-hour + $0.014/million PUT units | $0.04/GB after free tier |

### Strengths & Weaknesses

| | Strengths | Weaknesses |
|---|---|---|
| **Azure Event Hubs** | Kafka-compatible API; Schema Registry with Avro; straightforward cold storage via Capture | No native stream processing; throughput unit sizing can be tricky |
| **Amazon Kinesis** | Longest retention (365 days); deep AWS analytics integration; Enhanced Fan-Out for low-latency consumers | Manual shard management is a burden at scale; not Kafka-compatible |
| **GCP Pub/Sub** | Fully auto-scaling; no shard/capacity management; generous free tier | Shorter retention (31 days max); no Kafka API; needs Dataflow for stateful processing |

---

## References

- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/) · [AWS Lambda](https://docs.aws.amazon.com/lambda/) · [GCP Cloud Functions](https://cloud.google.com/functions/docs)
- [Durable Functions](https://learn.microsoft.com/en-us/azure/azure-functions/durable/) · [AWS Step Functions](https://docs.aws.amazon.com/step-functions/) · [GCP Workflows](https://cloud.google.com/workflows/docs)
- [Azure Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/) · [AWS AppFlow](https://docs.aws.amazon.com/appflow/) · [GCP Application Integration](https://cloud.google.com/application-integration/docs)
- [Azure Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/) · [Amazon SQS](https://docs.aws.amazon.com/sqs/) · [GCP Pub/Sub](https://cloud.google.com/pubsub/docs)
- [Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/) · [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/) · [GCP Eventarc](https://cloud.google.com/eventarc/docs)
- [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/) · [Amazon Kinesis](https://docs.aws.amazon.com/kinesis/) · [GCP Pub/Sub Streaming](https://cloud.google.com/pubsub/docs/stream-messages-dataflow)

---

*CST8917 – Serverless Applications, Assignment 2*