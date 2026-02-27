# Running the Smart Image Analyzer Locally

## 1 Clone the repository

If you haven't already downloaded the code, clone it from GitHub and open the folder:

```bash
git clone https://github.com/SoufianeMouss/CST8917.git
cd CST8917/lab2
```

The supplied project is a **Python Azure Durable Functions app** that uses the fan‑out/fan‑in pattern. When an image is uploaded to a Blob Storage container called `images`, a blob‑triggered client function starts an orchestrator. The orchestrator fans out to run four activity functions in parallel (colour analysis, object detection, OCR and metadata extraction), then fans back in to generate a combined report and stores it in **Azure Table Storage**. An HTTP endpoint is exposed for retrieving reports.

The steps below show how to get the project running locally on your machine using Azurite (the local Azure Storage emulator) and Azure Functions Core Tools. It assumes that you have already completed the **Week 4 Durable Functions exercise**, have **Python 3.11 or 3.12**, **VS Code with the Azure Functions extension** and **Azure Functions Core Tools** installed. See the official documentation for general advice on developing functions locally.【185776472738070†L190-L204】

## 2 Install prerequisites

1. **Python environment** – Create and activate a virtual environment so that packages do not pollute your global Python installation. In your project folder:

   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows PowerShell
   # .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies** – Install Python packages from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Azure Functions Core Tools** – If you have not already installed the Core Tools (v4 or later), do so using npm:

   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

4. **Azurite (local storage emulator)** – The function app uses Blob and Table Storage triggers/bindings, so you need a local emulator. Install Azurite globally and start it in another terminal window:

   ```bash
   npm install -g azurite
   # start the emulator – it listens on ports 10000 (Blob), 10001 (Queue) and 10002 (Table)
   azurite --silent
   ```

   Azure Functions notes that when you set the `AzureWebJobsStorage` connection string to **`UseDevelopmentStorage=true`**, the Functions host uses the Azurite emulator.【185776472738070†L280-L285】 Our `local.settings.json` uses `UseDevelopmentStorage=true` so the function app will talk to the local emulator.

## 3 Configure local settings

The `local.settings.json` file contains application settings that apply only when running locally. Do **not** commit secrets here to source control.

Ensure these keys exist in the `Values` section (names must match exactly):

* `AzureWebJobsStorage` = `UseDevelopmentStorage=true`
* `FUNCTIONS_WORKER_RUNTIME` = `python`
* `ImageStorageConnection` = `UseDevelopmentStorage=true`

`AzureWebJobsStorage` tells the Functions host where to find storage for triggers and logging. When set to `UseDevelopmentStorage=true` it uses Azurite. `ImageStorageConnection` is used by the Blob trigger and Table Storage client and points to the same emulator.

## 4 Start the function host

From the project root (where `function_app.py`, `host.json` and `local.settings.json` live), run:

```bash
func start
```

This launches the local Functions runtime on port `7071` and loads your durable functions.

> If port 7071 is in use, run `func start --port 7080`.

## 5 Upload an image to trigger the orchestration

1. Open **Azure Storage Explorer**.
2. Connect to local storage using connection string: `UseDevelopmentStorage=true`.
3. Create a blob container named **`images`**.
4. Upload any test image (`.jpg` / `.png`) into the `images` container.

When the blob is added, the blob trigger fires and starts the orchestration. The activities run in parallel, then a report is generated and saved to Table Storage.

## 6 Retrieve analysis results (HTTP)

The app exposes an HTTP endpoint for reading stored results:

| Endpoint                                     | Description                                                               |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| `GET http://localhost:7071/api/results`      | Returns the most recent 10 results (use `?limit=5` to change the number). |
| `GET http://localhost:7071/api/results/{id}` | Returns the full report for a specific analysis ID.                       |

Example:

```bash
curl http://localhost:7071/api/results
```

## 7 Cleanup / stop

* Stop the Functions host: `Ctrl + C`
* Stop Azurite: `Ctrl + C` in the Azurite terminal

## Notes

* To test against a real Azure Storage account instead of Azurite, replace the `UseDevelopmentStorage=true` values with a real connection string in `local.settings.json`. Be careful: local tests can affect live resources.
