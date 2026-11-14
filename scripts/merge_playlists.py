#!/usr/bin/env python3
"""Merge the three iptv-org public playlists and remove duplicate channel names."""
from __future__ import annotations

import re
import unicodedata
from urllib.request import Request, urlopen

SOURCES = [
    ("Saudi", "https://iptv-org.github.io/iptv/countries/sa.m3u"),
    ("Sports", "https://iptv-org.github.io/iptv/categories/sports.m3u"),
    ("Arab", "https://iptv-org.github.io/iptv/regions/arab.m3u"),
]

def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Saudi-Arabic-Sports-IPTV/1.0"})
    with urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8-sig", errors="replace")

def channel_key(extinf: str) -> str:
    display_name = extinf.rsplit(",", 1)[-1].strip()
    # Prefer the visible channel name; remove common quality suffixes.
    display_name = re.sub(r"\b(4k|uhd|fhd|hd|sd|1080p|720p|576p|480p)\b", " ", display_name, flags=re.I)
    display_name = unicodedata.normalize("NFKD", display_name)
    display_name = "".join(c for c in display_name if not unicodedata.combining(c))
    display_name = display_name.casefold()
    display_name = re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", display_name)
    return display_name

def parse(text: str):
    lines = [line.strip() for line in text.replace("\r", "").split("\n") if line.strip()]
    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U"
    entries = []
    current = []
    for line in lines[1:] if lines and lines[0].startswith("#EXTM3U") else lines:
        if line.startswith("#EXTINF"):
            if current:
                current = []
            current = [line]
        elif current:
            current.append(line)
            if not line.startswith("#"):
                entries.append(current)
                current = []
    return header, entries

def main():
    seen_names = set()
    seen_urls = set()
    output = [
        '#EXTM3U',
        '#PLAYLIST:Saudi + Arabic + Sports (deduplicated)',
        '# Generated automatically from iptv-org public playlists',
    ]
    counts = {}
    for label, url in SOURCES:
        _, entries = parse(fetch(url))
        added = 0
        for entry in entries:
            extinf = entry[0]
            stream_url = next((x for x in entry[1:] if x and not x.startswith("#")), None)
            if not stream_url:
                continue
            key = channel_key(extinf)
            if not key or key in seen_names or stream_url in seen_urls:
                continue
            seen_names.add(key)
            seen_urls.add(stream_url)
            output.extend(entry)
            added += 1
        counts[label] = added
    if not seen_urls:
        raise RuntimeError("No valid streams were found; refusing to overwrite playlist.")
    with open("playlist.m3u", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(output) + "\n")
    print(f"Playlist generated: {len(seen_urls)} unique channels")
    print("Added by source: " + ", ".join(f"{k}={v}" for k, v in counts.items()))

if __name__ == "__main__":
    main()
