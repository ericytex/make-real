from typing import Dict, Any, List

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from . import Tool


def web_search(args: Dict[str, Any]) -> Dict[str, Any]:
    query: str = args.get("query", "")
    max_results: int = int(args.get("max_results", 5))
    if not query:
        return {"ok": False, "error": "Missing 'query'"}
    try:
        with DDGS() as ddgs:
            results: List[Dict[str, Any]] = []
            for hit in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": hit.get("title"),
                    "href": hit.get("href"),
                    "body": hit.get("body"),
                })
        return {"ok": True, "results": results}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def http_get(args: Dict[str, Any]) -> Dict[str, Any]:
    url: str = args.get("url", "")
    if not url:
        return {"ok": False, "error": "Missing 'url'"}
    try:
        resp = requests.get(url, timeout=20)
        content_type = resp.headers.get("content-type", "")
        text = resp.text
        title = None
        if "html" in content_type:
            soup = BeautifulSoup(text, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else None
        return {
            "ok": True,
            "status": resp.status_code,
            "content_type": content_type,
            "title": title,
            "text": text,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_tools() -> Dict[str, Tool]:
    return {
        "web.search": Tool(
            name="web.search",
            description="Search the web with DuckDuckGo and return results.",
            schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
            runner=web_search,
        ),
        "web.get": Tool(
            name="web.get",
            description="HTTP GET a URL; returns status, content type, optional title, and text.",
            schema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
            runner=http_get,
        ),
    }
