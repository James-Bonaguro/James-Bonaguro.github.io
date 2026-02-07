# Agent Instructions — Notion Page Customization

This repo is a control center for AI agents to customize Notion pages.

## How This Repo Works

1. The user creates a **request** in `requests/` describing what Notion page(s) to create or modify
2. An agent reads the request, references `templates/` and `notion-config.json` for context
3. The agent uses the Notion API (via `scripts/notion_client.py`) to execute the changes
4. The agent marks the request as done and commits the result

## Setup

Before making any Notion API calls, ensure:
- The `NOTION_API_TOKEN` environment variable is set (see `.env.example`)
- The target database/page IDs are listed in `notion-config.json`
- Required Python packages are installed: `pip install -r requirements.txt`

## Workflow

### 1. Read the request
Look in `requests/` for any `.md` file without a `status: done` frontmatter field. Each request describes:
- What page or database to target
- What changes to make (content, properties, layout)
- Which template to base it on (if any)

### 2. Resolve references
- `notion-config.json` — maps friendly names to Notion page/database IDs
- `templates/` — reusable JSON structures for common page types

### 3. Execute via Notion API
Use the helper in `scripts/notion_client.py` or call the Notion API directly.

Key operations:
- **Create a page**: `python scripts/notion_client.py create-page --parent <id> --template <template.json>`
- **Update a page**: `python scripts/notion_client.py update-page --page <id> --content <content.json>`
- **Query a database**: `python scripts/notion_client.py query-db --database <id>`
- **Append blocks**: `python scripts/notion_client.py append-blocks --page <id> --blocks <blocks.json>`

### 4. Mark complete
After making changes, update the request file's frontmatter to `status: done` and commit.

## Conventions

- All Notion block content uses the [Notion API block format](https://developers.notion.com/reference/block)
- Templates in `templates/` are valid Notion API request bodies
- Page IDs in `notion-config.json` use the 32-char hex format (no dashes)
- Keep requests atomic — one request per page or logical change
