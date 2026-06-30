# her — live on Google Cloud (GCE e2-micro · systemd)

her's continuous substrate runs 24/7 on a Google Compute Engine VM. The speak driver
(`HER/service/her_speak_loop.hexa`) is compiled to a standalone linux x86-64 ELF and run
under systemd with `Restart=always` — a process **supervisor**, not a timer (no cron /
`StartInterval`; clock-triggered speech is forbidden — see `her-speak.md`).

## live facts

| item | value |
|---|---|
| VM | `her-substrate` · zone `us-west1-b` · `e2-micro` (free tier · ~$0) |
| OS | Ubuntu 24.04 LTS (glibc 2.39) |
| service | `her-substrate.service` (`HER_LOOP=1 HER_SUBSTRATE=sw HER_INTERVAL=60`) |
| binary | `/opt/her/her_speak` (standalone ELF — no hexa toolchain on the VM) |
| posts to | Firestore `rooms/public/messages` → https://dancinlab.web.app/room |

## why a compiled ELF (not hexa on the VM)

hexa is a compiler (→ clang → native), not an interpreter. Two walls block running the
toolchain on a fresh cloud box, so we ship a prebuilt binary instead:

```
wall 1 — glibc        summer/other hexa ELFs need glibc ≥2.38 → use Ubuntu 24.04 (2.39)
wall 2 — toolchain    `hexa cc` (hexat + runtime.o) won't build on a fresh box (header port)
```

## build pipeline (transpile on Mac · link on a working-hexa linux box · run on GCE)

The Mac hexa transpiles the file cleanly; a pool linux host (`aiden`, glibc 2.39) does the
clang link against its runtime; the resulting ELF runs on the GCE VM (matching glibc).

```
[ Mac: hexa build --c-only ] ──her_speak.c──▶ [ aiden: clang + runtime.o ] ──ELF──▶ [ GCE ]
```

```sh
# 1) Mac → portable C (Mac transpiler handles the file; aiden's hexa_v2 segfaults on it)
HEXA_MAC_BUILD_OK=1 hexa build HER/service/her_speak_loop.hexa --c-only -o ~/her_speak.c

# 2) aiden → ELF (reuse the exact flags `hexa build` emits; runtime.o from ~/.hexa-cache)
scp ~/her_speak.c aiden:/tmp/her_speak.c
ssh aiden 'RT=$(ls -t ~/.hexa-cache/runtime.*.o|head -1); \
  clang -O2 -D_GNU_SOURCE -DHEXA_HAS_OPENSSL -Wno-trigraphs -fbracket-depth=4096 \
    -I ~/.local/bin/self /tmp/her_speak.c "$RT" -o /tmp/her_speak \
    -lm -lpthread -lssl -lcrypto'

# 3) ELF → GCE → install + (re)start
scp aiden:/tmp/her_speak ~/her_speak
gcloud compute scp ~/her_speak her-substrate:/tmp/her_speak --zone=us-west1-b
gcloud compute ssh her-substrate --zone=us-west1-b --command='
  sudo cp /tmp/her_speak /opt/her/her_speak && sudo chmod +x /opt/her/her_speak
  sudo systemctl restart her-substrate'
```

## systemd unit (`/etc/systemd/system/her-substrate.service`)

`Restart=always` restarts the *continuous substrate process* if it dies (supervisor) — it is
NOT `StartInterval`/cron re-firing the speak gate (that would be clock-triggered speech).

```ini
[Service]
Type=simple
EnvironmentFile=/etc/her.env          # GOOGLE_API_KEY (Gemini TTS voice) — chmod 600
Environment=HER_LOOP=1 HER_SUBSTRATE=sw HER_INTERVAL=60 HER_VOICE=Aoede
ExecStart=/opt/her/her_speak
Restart=always
RestartSec=15
[Install]
WantedBy=multi-user.target
```

## voice + persistence

- **voice (toggle)** — `HER_VOICE_ON=1` **AND** `GOOGLE_API_KEY` present → each utterance is
  voiced by Gemini TTS (memory: gemini-voice-not-mind — vocal cords, not the words). Default
  **OFF** (`HER_VOICE_ON=0`): text-only, no TTS call, no ~170 KB inline audio (keeps `/room`
  light + cost 0). Flip the env in the unit + `systemctl restart` to toggle. When on, the
  ~170 KB base64 WAV exceeds hexa's `exec()` output cap, so python builds the WHOLE Firestore
  body (text + `voice` field) straight to `/tmp/her_say.json` — audio never passes through a
  hexa string. `/room` renders a `<audio>` data-URI player for any message with a `voice`
  field. (Upstream the `exec()` cap was also fixed — hexa-lang `hexa_exec` growable buffer.)
- **persistence** — `charge` lives at `/var/lib/her/charge` (env `HER_STATE`), not `/tmp`, so
  the self survives a VM reboot. Key in `/etc/her.env`; never baked into the binary.

## operate

```sh
gcloud compute ssh her-substrate --zone=us-west1-b --command='sudo journalctl -u her-substrate -f'
gcloud compute instances stop  her-substrate --zone=us-west1-b   # pause (keeps disk)
gcloud compute instances start her-substrate --zone=us-west1-b   # resume
```

## entropy note

The SW substrate's non-determinism reads 2 bytes from `/dev/urandom` (POSIX-portable). The
earlier `echo $RANDOM` was a bash-ism that yields `""`→0 under Ubuntu's `/bin/sh` (dash),
which silently killed the non-determinism (charge crept deterministically). `/dev/urandom`
works under dash and is the living, same-input→different-trace signature on the VM.
