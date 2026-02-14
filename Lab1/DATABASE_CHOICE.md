# DATABASE CHOICE

## My Choice
Azure Cosmos DB (Core SQL API, Serverless Tier)

## Justification
Azure Cosmos DB is the best choice for storing Text Analyzer results because it natively supports JSON document storage, which aligns perfectly with the structure of the analysis output. The serverless tier allows automatic scaling and pay-per-request pricing, making it cost-effective for our student workloads
It integrates easily with Azure Functions using the Python SDK and requires no predefined schema, reducing complexity.
Additionally, Cosmos DB provides powerful SQL-like querying over JSON documents, enabling future analysis of historical results.

## Alternatives Considered

### Azure Table Storage
Although cheaper and simple, Azure Table Storage has limited querying capabilities and lacks advanced indexing and JSON querying features. It is better suited for simple key-value storage rather than flexible document queries.

### Azure SQL Database
Azure SQL Database is ideal for structured relational data and complex joins.
However, it requires predefined schemas and is less natural for storing flexible JSON documents, making it less suitable for this use case.

### Azure Blob Storage
Blob Storage can store JSON files, but it does not support querying or indexing. Retrieving specific historical analysis results would require downloading entire blobs, which is inefficient for database-style access.

## Cost Considerations
Azure Cosmos DB offers a free tier with limited RU/s and storage, making it suitable for student projects. The serverless tier charges based on request units (RU) consumed, meaning costs remain very low for small workloads. This aligns well with a serverless architecture and lab environment.
