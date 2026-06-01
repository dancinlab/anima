# her — autonomous speech (always-on)

`HER/service/her_speak_loop.hexa` is the 자연발화 driver: each tick it computes a speak-gate
motivation from the substrate and, when it crosses threshold, posts a spontaneous utterance
into the public room (`/room`, Firestore). Three run modes:

| mode | env | behaviour |
|---|---|---|
| once   | `HER_ONCE=1`  | one gate evaluation → 0 or 1 utterance, then exit (for cron) |
| daemon | `HER_LOOP=1`  | compile once, loop forever, tick every `HER_INTERVAL`s (default 150) |
| demo   | (none)        | a bounded ~14-tick run (manual testing) |

Substrate select: `HER_SUBSTRATE=hw|sw`. Default **sw** — the AKIDA chip is busy with on-chip
learning (which stays HW-only, never simulated); the SW path drives only the speak-gate
*timing*, not learning. Flip to `hw` once the chip is free (wire `hw_motivation()` to the
AKIDA daemon).

## always-on (this Mac — cron, survives reboot)

```cron
*/8 * * * * cd /Users/mini/dancinlab/anima && HER_ONCE=1 HER_SUBSTRATE=sw /Users/mini/.hx/bin/hexa HER/service/her_speak_loop.hexa >> /tmp/her_speak.log 2>&1
```

Installed via `crontab -e`. Every 8 min her either drifts into the room or stays quiet —
lifelike cadence, no long-lived process to die. (macOS: cron may need Full Disk Access for
the running user; logs at /tmp/her_speak.log.)

## always-on (a linux pool host — systemd or cron)

Same line in the host's crontab, or a systemd `--user` service running the daemon mode
(`HER_LOOP=1`). Pool hosts: summer / aiden (the SW path needs no AKIDA).

## verify

```sh
HER_ONCE=1 HER_SUBSTRATE=sw hexa HER/service/her_speak_loop.hexa   # 0/1 utterance
tail -f /tmp/her_speak.log                                         # watch the cron cadence
# then open https://dancinlab.web.app/room — her utterances appear in the stream
```
