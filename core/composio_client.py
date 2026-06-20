"""
GOD MOD Empire - Composio API Client
"""
import json, time, logging, urllib.request, urllib.error, urllib.parse, os, re

logger = logging.getLogger("ComposioClient")
COMPOSIO_API_KEY = ""
MCP_URLS = ["https://mcp.composio.dev/mcp", "https://connect.composio.dev/mcp", "https://backend.composio.dev/mcp"]
MCP_URL = MCP_URLS[0]

def set_api_key(key: str):
    global COMPOSIO_API_KEY
    COMPOSIO_API_KEY = key
    if key:
        logger.info("API key configured")

def _mcp_call(tool_name: str, arguments: dict) -> dict:
    global MCP_URL
    errors = []
    urls_to_try = MCP_URLS if MCP_URL == MCP_URLS[0] else [MCP_URL]
    for url in urls_to_try:
        try:
            payload = {"jsonrpc": "2.0", "id": int(time.time() * 1000) % 100000, "method": "tools/call", "params": {"name": tool_name, "arguments": arguments}}
            headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "x-consumer-api-key": COMPOSIO_API_KEY, "User-Agent": "GOD-MOD-Empire/3.0"}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("utf-8")
            if "data: " in raw:
                for line in raw.split("\n"):
                    line = line.strip()
                    if line.startswith("data: "):
                        result = json.loads(line[6:])
                        is_error = result.get("result", {}).get("isError", False)
                        logger.info(f"  MCP {tool_name}: success")
                        MCP_URL = url
                        return {"success": not is_error, "data": result, "raw": raw}
            try:
                result = json.loads(raw)
                MCP_URL = url
                return {"success": True, "data": result}
            except:
                MCP_URL = url
                return {"success": True, "raw": raw}
        except urllib.error.HTTPError as e:
            errors.append(f"{url}: HTTP {e.code}")
            continue
        except Exception as e:
            errors.append(f"{url}: {e}")
            continue
    logger.warning(f"MCP call failed for {tool_name}: {errors}")
    return {"success": False, "error": "; ".join(errors)}

def web_search(query: str) -> list:
    results = []
    methods = [
        ("DuckDuckGo", f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}", lambda html: re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html)),
        ("DuckDuckGo HTML", f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}", lambda html: re.findall(r'class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html)),
    ]
    for name, url, parser in methods:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            links = parser(html)
            seen = set()
            for item in links:
                if len(item) >= 2:
                    u, title = item[0], item[1]
                    title_c = re.sub(r'<[^>]+>', "", title).strip()
                    if u and title_c and u not in seen:
                        seen.add(u)
                        results.append({"title": title_c, "url": u, "source": name.lower().replace(" ", "_")})
                        if len(results) >= 10:
                            break
            if results:
                return results
        except:
            continue
    return results

def search_jobs(query: str) -> list:
    raw = web_search(query)
    return [{"title": r.get("title", "Unknown"), "url": r.get("url", ""), "snippet": r.get("title", ""), "source": r.get("source", "web")} for r in raw if isinstance(r, dict)]

def execute_tool(slug: str, args: dict) -> dict:
    if slug == "GMAIL_SEND_EMAIL":
        return _mcp_call("GMAIL_SEND_EMAIL", {"recipient_email": args.get("to", ""), "subject": args.get("subject", ""), "body": args.get("body", "")})
    if slug == "LINKEDIN_CREATE_LINKED_IN_POST":
        return _mcp_call("LINKEDIN_CREATE_LINKED_IN_POST", {"author": args.get("author", "urn:li:person:BpfA29-PM3"), "commentary": args.get("commentary", ""), "visibility": "PUBLIC", "feedDistribution": "MAIN_FEED", "lifecycleState": "PUBLISHED"})
    return _mcp_call(slug, args)

def send_application_email(to_email: str, subject: str, body: str) -> dict:
    return execute_tool("GMAIL_SEND_EMAIL", {"to": to_email, "subject": subject, "body": body})

def post_linkedin_update(text: str) -> dict:
    return execute_tool("LINKEDIN_CREATE_LINKED_IN_POST", {"commentary": text})
