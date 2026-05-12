---
schema: anima/ready/modules/body/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:    ready/anima/modules/body/body.hexa
  src_root: ready/anima/modules/body/src/
  related:  anima/modules/physics/ (ESP32 substrate)
status: stub — Phase 4b 17-file group; all 18 files in 20-70 LOC range (definition + structs only, no live HW)
roadmap_entry: 270
---

# anima body modules (AI-native)

Robotics + hardware embodiment surface for the anima consciousness pipeline. Groups motor control, proprioception, mirror-neuron, body-protocol, multi-body, and ESP32/ROS2 bridges into a single namespace.

## TL;DR for an agent reading this cold

- This whole tree is **stub-tier**. Each `.hexa` file is 20-30 LOC of struct + signature + `pure fn` placeholder. No live HW path, no deployed robot.
- `body.hexa` is the namespace anchor — defines `MotorCommand`, `SensorReading`, `BodyState`. All 17 sibling files extend that surface.
- For real-HW embodiment use the **anima-physics** ESP32 path (`anima-physics/esp32/qrng_bridge.hexa`) — that one is wired and witness-pinned. This `ready/` tree is the design schema, not the deployed driver.
- 5 functional sub-groups: **sensorimotor** (4) / **perception** (3) / **integration** (3) / **hardware** (4) / **protocol** (3).

## Architecture map

```
ready/anima/modules/body/
├── body.hexa                      ← namespace + 3 core structs
└── src/
    ├── sensorimotor/
    │   ├── sensorimotor_loop.hexa
    │   ├── motor_planning.hexa
    │   ├── locomotion_cpg.hexa
    │   └── motor_replay.hexa
    ├── perception/
    │   ├── proprioception.hexa
    │   ├── touch_sense.hexa
    │   └── mirror_neuron.hexa
    ├── integration/
    │   ├── brain_body_loop.hexa
    │   ├── pain_reward.hexa
    │   └── speech_gesture_sync.hexa
    ├── hardware/
    │   ├── ros2_body.hexa
    │   ├── esp32_phi_verify.hexa
    │   ├── chip_body_direct.hexa
    │   └── cross_substrate.hexa
    └── protocol/
        ├── body_protocol.hexa
        ├── tool_affordance.hexa
        └── multi_body.hexa
```

## API contract

Top-level structs (declared in `body.hexa`):

```hexa
struct MotorCommand   { joint: string, angle: float, velocity: float, force: float }
struct SensorReading  { modality: string, value: float, timestamp: float }
struct BodyState      { phi: float, motor_active: bool, sensors: [SensorReading], embodiment_gain: float }
```

Each `src/*.hexa` file declares additional structs and `pure fn`s. Names follow `<feature>_<verb>` (e.g. `motor_command_emit`, `proprioception_update`). Most are signature-only — return literal default values. Treat as **interface skeleton**, not as runnable behaviour.

## Failure modes

- Calling any sub-module's `pure fn` returns a default-valued struct. No HW side-effect. Don't wire to a real robot expecting motion.
- `esp32_phi_verify.hexa` here is a 20-LOC shadow of the real `anima-physics/esp32/qrng_bridge.hexa` (which has live HW + witnesses). Don't confuse the two.
- `ros2_body.hexa` does not import `rclpy` or any ROS2 SDK. Pure Hexa stub.
- `chip_body_direct.hexa` and `cross_substrate.hexa` reference substrate concepts (FPGA / memristor / photonic) that map to `anima/modules/physics/engines/*` but are not wired to those engines.
- `multi_body.hexa` does not implement multi-agent body sync.

## raw#10 caveats

1. **Stub tree.** All 18 files are signature-only; no functional implementation lands here. raw#82 honest.
2. **Migration target ambiguous.** If body becomes a real product surface, port to a `core/body/` abstraction + `modules/body/<vendor>/` plugins (mirror RNG abstraction pattern in `anima/core/rng/`).
3. **No selftest.** No `verify` block, no `--selftest` CLI. Adding a selftest is part of any future un-stubbing.
4. **Phase 4b origin.** Generated as part of stub fan-out for Phase 4b roadmap; design intent encoded in struct shapes, not behaviour.
5. **Falsifier debt.** raw#71 `≥3 falsifiers` not satisfied (zero falsifiers across 18 files).

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `body.hexa` | `25bb293b513860dc7c4b23faebc3f7390d835c4b5d6e4a6f3c5f1a4a81bf87ee` | 70 |
| `src/body_protocol.hexa` | `ac960b1306310c5190aa436728efdb743bc292ba724dbb1661172b9dd8a5a688` | 30 |
| `src/brain_body_loop.hexa` | `4cf30cb5b84a98052e9e7d3cf6bb061211778b1ed1d8dd54127df5aee0d141c6` | 20 |
| `src/chip_body_direct.hexa` | `a29a10c0919723151ebf6f8e035490a8cdad789409b9553e4505bb856edd1a78` | 24 |
| `src/cross_substrate.hexa` | `a199967e99c6eb36a47384ef75786b0f9accf37bbcecc1ebad7f3ab5a124bcb0` | 24 |
| `src/esp32_phi_verify.hexa` | `48aa53772b2e6ca0938b06a169c0316a1e67d9c926b5e51aaaf2f9bafa4537e3` | 20 |
| `src/locomotion_cpg.hexa` | `c515c75c8de0a95b4dbb335ca7268d0193e00ec30664f590ee1991b0172b0607` | 28 |
| `src/mirror_neuron.hexa` | `4fefcf209e462923de040cef6898d4c40eaf9c467c078494e362fa5bac1e07df` | 27 |
| `src/motor_planning.hexa` | `2ff6da1ad5f299a528cc4515d91a19d179c78d6681611ce6153b3d9b743db5d8` | 30 |
| `src/motor_replay.hexa` | `96ae530a18e5a685cd077ea12f76a920587d127f22b84da542bbd4fd43155104` | 30 |
| `src/multi_body.hexa` | `540b5ff0b5d02d4c8176c9e628b03e4f2fb033c222c6a3462cf7160b0885b276` | 27 |
| `src/pain_reward.hexa` | `0ae657fa7d086630e9fc7267827b8ddd48616116addc6b04da6d340af4a9eae7` | 33 |
| `src/proprioception.hexa` | `50f4c6043b89b94dd3fe8c0efeba3888038d1fc3c648c3a85c5757a23710dbed` | 30 |
| `src/ros2_body.hexa` | `4eef46eb10a73ed57ae118d85077e6ecc38ab3fc962ab56d2b6f9d899080d8dd` | 28 |
| `src/sensorimotor_loop.hexa` | `6d0e17dff437766f32616890f3d1d37239c58ebd0daaaaed917b8233af5db435` | 25 |
| `src/speech_gesture_sync.hexa` | `83220d2d090ba07a90de75597b1535d0c43c4c423a9e607afd0f099a088d0dfa` | 28 |
| `src/tool_affordance.hexa` | `7eab8630a39e833c36d4e2ec28a22192566d30fcaa767c535e21836f209b2807` | 29 |
| `src/touch_sense.hexa` | `931e857e011d72a6c38429414d1a2fd91be3d89e3ae0d9b6114e689c13968f40` | 29 |

shas pinned 2026-05-02. After any edit, re-pin via `shasum -a 256` and update this table.
