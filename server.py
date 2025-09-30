from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Step 1 — Create MCP instance
mcp = FastMCP("email-server")

# Step 2 — Define input schema
class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str

# Step 3 — Register the sendEmail tool
@mcp.tool()
def sendEmail(input: SendEmailInput):
    """
    Mock email sender.
    In production, you’ll connect to Outlook/Gmail API here.
    """
    print(f"[{datetime.now()}] Sending mock email to {input.to}")
    print(f"Subject: {input.subject}")
    print(f"Body: {input.body}\n")

    return {
        "status": "sent",
        "to": input.to,
        "subject": input.subject,
        "messageId": f"mock-{int(datetime.now().timestamp())}"
    }

# Step 4 — Build FastAPI app
app = FastAPI(title="Email MCP Server")

# Add global exception handler for debugging
@app.exception_handler(Exception)
async def unhandled_exc(_, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": type(exc).__name__, "detail": str(exc)},
    )

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# List tools
@app.get("/tools")
async def list_tools():
    tools = await mcp.list_tools()        # async call!
    names = [t.name for t in tools]
    return {"tools": names}

# Get single tool
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

    # Call the tool (async)
    result = await mcp.call_tool(tool_name, payload)
    return {"result": result}

# Step 5 — Run server
if __name__ == "__main__":
    import uvicorn
    print("Starting custom FastAPI MCP server...")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="debug")




