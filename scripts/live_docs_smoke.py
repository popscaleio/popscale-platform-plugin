#!/usr/bin/env python3
"""Run a read-only JSON-RPC smoke test against the public Docs MCP."""

from __future__ import annotations

import json
import urllib.request


ENDPOINT = "https://docs.popscale.io/mcp"
PROTOCOL_VERSION = "2025-11-25"


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

    search = rpc(
        3,
        "tools/call",
        {
            "name": "search_docs",
            "arguments": {"query": "Popscale MCP plugin", "limit": 5},
        },
    )
    search_text = json.dumps(search)
    canonical_path = "/integrations/popscale-mcp/"
    assert canonical_path in search_text

    pages = rpc(
        4,
        "tools/call",
        {"name": "get_pages", "arguments": {"paths": [canonical_path]}},
    )
    pages_text = json.dumps(pages)
    assert canonical_path in pages_text
    assert '"status"' in pages_text

    resources = rpc(5, "resources/list", {})["resources"]
    assert any(resource["uri"] == "docs://overview" for resource in resources)
    assert any(resource["uri"] == "docs://pages/integrations--popscale-mcp" for resource in resources)

    print("Live Popscale Docs MCP smoke passed")
    print("initialize, tools/list, search_docs, get_pages, and resources/list succeeded")


if __name__ == "__main__":
    main()
