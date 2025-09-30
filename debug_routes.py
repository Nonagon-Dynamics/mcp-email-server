from mcp.server.fastmcp import FastMCP

mcp = FastMCP("email-server")

print("Available routes in SSE app:")
for route in mcp.sse_app.router.routes:
    print(route.path)

print("\nAvailable routes in Streamable HTTP app:")
for route in mcp.streamable_http_app.router.routes:
    print(route.path)
