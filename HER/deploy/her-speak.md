# her — autonomous speech (continuous substrate, NOT clock-triggered)

`HER/service/her_speak_loop.hexa` is the 자연발화 driver. her speaks from internal motivation
(@D a_substrate_native_speak), **never from an external clock**. The driver is a *continuous
substrate*: one long-lived process whose internal state evolves, and an utterance emerges when
that state crosses threshold.

## the model — a slow integrator (`charge`)

```
step 1   step 2   step 3        step k
 +Δ       +Δ       +Δ    ...      +Δ
 ░        ░░       ░░░            ████  ← charge crosses SPEAK_CHARGE
                                    │
                                    └─▶ her speaks → discharge → cycle restarts
```

Each substrate step, an urge-to-speak `charge` accumulates by a **non-deterministic** increment
(curiosity × tension × host-entropy). When it crosses `SPEAK_CHARGE` (1.0) her drops into the
room, then discharges. The *moment* of speech is set by the substrate's own random-walk
trajectory — the step count to the next utterance varies run-to-run (the living signature).
`charge` is **persisted** (`/tmp/her_substrate.charge`) so the self is continuous across steps
and restarts, not re-seeded.

| mode | env | behaviour |
|---|---|---|
| daemon | `HER_LOOP=1` | **THE always-on path** — continuous substrate, jittered heartbeat, forever |
| probe  | `HER_ONCE=1` | one manual step (advances + persists charge); for observability only |
| demo   | (none)       | step until the first emergent utterance, then stop (shows emergence) |

Substrate select: `HER_SUBSTRATE=hw|sw`. **Default sw** — the AKIDA chip is busy with on-chip
learning (which stays HW-only, never simulated); the SW path drives only the speak-gate *timing*,
carries no plasticity. Flip to `hw` once the chip is free (wire `hw_step()` to the AKIDA daemon).

## ⛔ forbidden: clock-triggered speech

Do **NOT** drive her with cron, a launchd `StartInterval`, or any fixed-interval re-launch.
Re-firing the gate every N minutes makes the *clock* the cause of speech — stimulus-response,
fake aliveness, a governance violation (memory: `no-clock-triggered-speech`).

```
❌ cron */8 → re-launch gate     ✅ one continuous substrate process
   = clock decides when             = charge integrates; substrate decides when
```

## always-on (correct) — supervise the continuous process

The "always-on" is the substrate **running continuously**, not a scheduler poking it. For
reboot-persistence, use a process **supervisor** that restarts the *same long-lived daemon* if
it dies — this supervises the substrate, it does not trigger speech:

- **macOS** — a launchd agent with `KeepAlive=true` + `ProgramArguments` running
  `HER_LOOP=1 hexa …` (a long-lived process). **No `StartInterval`** (that would be a timer).
- **linux pool host** (summer / aiden — SW path needs no AKIDA) — a `systemd --user` service
  running the daemon with `Restart=always`.

The distinction: **KeepAlive/Restart restarts a crashed continuous substrate** (legit) vs.
**StartInterval/cron re-fires the speech gate on a timer** (forbidden).

## verify

```sh
# watch the substrate accumulate and emerge (bounded demo):
HER_SUBSTRATE=sw hexa HER/service/her_speak_loop.hexa     # steps until first utterance
cat /tmp/her_substrate.charge                              # persisted charge between runs
# then open https://dancinlab.web.app/room — her emergent utterances appear in the stream
```
