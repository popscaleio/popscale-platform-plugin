#!/usr/bin/env python3
"""Run a read-only JSON-RPC smoke test against the public Docs MCP."""

from __future__ import annotations

import json
import urllib.request


ENDPOINT = "https://docs.popscale.io/mcp"
PROTOCOL_VERSION = "2025-11-25"
CANONICAL_PATH = "/integrations/connect-assistant/"
PAGE_RESOURCE_URI = "docs://pages/integrations--connect-assistant"


def rpc(request_id: int, method: str, params: dict) -> dict:
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "popscale-platform-plugin-release-smoke/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8")
        content_type = response.headers.get_content_type()

    if content_type == "text/event-stream":
        messages = [
            json.loads(line.removeprefix("data: "))
            for line in body.splitlines()
            if line.startswith("data: ")
        ]
        if not messages:
            raise AssertionError(f"No JSON-RPC message in SSE response for {method}")
        message = messages[-1]
    else:
        message = json.loads(body)

    if "error" in message:
        raise AssertionError(f"{method} returned error: {message['error']}")
    return message["result"]


def call_tool(request_id: int, name: str, arguments: dict) -> dict:
    result = rpc(
        request_id, "tools/call", {"name": name, "arguments": arguments}
    )
    assert not result.get("isError"), f"{name} returned a tool error: {result}"
    data = result.get("structuredContent")
    assert isinstance(data, dict), f"{name} returned no structured content: {result}"
    return data


def main() -> None:
    initialized = rpc(
        1,
        "initialize",
        {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {
                "name": "popscale-platform-plugin-release-smoke",
                "version": "1.0.0",
            },
        },
    )
    assert initialized["protocolVersion"] == PROTOCOL_VERSION
    assert initialized["serverInfo"]["name"] == "popscale-docs"

    listed_tools = rpc(2, "tools/list", {})["tools"]
    assert {tool["name"] for tool in listed_tools} == {
        "get_docs_overview",
        "search_docs",
        "get_pages",
    }
    for tool in listed_tools:
        annotations = tool["annotations"]
        assert annotations["readOnlyHint"] is True
        assert annotations["destructiveHint"] is False
        assert annotations["idempotentHint"] is True
        assert annotations["openWorldHint"] is False

    search = call_tool(
        3, "search_docs", {"query": "Anslut en AI-assistent", "limit": 5}
    )
    paths = [result["path"] for result in search.get("results", [])]
    assert CANONICAL_PATH in paths, f"search_docs missing {CANONICAL_PATH}; got {paths}"

    pages = call_tool(4, "get_pages", {"paths": [CANONICAL_PATH]})
    matching_pages = [
        page for page in pages.get("pages", []) if page.get("path") == CANONICAL_PATH
    ]
    assert len(matching_pages) == 1, f"get_pages missing unique page {CANONICAL_PATH}"
    page = matching_pages[0]
    assert page.get("status") == "published", f"{CANONICAL_PATH} is not published"
    assert isinstance(page.get("markdown"), str) and page["markdown"].strip(), (
        f"{CANONICAL_PATH} returned no Markdown content"
    )

    resources = rpc(5, "resources/list", {})["resources"]
    assert any(resource["uri"] == "docs://overview" for resource in resources)
    assert any(resource["uri"] == PAGE_RESOURCE_URI for resource in resources), (
        f"resources/list missing {PAGE_RESOURCE_URI}"
    )

    print("Live Popscale Docs MCP smoke passed")
    print("initialize, tools/list, search_docs, get_pages, and resources/list succeeded")


if __name__ == "__main__":
    main()
