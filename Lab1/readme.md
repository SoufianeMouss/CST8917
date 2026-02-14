# Text Analyzer – Local Development Guide

## Prerequisites

Before running the project locally, ensure you have the following installed:

- **Python 3.10** (recommended to match Azure runtime)
- **Azure Functions Core Tools v4**
- **Azure CLI** (optional, for deployment)

Verify your Python version:

```bash
python --version
````

Expected output:

```text
Python 3.10.x
```

## 1. Clone the Repository

```bash
git clone https://github.com/SoufianeMouss/CST8917/Lab1
cd <project-folder>
```

## 2. Create a Virtual Environment

Create a virtual environment using Python 3.10:

```bash
py -3.10 -m venv .venv
```

Activate it:

### Windows

```bash
.\.venv\Scripts\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

Confirm the correct Python version is active:

```bash
python --version
```

## 3. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create or update the `local.settings.json` file in the project root:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "COSMOS_CONNECTION_STRING": "YOUR_COSMOS_CONNECTION_STRING",
    "COSMOS_DATABASE_NAME": "DBNAME",
    "COSMOS_CONTAINER_NAME": "CONTAIMERNAME"
  }
}
```

### Important

* Replace `YOUR_COSMOS_CONNECTION_STRING` with the **Primary Connection String** from Azure Cosmos DB.
* The database and container names must match what you created in Azure.
* `local.settings.json` is excluded from source control (do not commit it).
* Replace `DBNAME` with your database name
* Replace `CONTAINERNAME` with your container name

## 5. Start the Function Locally

Run:

```bash
func start
```

The API will start at:

```text
http://localhost:7071
```

## 6. Test the Endpoints

### Analyze Text

Using URL query:

```text
http://localhost:7071/api/TextAnalyzer?text=Hello world
```

Or send a POST request with JSON body:

```json
{
  "text": "Your text here"
}
```

### Retrieve Analysis History

Default (returns latest 10 results):

```text
http://localhost:7071/api/GetAnalysisHistory
```

With limit parameter:

```text
http://localhost:7071/api/GetAnalysisHistory?limit=5
```

## Notes

* Azure Cosmos DB must already be created in Azure.
* Ensure the database name and container name match your environment variables.
* Python version must match the Azure runtime version (3.10 recommended).
* `AzureWebJobsStorage` is required for the Azure Functions runtime, even when using Cosmos DB.

