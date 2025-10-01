from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Create the MCP server
mcp = FastMCP("email-server")

# -----------------------
# TOOL 1: sendEmail
# -----------------------
class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str
    confirm: Optional[bool] = False
    confirmOverride: Optional[bool] = False

@mcp.tool()
def sendEmail(input: SendEmailInput):
    """
    Simulated email send.
    Requires confirm=True or confirmOverride=True.
    """
    if not (input.confirm or input.confirmOverride):
        return {"error": "Confirmation required before sending."}
    
    print("✅ sendEmail tool triggered")
    print(f"[{datetime.now()}] Simulating send to {input.to}")
    print(f"Subject: {input.subject}")
    print(f"Body: {input.body}\n")

    return {
        "status": "sent",
        "to": input.to,
        "subject": input.subject,
        "messageId": f"mock-{int(datetime.now().timestamp())}"
    }

# -----------------------
# TOOL 2: draftEmail
# -----------------------
class DraftEmailInput(BaseModel):
    to: Optional[str] = None
    subject: Optional[str] = None
    body: str
    tone: Optional[str] = "concise"

@mcp.tool()
def draftEmail(input: DraftEmailInput):
    """
    Create a draft email.
    """
    print("📝 draftEmail tool triggered")
    print(f"To: {input.to or '(not set yet)'}")
    print(f"Subject: {input.subject or '(suggested later)'}")
    print(f"Body: {input.body}\n")

    return {
        "draftId": f"draft-{int(datetime.now().timestamp())}",
        "subject": input.subject or "Draft Subject",
        "body": input.body
    }

# -----------------------
# TOOL 3: searchMailbox
# -----------------------
class SearchMailboxInput(BaseModel):
    query: Optional[str] = None
    from_: Optional[str] = None
    subject: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    folder: Optional[str] = "inbox"
    limit: Optional[int] = 5

@mcp.tool()
def searchMailbox(input: SearchMailboxInput):
    """
    Mock search tool — returns placeholder results.
    """
    print("🔍 searchMailbox tool triggered")
    print(f"Query: {input.query or 'none'} | Folder: {input.folder}\n")

    results = [
        {"id": f"msg-{i}", "from": "alice@example.com", "subject": f"Mock Email {i}",
         "snippet": "This is a simulated email preview...", "date": str(datetime.now())}
        for i in range(1, input.limit + 1)
    ]

    return {"results": results}

# -----------------------
# TOOL 4: getMessage
# -----------------------
class GetMessageInput(BaseModel):
    id: str

@mcp.tool()
def getMessage(input: GetMessageInput):
    """
    Retrieve a mock email message by ID.
    """
    print("📬 getMessage tool triggered")
    print(f"Fetching message ID: {input.id}\n")

    return {
        "id": input.id,
        "from": "bob@example.com",
        "to": ["user@example.com"],
        "subject": "Mock Message",
        "date": str(datetime.now()),
        "body": "This is the content of the mock message.",
        "attachments": []
    }

# -----------------------
# TOOL 5: moveMessage
# -----------------------
class MoveMessageInput(BaseModel):
    id: str
    destination: str

@mcp.tool()
def moveMessage(input: MoveMessageInput):
    """
    Mock moving a message to a folder.
    """
    print("📂 moveMessage tool triggered")
    print(f"Moving {input.id} to {input.destination}\n")

    return {"id": input.id, "status": "moved", "destination": input.destination}

# -----------------------
# TOOL 6: markRead
# -----------------------
class MarkReadInput(BaseModel):
    id: str
    isRead: bool

@mcp.tool()
def markRead(input: MarkReadInput):
    """
    Toggle message read/unread.
    """
    print("👁️ markRead tool triggered")
    print(f"Message {input.id} marked as {'read' if input.isRead else 'unread'}\n")

    return {"id": input.id, "isRead": input.isRead}

# -----------------------
# TOOL 7: suggestSubject
# -----------------------
class SuggestSubjectInput(BaseModel):
    body: str
    style: Optional[str] = "concise"

@mcp.tool()
def suggestSubject(input: SuggestSubjectInput):
    """
    Suggest subject lines from body text.
    """
    print("💡 suggestSubject tool triggered")
    print(f"Generating subject for style: {input.style}\n")

    suggestions = [
        "Quick update",
        "Follow-up from our meeting",
        "Next steps",
        "Action required"
    ]

    return {"suggestions": suggestions[:3]}

# -----------------------
# Run MCP Server
# -----------------------
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MCP server...")
    uvicorn.run(mcp.fastapi_app, host="127.0.0.1", port=8000, log_level="info")



