# PhotoPipe — CST8917 Lab 4

Event-driven image processing pipeline using Azure Event Grid, Azure Functions, and Blob Storage.

##  Demo Video
[Watch the demo](https://www.awesomescreenshot.com/video/51504972?key=350c3a7168483e19674ca981ce887ad2)

---

## Architecture

```
Browser (client.html)
    │  PUT image
    ▼
Blob Storage (image-uploads)
    │  BlobCreated event
    ▼
Event Grid System Topic
    ├── Subscription 1 (.jpg/.png filter) ──► process-image function ──► image-results container
    └── Subscription 2 (all events) ────────► audit-log function ──────► Table Storage (processinglog)
```

---

## Project Structure

```
├── function_app.py               # All Azure Functions (Python v2 model)
├── requirements.txt              # Python dependencies
├── local.settings.example.json   # Config template (copy → local.settings.json)
├── test-function.http            # REST Client test requests
├── client.html                   # PhotoPipe web app
└── README.md
```

---

## Prerequisites

- Azure subscription
- Python 3.11 or 3.12
- VS Code with extensions: Azure Functions, Azurite, REST Client

---

## Setup

### 1. Storage Account
1. Create a storage account (e.g. `yournamephotopipe`) in Azure Portal
2. Under **Configuration**, enable **Allow Blob anonymous access**
3. Create two containers:
   - `image-uploads` — Blob public access
   - `image-results` — Private
4. Under **Resource sharing (CORS)**, add a rule: origins `*`, methods `GET PUT OPTIONS HEAD`
5. Copy the connection string from **Access keys**

### 2. Azure Functions
1. Open this folder in VS Code
2. Copy `local.settings.example.json` → `local.settings.json` and paste your connection string
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Deploy via VS Code: **F1 → Azure Functions: Deploy to Function App**
5. In the portal, add `STORAGE_CONNECTION_STRING` to the Function App's **Environment variables**
6. Under **CORS**, add `*` to allowed origins
7. Verify: `https://<your-func-app>.azurewebsites.net/api/health`

### 3. Event Grid
1. In the Azure Portal, find the Event Grid System Topic auto-created for your storage account
2. Create **Subscription 1** (`process-image-sub`):
   - Endpoint: `process_image` function
   - Subject begins with: `/blobServices/default/containers/image-uploads`
   - Advanced filter: `subject` → `String ends with` → `.jpg` and `.png` (two separate values in one row, leave Subject Ends With empty)
3. Create **Subscription 2** (`audit-log-sub`):
   - Endpoint: `audit_log` function
   - Subject begins with: `/blobServices/default/containers/image-uploads`
   - No suffix filter

### 4. Web Client
1. Generate a SAS token in the portal (Blob service, Container + Object, Read/Write/Create/List, 24h expiry)
2. Open `client.html` with VS Code Live Server
3. Fill in the three config fields:
   - **Storage Account Name** — your storage account name
   - **SAS Token** — paste the generated token
   - **Function App URL** — `https://<your-func-app>.azurewebsites.net`

---

## Testing

| Action | Expected Result |
|---|---|
| Upload a `.jpg` | Results tab shows metadata card, Audit Log shows new entry |
| Upload a `.png` | Same as above |
| Upload a `.txt` or `.pdf` | Only Audit Log gets a new entry — no Results card |

---

## Security Notes

- `local.settings.json` is git-ignored — never commit real keys
- Use `local.settings.example.json` with placeholder values for version control
- SAS tokens should have short expiry and restricted permissions in production
- CORS wildcard (`*`) is for lab convenience only — restrict to your domain in production