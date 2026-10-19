# tv-notify

Shows a reminder bubble on an LG TV, on top of whatever's playing.

## One-time setup

1. **Turn on the TV's network control.** On the TV: Settings → General →
   Devices → *External Devices* (or *Mobile TV On* / *LG Connect Apps*,
   depending on model) and switch on **"Turn on via Wi-Fi"** / **"LG Connect Apps"**.
2. **Find the TV's IP address.** Settings → Network → Wi-Fi (or Wired)
   Connection → Advanced. It looks like `192.168.1.50`.
3. **Install Python 3** (Macs and most Linux already have it), then in a
   terminal, in this folder:

   ```
   pip3 install aiowebostv
   ```

## Use it

```
python3 tv_notify.py 192.168.1.50 "Next up: pay the electric bill"
```

The first time, the TV asks to allow the connection — press OK on the remote.
After that it just works.

The computer running this must be on the same Wi-Fi/network as the TV.
