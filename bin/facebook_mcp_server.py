import json, sys, os, urllib.request, urllib.error, urllib.parse

FACEBOOK_API = "https://graph.facebook.com/v22.0"
PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN", "")

TOOLS = [
    {
        "name": "get_page_insights",
        "description": "Get organic page insights (reach, impressions, engagement, fan count) for a date range",
        "inputSchema": {
            "type": "object",
            "properties": {
                "since": {"type": "string", "description": "Start date YYYY-MM-DD or relative like 30daysago"},
                "until": {"type": "string", "description": "End date YYYY-MM-DD or today"}
            }
        }
    },
    {
        "name": "list_recent_posts",
        "description": "List recent posts from the page with id, message, created_time, permalink_url",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Number of posts to return (default 10)"}
            }
        }
    },
    {
        "name": "get_post_insights",
        "description": "Get insights for a specific post (impressions, engagement, reactions, clicks)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string", "description": "Facebook post ID"}
            },
            "required": ["post_id"]
        }
    },
    {
        "name": "get_page_fans",
        "description": "Get total page follower count",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_demographics",
        "description": "Get follower demographics (city, age/gender, country)",
        "inputSchema": {"type": "object", "properties": {}}
    }
]

def graph_get(path, params=None):
    if params is None:
        params = {}
    params["access_token"] = ACCESS_TOKEN
    qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"{FACEBOOK_API}/{path}?{qs}"
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}
    except Exception as e:
        return {"error": str(e)}

def handle(req):
    method = req.get("method", "")
    params = req.get("params", {})
    rid = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": rid,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "facebook-insights", "version": "1.0.0"}
            }
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})

        if name == "get_page_insights":
            data = graph_get(f"{PAGE_ID}/insights", {
                "metric": "page_impressions,page_impressions_unique,page_engaged_users,page_fans,page_fan_adds,page_impressions_organic",
                "since": args.get("since", "30daysago"),
                "until": args.get("until", "today"),
                "period": "day"
            })
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2, ensure_ascii=False)}]}}

        if name == "list_recent_posts":
            data = graph_get(f"{PAGE_ID}/posts", {
                "limit": args.get("limit", 10),
                "fields": "id,message,created_time,permalink_url"
            })
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2, ensure_ascii=False)}]}}

        if name == "get_post_insights":
            data = graph_get(f"{args['post_id']}/insights", {
                "metric": "post_impressions,post_impressions_unique,post_engaged_users,post_reactions_by_type_total,post_clicks",
                "period": "lifetime"
            })
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2, ensure_ascii=False)}]}}

        if name == "get_page_fans":
            data = graph_get(PAGE_ID, {"fields": "fan_count"})
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2, ensure_ascii=False)}]}}

        if name == "get_demographics":
            data = graph_get(f"{PAGE_ID}/insights", {
                "metric": "page_fans_city,page_fans_gender_age,page_fans_country"
            })
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(data, indent=2, ensure_ascii=False)}]}}

        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"Unknown tool: {name}"}}

    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"Unknown method: {method}"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()
