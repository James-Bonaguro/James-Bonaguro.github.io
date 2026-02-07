# Notion Agent Customization Hub

A repo you point AI agents at to customize your Notion pages. Define what you want in plain markdown, and agents use the Notion API to make it happen.

## How it works

1. **You** add a request file in `requests/` describing what Notion page to create or modify
2. **An agent** reads the request, picks up the right template, and executes via the Notion API
3. **Done** — the agent marks the request complete and commits

## Repo structure

```
├── CLAUDE.md              # Agent instructions (agents read this first)
├── notion-config.json     # Maps friendly names -> Notion page/database IDs
├── .env.example           # Notion API token setup
├── requirements.txt       # Python dependencies
├── requests/              # Customization requests (one per file)
│   ├── _template.md       # Template for new requests
│   └── example-*.md       # Example requests
├── templates/             # Reusable Notion page/database templates (JSON)
│   ├── project-tracker.json
│   ├── meeting-notes.json
│   └── dashboard.json
└── scripts/
    └── notion_client.py   # CLI tool for Notion API operations
```

## Setup

1. Create a [Notion integration](https://www.notion.so/my-integrations) and get your API token
2. Copy `.env.example` to `.env` and add your token
3. Share your Notion pages/databases with the integration
4. Add page/database IDs to `notion-config.json`
5. Install dependencies: `pip install -r requirements.txt`

## Creating a request

Copy `requests/_template.md` and fill in:
- **target**: `page` or `database`
- **notion_id**: friendly name from `notion-config.json` or a raw Notion ID
- **template**: optional template from `templates/`
- **description**: what you want done

## Available templates

| Template | Type | Description |
|----------|------|-------------|
| `project-tracker.json` | database | Project board with status, priority, dates, ownership |
| `meeting-notes.json` | page | Structured meeting notes with agenda and action items |
| `dashboard.json` | page | Overview dashboard with linked database sections |

## CLI usage

```bash
# Create a page from template
python scripts/notion_client.py create-page --parent example-landing --template templates/meeting-notes.json

# Create a database from template
python scripts/notion_client.py create-db --parent example-landing --template templates/project-tracker.json --title "Projects"

# Query a database
python scripts/notion_client.py query-db --database example-projects

# Append content to a page
python scripts/notion_client.py append-blocks --page example-landing --blocks content.json

# Get page details
python scripts/notion_client.py get-page --page example-landing
```

## Also in this repo
- `index.html` — personal site (single-file, inline CSS)
- `se-demo.html` — demo framework page
- Live at https://james-bonaguro.github.io/

## Contact
- Email: james.bonaguro@gmail.com
- LinkedIn: https://linkedin.com/in/jamesbonaguro
