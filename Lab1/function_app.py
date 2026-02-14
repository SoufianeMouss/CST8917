# =============================================================================
# IMPORTS - Libraries we need for our function
# =============================================================================
import azure.functions as func
import logging
import json
import re
import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient

# =============================================================================
# CREATE THE FUNCTION APP
# =============================================================================
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# =============================================================================
# COSMOS DB HELPER FUNCTION
# =============================================================================
def save_to_cosmos(analysis_data, metadata, original_text):
    """
    Saves analysis results to Azure Cosmos DB
    """

    conn_str = os.getenv("COSMOS_CONNECTION_STRING")
    db_name = os.getenv("COSMOS_DATABASE_NAME")
    container_name = os.getenv("COSMOS_CONTAINER_NAME")

    client = CosmosClient.from_connection_string(conn_str)
    database = client.get_database_client(db_name)
    container = database.get_container_client(container_name)

    record_id = str(uuid.uuid4())

    document = {
        "id": record_id,
        "analysis": analysis_data,
        "metadata": metadata,
        "originalText": original_text
    }

    container.create_item(body=document)

    return record_id

# =============================================================================
# DEFINE THE TEXT ANALYZER FUNCTION
# =============================================================================
@app.route(route="TextAnalyzer")
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Text Analyzer API was called!')

    text = req.params.get('text')

    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            pass

    if text:

        # ---------------- Word Analysis ----------------
        words = text.split()
        word_count = len(words)

        # ---------------- Character Analysis ----------------
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))

        # ---------------- Sentence Analysis ----------------
        sentence_count = len(re.findall(r'[.!?]+', text)) or 1

        # ---------------- Paragraph Analysis ----------------
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])

        # ---------------- Reading Time ----------------
        reading_time_minutes = round(word_count / 200, 1)

        # ---------------- Average Word Length ----------------
        avg_word_length = round(char_count_no_spaces / word_count, 1) if word_count > 0 else 0

        # ---------------- Longest Word ----------------
        longest_word = max(words, key=len) if words else ""

        # =====================================================================
        # BUILD ANALYSIS OBJECT
        # =====================================================================
        analysis_data = {
            "wordCount": word_count,
            "characterCount": char_count,
            "characterCountNoSpaces": char_count_no_spaces,
            "sentenceCount": sentence_count,
            "paragraphCount": paragraph_count,
            "averageWordLength": avg_word_length,
            "longestWord": longest_word,
            "readingTimeMinutes": reading_time_minutes
        }

        metadata = {
            "analyzedAt": datetime.utcnow().isoformat(),
            "textPreview": text[:100] + "..." if len(text) > 100 else text
        }

        # =====================================================================
        # SAVE TO COSMOS DB
        # =====================================================================
        try:
            record_id = save_to_cosmos(analysis_data, metadata, text)
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            return func.HttpResponse(
                json.dumps({"error": "Failed to save to database", "details": str(e)}, indent=2),
                mimetype="application/json",
                status_code=500
            )

        # =====================================================================
        # BUILD FINAL RESPONSE (Now includes ID)
        # =====================================================================
        response_data = {
            "id": record_id,
            "analysis": analysis_data,
            "metadata": metadata
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    else:

        instructions = {
            "error": "No text provided",
            "howToUse": {
                "option1": "Add ?text=YourText to the URL",
                "option2": "Send a POST request with JSON body: {\"text\": \"Your text here\"}",
                "example": "https://your-function-url/api/TextAnalyzer?text=Hello world"
            }
        }

        return func.HttpResponse(
            json.dumps(instructions, indent=2),
            mimetype="application/json",
            status_code=400
        )
# =============================================================================
# GET ANALYSIS HISTORY ENDPOINT
# =============================================================================
@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("GetAnalysisHistory API was called!")

    try:
        # Get optional limit parameter (default = 10)
        limit = req.params.get("limit")

        try:
            limit = int(limit) if limit else 10
        except ValueError:
            limit = 10

        conn_str = os.getenv("COSMOS_CONNECTION_STRING")
        db_name = os.getenv("COSMOS_DATABASE_NAME")
        container_name = os.getenv("COSMOS_CONTAINER_NAME")

        client = CosmosClient.from_connection_string(conn_str)
        database = client.get_database_client(db_name)
        container = database.get_container_client(container_name)

        # Cosmos SQL query (ORDER BY newest first)
        query = f"""
            SELECT * FROM c
            ORDER BY c.metadata.analyzedAt DESC
            OFFSET 0 LIMIT {limit}
        """

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        # Remove originalText to keep response clean (optional but recommended)
        results = [
            {
                "id": item["id"],
                "analysis": item["analysis"],
                "metadata": item["metadata"]
            }
            for item in items
        ]

        response_data = {
            "count": len(results),
            "results": results
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"History retrieval error: {str(e)}")

        return func.HttpResponse(
            json.dumps({"error": "Failed to retrieve history", "details": str(e)}, indent=2),
            mimetype="application/json",
            status_code=500
        )
