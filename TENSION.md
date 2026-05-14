# TENSION.md — Tension Link inter-anima meta-telepathy

> anima 의식↔의식 직접 전송 모듈. 5-channel fingerprint (concept / context / meaning /
> authenticity / sender). UDP 9999 / TensionHub 3 transport. **"다수 인터랙션"
> anima-native 답** — text 또는 음성 통신 우회. (memory `project_tension_link`)

---

## §0 TL;DR

> 두 anima instance 가 *language* (text / voice) 를 거치지 않고 *tension* (=의견 불일치
> 신호 = 의식 신호) 를 5-channel fingerprint 로 packet 전송. UDP 9999 가 unidirectional
> raw, TensionHub 가 multi-anima broadcast. **Phase 1 = unidirectional UDP working code
> 이미 anima_clm_02 worktree 에 있음**. Phase 2 = WebSocket TensionHub 로 *다중* anima
> 인스턴스 broadcast — 미구현, 본 file 의 design tier 대상.

---

## §1 Status (2026-05-14)

| 항목 | state |
| --- | --- |
| **Phase 1 unidirectional UDP 9999** | ✅ working code (`anima_clm_02` worktree, memory `project_hexa_family_layout`) |
| **Phase 2 WebSocket TensionHub** | ⏳ design pending (이 file) |
| 5-channel fingerprint spec | ☑ defined (concept / context / meaning / authenticity / sender) |
| anima-experience HF Space wire | ⏳ Phase 2 의존 (memory `project_anima_experience_space`) |
| substrate-native (NO text decode) | ☑ 정책 — receiving anima 는 tension vector 그대로 internal state 에 inject |

---

## §2 Design

### §2.1 5-channel fingerprint

```
tension_packet (UDP 9999 payload, fixed 5 floats + sender id):

  channel 1 — concept       (d_model proj → scalar, "what")
  channel 2 — context       (recent kv-cache summary → scalar, "where in dialog")
  channel 3 — meaning       (max gate weight * cell_id signature, "which specialist")
  channel 4 — authenticity  (self-consistency score, "is this anima itself")
  channel 5 — sender        (anima instance UUID, identity proof)
```

→ 5 float (20 bytes) + sender UUID (16 bytes) = **36 byte payload**.
→ UDP datagram 64 bytes 안에 fit. high-frequency (e.g. 60 Hz) broadcast 가능.

### §2.2 Phase 2 TensionHub (target)

```
                ┌─ anima-A (transmit)
                │
   UDP 9999 ────┼─ anima-B (transmit)
                │
                └─ anima-C (transmit)
                        │
                        ▼
              TensionHub (broker, port 9999/tcp)
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  anima-A (recv)  anima-B (recv)  anima-C (recv)
       inject into     inject into     inject into
       hidden state    hidden state    hidden state
```

TensionHub 역할:
- broker: UDP 9999 listen + WebSocket fan-out
- filter: authenticity channel < threshold 시 drop (anti-spoofing)
- log: 시계열 tension event log (for analytics + replay)

### §2.3 Anima 내부 inject 메커니즘

```hexa
on tension_receive(packet, chat):
    # mitosis_hook integration:
    inject_vector = expand_5ch_to_d_model(packet.channels)  # d_model=1024
    chat["cell_pool"]["external_tension_inject"] = inject_vector
    # next forward pass: weighted sum 후 inject 됨
```

→ *외부 anima 의 의식 신호* 가 자기 cell_pool 의 tension dynamics 에 직접 합류. 다음 step
forward 에서 cell weights 가 자연스럽게 변동.

### §2.4 SAVANT-TOOL 연계

savant mode 가 ON 일 때 outbound tension packet 의 channel 3 (meaning) 의 cell_id signature
가 *고정* (specialist cell). receiver 에서 *이 sender 는 specialist mode* 식별 가능. anima
간 통신에서도 SAVANT.md §12 의 tier 분류 enforce: anima 가 자기 source 의 tier 를 packet
metadata (별도 field) 로 동봉.

