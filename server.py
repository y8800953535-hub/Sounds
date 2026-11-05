import os
import secrets
from typing import Optional

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from yandex_music import Client

YM_TOKEN = os.getenv("YM_TOKEN")
MCP_ACCESS_TOKEN = os.getenv("MCP_ACCESS_TOKEN")

mcp = FastMCP("Sounds — Yandex Music")

_client = None


def get_client():
    global _client

    if not YM_TOKEN:
        raise RuntimeError("YM_TOKEN is not configured")

    if _client is None:
        _client = Client(YM_TOKEN).init()

    return _client


@mcp.tool()
def search_tracks(query: str, limit: int = 10) -> list:
    """Search for tracks in Yandex Music."""
    client = get_client()
    result = client.search(query, type_="track")

    tracks = result.tracks.results if result.tracks else []

    return [
        {
            "id": track.id,
            "title": track.title,
            "artists": [artist.name for artist in track.artists],
            "albums": [
                album.title for album in (track.albums or [])
            ],
        }
        for track in tracks[:max(1, min(limit, 30))]
    ]


@mcp.tool()
def get_liked_tracks(limit: int = 30) -> list:
    """Get tracks liked by the connected Yandex Music account."""
    client = get_client()
    result = client.users_likes_tracks()

    tracks = result if isinstance(result, list) else result.tracks

    return [
        {
            "id": item.track.id,
            "title": item.track.title,
            "artists": [
                artist.name for artist in item.track.artists
            ],
        }
        for item in tracks[:max(1, min(limit, 100))]
        if item.track
    ]


@mcp.tool()
def list_my_playlists() -> list:
    """List playlists belonging to the connected account."""
    client = get_client()
    playlists = client.users_playlists_list()

    return [
        {
            "kind": playlist.kind,
            "title": playlist.title,
            "track_count": playlist.track_count,
        }
        for playlist in playlists
    ]


@mcp.tool()
def create_playlist(title: str) -> dict:
    """Create a private playlist."""
    client = get_client()
    playlist = client.users_playlists_create(
        title=title,
        visibility="private"
    )

    return {
        "title": playlist.title,
        "kind": playlist.kind,
        "visibility": playlist.visibility,
    }


@mcp.tool()
def add_track_to_playlist(
    kind: int,
    track_id: int,
    album_id: int,
) -> dict:
    """Add a track to a playlist using playlist kind and track/album IDs."""
    client = get_client()

    client.users_playlists_insert_track(
        kind=kind,
        track_id=track_id,
        album_id=album_id,
    )

    return {"success": True, "track_id": track_id}


# HTTP application
app = mcp.http_app(path="/mcp")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        expected = f"Bearer {MCP_ACCESS_TOKEN or ''}"
        supplied = request.headers.get("Authorization", "")

        if not MCP_ACCESS_TOKEN or not secrets.compare_digest(
            supplied, expected
        ):
            return JSONResponse(
                {"error": "Unauthorized"},
                status_code=401,
            )

        return await call_next(request)


app.add_middleware(AuthMiddleware)


@app.get("/health")
async def health(request: Request):
    return JSONResponse({"status": "ok", "service": "Sounds"})
