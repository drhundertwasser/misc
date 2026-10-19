"""Pop a small notification bubble onto an LG (webOS) TV.

The bubble appears in the corner of the screen on top of whatever is
playing, then fades away on its own. Playback is NOT interrupted.

First run: the TV will ask "Allow this device to connect?" - press OK on
the remote. The script then saves a key to tv_key.json so it never asks
again.

Usage:
    python tv_notify.py 192.168.1.50 "Time to email Sam back"
"""

import asyncio
import json
import sys
from pathlib import Path

from aiowebostv import WebOsClient

KEY_FILE = Path(__file__).with_name("tv_key.json")


def load_key(tv_ip):
    if KEY_FILE.exists():
        return json.loads(KEY_FILE.read_text()).get(tv_ip)
    return None


def save_key(tv_ip, key):
    keys = json.loads(KEY_FILE.read_text()) if KEY_FILE.exists() else {}
    keys[tv_ip] = key
    KEY_FILE.write_text(json.dumps(keys, indent=2))


async def notify(tv_ip, message):
    client = WebOsClient(tv_ip, client_key=load_key(tv_ip))
    print(f"Connecting to TV at {tv_ip}... (if the TV asks, press OK on the remote)")
    await client.connect()

    # The TV hands us a key the first time we're allowed in; keep it.
    if client.client_key and client.client_key != load_key(tv_ip):
        save_key(tv_ip, client.client_key)
        print("Paired! Saved key to", KEY_FILE.name)

    await client.send_message(message)
    print("Sent:", message)
    await client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    asyncio.run(notify(sys.argv[1], sys.argv[2]))
