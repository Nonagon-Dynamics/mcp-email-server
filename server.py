from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import uvicorn

# Step 1 — Create MCP instance
mcp = FastMCP("email-server")

# -------------------------------
# Step 2 — Define Input Schemas
# -------------------------------

class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str

class SearchInput(BaseModel):
    query: str

# -------------------------------
# Step 3 — Register Tools
# -------------------------------

@mcp.tool()
def sendEmail(input: SendEmailInput):
    """Mock email sender."""
    print(f"[{datetime.now()}] Sending mock email to {input.to}")
    print(f"Subject: {input.subject}")
    print(f"Body: {input.body}\n")

    return {
        "status": "sent",
        "to": input.to,
        "subject": input.subject,
        "messageId": f"mock-{int(datetime.now().timestamp())}"
    }

@mcp.tool()
def saveDraft(input: SendEmailInput):
    """Saves an email as a draft (mock)."""
    print(f"[{datetime.now()}] Saving draft for {input.to}")
    return {
        "status": "draft_saved",
        "to": input.to,
        "subject": input.subject,
        "savedAt": datetime.now().isoformat()
    }

@mcp.tool()
def getInboxSummary():
    """Returns a mock summary of recent emails."""
    return {
        "unread": 3,
        "latest": [
            {"from": "team@example.com", "subject": "Project Update"},
            {"from": "hr@example.com", "subject": "Policy Change"},
            {"from": "boss@example.com", "subject": "Meeting Reminder"},
        ],
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
def searchEmails(input: SearchInput):
    """Search inbox for matching messages (mock)."""
    print(f"[{datetime.now()}] Searching inbox for query: {input.query}")
    return {
        "query": input.query,
        "results": [
            {"from": "noreply@example.com", "subject": "Receipt for your order"},
            {"from": "support@example.com", "subject": f"Follow-up: {input.query}"},
        ],
        "timestamp": datetime.now().isoformat()
    }

# -------------------------------
# Step 4 — Build FastAPI App
# -------------------------------

app = FastAPI(title="Email MCP Server")

# Global exception handler
@app.exception_handler(Exception)
async def unhandled_exc(_, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": type(exc).__name__, "detail": str(exc)},
    )

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# List all tools
@app.get("/tools")
async def list_tools():
    tools = await mcp.list_tools()
    names = [t.name for t in tools]
    return {"tools": names}

# Get a specific tool
@app.get("/tools/{tool_name}")
async def get_tool(tool_name: str):
    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    if tool_name not in tool_names:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"tool": tool_name}

# Execute a tool
@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    payload = await request.json()

    # Validate that the tool exists
    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    if tool_name not in tool_names:
        raise HTTPException(status_code=404, detail="Tool not found")

    # Execute the tool
    result = await mcp.call_tool(tool_name, payload)
    return {"result": result}

# -------------------------------
# Step 5 — Run Server
# -------------------------------

if __name__ == "__main__":
    print("🚀 Starting custom FastAPI MCP server...")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="debug")



#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



