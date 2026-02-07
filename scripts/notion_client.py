#!/usr/bin/env python3
"""
Notion API client for agent-driven page customization.

Usage:
    python notion_client.py create-page --parent <page_id> --template <template.json>
    python notion_client.py update-page --page <page_id> --content <content.json>
    python notion_client.py query-db --database <database_id>
    python notion_client.py append-blocks --page <page_id> --blocks <blocks.json>
    python notion_client.py get-page --page <page_id>
    python notion_client.py create-db --parent <page_id> --template <template.json>
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client

# Load .env from repo root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

NOTION_TOKEN = os.environ.get("NOTION_API_TOKEN")
CONFIG_PATH = Path(__file__).resolve().parent.parent / "notion-config.json"


def get_client() -> Client:
    if not NOTION_TOKEN:
        print("Error: NOTION_API_TOKEN not set. See .env.example", file=sys.stderr)
        sys.exit(1)
    return Client(auth=NOTION_TOKEN)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def resolve_id(name: str) -> str:
    """Resolve a friendly name from notion-config.json to a Notion ID, or return as-is."""
    config = load_config()
    for section in ("pages", "databases"):
        if name in config.get(section, {}):
            return config[section][name]["id"]
    return name


def load_json_file(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def cmd_create_page(args):
    client = get_client()
    parent_id = resolve_id(args.parent)
    template = load_json_file(args.template) if args.template else {}

    properties = template.get("properties", {})
    if isinstance(properties, dict) and "title" in properties and isinstance(properties["title"], str):
        # Convert shorthand title string to Notion API format
        title_text = properties.pop("title")
        properties["title"] = {
            "title": [{"type": "text", "text": {"content": title_text}}]
        }

    response = client.pages.create(
        parent={"page_id": parent_id},
        properties=properties,
        children=template.get("children", []),
    )
    print(json.dumps(response, indent=2, default=str))


def cmd_create_db(args):
    client = get_client()
    parent_id = resolve_id(args.parent)
    template = load_json_file(args.template)

    response = client.databases.create(
        parent={"page_id": parent_id},
        title=[{"type": "text", "text": {"content": args.title or "Untitled"}}],
        properties=template.get("properties", {}),
    )
    print(json.dumps(response, indent=2, default=str))


def cmd_update_page(args):
    client = get_client()
    page_id = resolve_id(args.page)
    content = load_json_file(args.content)

    response = client.pages.update(page_id=page_id, **content)
    print(json.dumps(response, indent=2, default=str))


def cmd_query_db(args):
    client = get_client()
    db_id = resolve_id(args.database)

    filter_obj = load_json_file(args.filter) if args.filter else None
    kwargs = {"database_id": db_id}
    if filter_obj:
        kwargs["filter"] = filter_obj

    response = client.databases.query(**kwargs)
    print(json.dumps(response, indent=2, default=str))


def cmd_append_blocks(args):
    client = get_client()
    page_id = resolve_id(args.page)
    blocks = load_json_file(args.blocks)

    if isinstance(blocks, dict):
        blocks = blocks.get("children", [blocks])

    response = client.blocks.children.append(block_id=page_id, children=blocks)
    print(json.dumps(response, indent=2, default=str))


def cmd_get_page(args):
    client = get_client()
    page_id = resolve_id(args.page)

    page = client.pages.retrieve(page_id=page_id)
    blocks = client.blocks.children.list(block_id=page_id)

    result = {"page": page, "blocks": blocks}
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="Notion API client for agents")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create-page", help="Create a new page")
    p_create.add_argument("--parent", required=True, help="Parent page ID or config name")
    p_create.add_argument("--template", help="Path to template JSON file")
    p_create.set_defaults(func=cmd_create_page)

    p_create_db = sub.add_parser("create-db", help="Create a new database")
    p_create_db.add_argument("--parent", required=True, help="Parent page ID or config name")
    p_create_db.add_argument("--template", required=True, help="Path to template JSON file")
    p_create_db.add_argument("--title", help="Database title")
    p_create_db.set_defaults(func=cmd_create_db)

    p_update = sub.add_parser("update-page", help="Update page properties")
    p_update.add_argument("--page", required=True, help="Page ID or config name")
    p_update.add_argument("--content", required=True, help="Path to content JSON file")
    p_update.set_defaults(func=cmd_update_page)

    p_query = sub.add_parser("query-db", help="Query a database")
    p_query.add_argument("--database", required=True, help="Database ID or config name")
    p_query.add_argument("--filter", help="Path to filter JSON file")
    p_query.set_defaults(func=cmd_query_db)

    p_append = sub.add_parser("append-blocks", help="Append blocks to a page")
    p_append.add_argument("--page", required=True, help="Page ID or config name")
    p_append.add_argument("--blocks", required=True, help="Path to blocks JSON file")
    p_append.set_defaults(func=cmd_append_blocks)

    p_get = sub.add_parser("get-page", help="Get page details and blocks")
    p_get.add_argument("--page", required=True, help="Page ID or config name")
    p_get.set_defaults(func=cmd_get_page)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
