import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from config.settings import PLAYLIST_CONFIG


def save_playlist_config(playlist_id: str, playlist_url: str) -> None:
    path = Path(PLAYLIST_CONFIG)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "playlist_id": playlist_id,
        "playlist_url": playlist_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved playlist configuration to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Configure the Spotify target playlist")
    parser.add_argument("--playlist-id", type=str, help="Spotify playlist ID")
    parser.add_argument("--playlist-url", type=str, help="Spotify playlist URL")
    args = parser.parse_args()

    playlist_id = args.playlist_id
    playlist_url = args.playlist_url
    if not playlist_id:
        playlist_id = input("Playlist ID: ").strip()
    if not playlist_url:
        playlist_url = input("Playlist URL: ").strip()
    if not playlist_url.startswith("http"):
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

    save_playlist_config(playlist_id, playlist_url)


if __name__ == "__main__":
    main()