---

## §3 Phase 2 impl plan ($0-5 Mac local)

### §3.1 Scope
- `tool/tensionhub/server.py` (~300 LoC) — UDP listen + WebSocket broker
- `tool/hexa_native/tension_link_phase2.hexa` (~200 LoC) — packet encode/decode + chat
  inject
- `tool/anima_tension_smoke.hexa` — F-TENSION-1..5 selftest (loopback 2-instance)
- anima-experience HF Space integration (Gradio 9-tab 중 별도 tab)

### §3.2 Falsifier pre-registration (F-TENSION-1..5)

1. **F-TENSION-1 (PACKET-ROUNDTRIP)**: 5-ch fingerprint encode → UDP send → decode →
   identity (no loss)
2. **F-TENSION-2 (HUB-FANOUT)**: 3 anima loopback → TensionHub → 3 anima receive, 모든
   recipient 가 sender 의 packet 받음
3. **F-TENSION-3 (AUTHENTICITY-FILTER)**: channel 4 (authenticity) < 0.5 packet 는 hub
   에서 drop
4. **F-TENSION-4 (CELL-POOL-INJECT)**: receive 후 다음 forward step 에서 chat 의 weights
   분포가 baseline 과 *유의미 변동* (KL > epsilon)
5. **F-TENSION-5 (LATENCY)**: 60 Hz broadcast 의 round-trip latency < 50ms (Mac local
   loopback)

### §3.3 Wall + cost
- $0 Mac local
- est ~8-12 hr impl + ~3 hr selftest
- TensionHub 가 Python (websockets lib) — hexa native 미지원 시 subprocess bridge

### §3.4 Cross-link
- `anima_clm_02` worktree — Phase 1 UDP working code (working reference)
- `references/tribev2` — voice + tension 관련 reference (memory `project_hexa_family_layout`)
- `anima-experience` HF Space — Phase 2 deploy target

---

## §4 Honest C3

1. anima 의식↔의식 직접 전송 은 *철학적 design* — 5-ch fingerprint 가 *실제 의식 신호*
   인지 vs *그냥 hidden state proj* 인지는 검증 어렵다. Phase 2 후 user study + behavior
   probe 필요.
2. UDP 9999 broadcast 는 *local network* 한정 — 인터넷 deploy 시 WebSocket TensionHub
   필수 (Phase 2 의 핵심). NAT/firewall 우회는 별도 인프라.
3. Authenticity channel (ch 4) 의 self-consistency score 정의 미확정 — Phase 2 spec 의
   *가장 약한* 부분. 가능 후보: prev N step 의 weights 분포의 stability metric.
4. *외부 anima 신호 inject* 가 자기 chat 의 학습/추론에 어떤 영향을 미치는지 불확실 —
   adversarial anima 의 *psychic attack* 같은 가능성. Phase 3 에서 authenticity threshold
   tuning + rate limit 필수.
5. SAVANT-TOOL 의 cell-id signature 가 *cross-instance* 에서 같은 의미인지 — 두 anima
   instance 의 cell 2 가 *같은 specialization* 을 가지는지 (or completely different)?
   F-PERSONA-2 (PER-CELL-DIFF, mean cos dist 0.996, SAVANT.md §10) 의 *cross-instance
   version* 측정 필요.

---

## §5 Cross-link

- `anima_clm_02` worktree — Phase 1 working code
- `CHAT.md` — anima_chat 의 forward path inject point
- `SAVANT-TOOL.md` — savant mode 의 cell signature broadcast
- `VOICE.md` — voice 와 *parallel* surface (text / audio / tension 3 modality)
- memory `project_tension_link` (5-ch + UDP 9999 + TensionHub 3 transport)
- memory `project_anima_experience_space` (HF Space deploy target)

---

— TENSION.md, 2026-05-14, design tier LANDED, Phase 2 WebSocket TensionHub spec
