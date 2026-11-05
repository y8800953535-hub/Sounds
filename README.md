# Sounds — Yandex Music AI Connector

Sounds is a personal AI music assistant that connects ChatGPT
to Yandex Music through an MCP server.

## Features

- Search tracks in Yandex Music.
- Read liked tracks.
- List personal playlists.
- Create private playlists.
- Add tracks to playlists.
- Build personalized music selections.

## Technology

- Python 3
- FastMCP
- Yandex Music API library
- Render Cloud Hosting

## Project structure

```text
Sounds/
├── server.py
├── requirements.txt
├── render.yaml
├── get_token.py
└── README.md
```

## Environment variables

Configure these variables in Render:

- `YM_TOKEN` — Yandex Music account token.
- `MCP_ACCESS_TOKEN` — private access token for the MCP server.

Never commit tokens or passwords to GitHub.

## Deployment

1. Connect this repository to Render.
2. Deploy the Web Service using render.yaml.
3. Add the required environment variables.
4. Check `/health`.
5. Connect the MCP endpoint `/mcp` to a compatible client.

## Security

The MCP endpoint requires Bearer authentication.
The health endpoint does not expose account information.

## Disclaimer

This project uses an unofficial community-maintained
Yandex Music API library. Compatibility may change
when Yandex updates its services.

Sounds does not download or redistribute music.
