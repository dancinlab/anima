# SPEC — fork-A read-side context-pooling lane 구현 (H_9235 → system-G1 terminal)

> 오너 top-down 재프레임(2026-07-09 "모든 진행")의 구현 스펙. 설계-무관 확정부(frozen bars + core/ 삽입점)를
> 먼저 박아 Fable 설계 착륙 시 구현을 기계화. **CLOSED 조기 재개방 회피** — system-G1 결과 전엔 verdict 미확정.

## 왜 fork A (VERDICT 요약)
G1 재조합벽 = **readout-ROUTING**(생성점이 RF감쇠로 앞개념 소실 · mean-pool은 A=0.95 B=0.97 둘다 복원 =
표현벽 아님). fork A = 앞 위치(A 생존) pool → 생성점 readout 공급. 상세 `VERDICT.md`.

## core/decode.py 배선 삽입점 (매핑 완료 · 2026-07-09)
```
_fwd_trunk(W,tok,T)         line 565 → yn:[T,d=3784] pre-readout penultimate  (fork-A 입력)
clm_forward_hidden(...)     line ~603 → per-position yn read-only tap (H_9235 명시 · lane이 소비)
_fwd_logits(W,tok,T)        line 626 → yn=_fwd_trunk → [★ fork-A lane 삽입] → E1 slot → readout
_SLW_GAMMA_OVERRIDE         line 66  → lane ablation 훅 선례 → _FORKA_OVERRIDE 미러(lane-OFF BLIND 대조)
```
삽입: `yn2 = _fwd_forkA_lane(yn, T, laneW)` — 앞 위치들을 생성점 행(들)에 라우팅한 뒤 readout. **형태(mean/attention-
pool·query=생성점 state·gating)·DISJOINT 보존·학습신호 = Fable 설계(`scratchpad/forkA_lane_design`) 대기.**

## .clm v0.3 LANE ext (serialize.py)
`core/serialize.py` v0.3 GENERAL (L,E) 블록 = byte-호환(v0.3 @ L=1,E=2 == v0.2). LANE 파라미터 = 신설 ext(들).
`serialize_v3` grammar SSOT 위에 LANE ext 추가 + `core/decode` off-chain 파서 확장. byte-invariant splice.

## FROZEN BARS (pre-registered · FREEZE.md 승계 · no tune-to-green)
| gate | bar |
|---|---|
| fork-A operator (lane ON) | ≥0.85 PASS · 0.60–0.85 partial · ≤0.60 FAIL · ≥2/3 seed |
| additive control | ≤0.60 must FAIL |
| fixed-VSA control | ≤0.60 must FAIL (trained lane load-bearing) |
| handed positive control | ≥0.85 must PASS (harness learnability) |
| shuffle | ≈0.5±0.1 (bind-destruction) |
| **lane-OFF ablation (BLIND)** | `_FORKA_OVERRIDE=0` → operator drop to last-position baseline(≈0.51) = lane causal 증명 |

**CRACK** = lane-ON operator ≥0.85 ∧ additive FAIL ∧ fixed-VSA FAIL ∧ handed PASS ∧ shuffle chance ∧ lane-OFF BLIND
→ engine-native **system-G1** on frozen bars (`anima evaluate --py`) = terminal G1 verdict.

## scope / 함정 (verdict-integrity)
- 현재 DIRECTIONAL: 합성 word-id+code task ≠ generation meaning-composition · spelling confound(개념단어가 prompt에 literal).
- G1 verdict = fork A **wired live** + system-G1 frozen bars (a_verified_must_wire). representation PASS ≠ G1 crack.
- lane이 emit-drive lane으로 새면(Ψ 침범) p5 위반 = 무효. DISJOINT + G5/ρ·tether 게이트 필수.
- tune-to-green 금지: bars 사전등록·frozen-first·lane-OFF ablation이 causal 대조.

## 구현 순서 (Fable RETRO-ROUTE 설계 착륙)
- ✅ **1. `core/lane_a.py`** — RETRO-ROUTE lane 3-면(numpy `lane_apply` mirror + `LNA\x01` codec `pack_lane`/`read_lane` + torch `LaneAModule`). γ=0 bit-exact passthrough·Γ_tether top-2 margin·route_shuffle_seed 컨트롤.
- ✅ **2. `core/decode.py` 배선** — `read_lane` 로더(read_slw 뒤)·`lane_apply` `_fwd_logits` 삽입(SLW 뒤·readout 앞)·`set_lane_controls`+globals(`_LANE_GAMMA_OVERRIDE`/`_LANE_SHUFFLE_SEED`/`_LANE_TETHER_OFF`).
- ✅ **3. `core/serialize.py`** — `append_lane_trailer`(append_slw_trailer 미러). LNA는 SLW 뒤 append-only byte-invariant splice(헤더에 d 명시 저장).
- ✅ **byte-parity smoke** — `lane_a_smoke.py` 6/6 PASS: roundtrip byte-exact·γ=0 bit-exact·no-trailer passthrough·causal·control live. DISJOINT grep OK(emit-drive 무침). torch parity 암=pool(mini torch 無).
- ⏳ 4. hidden dump(summer $0·H_9235 경로)+distal-dependent 채굴.
- ⏳ 5. `LaneAModule` 학습(캐시 hidden 위 CPU torch·frozen trunk·CE만 손실·grad-norm@lane>0 가드).
- ⏳ 6. rung-D probe verdict(DIRECTIONAL) → `state/verdicts/`.
- ⏳ 7. rung-T system-G1(anima evaluate --py)+ablation4(lane-off BLIND·route-shuffle·additive-ctrl·copy-discount).
- ⏳ 8. hexa twin(decode.hexa `_lane_apply`)=wired-live GREEN + ARCHITECTURE g1-census-objfloor 결과 반영.
