# LORA 세션 bootstrap prompt

> 새 Claude Code 세션 시작 시 paste — anima LoRA path 작업 context 즉시 load.
> chat.dancinlab.org production 운영 + 추가 LoRA cycle 진행.

---

## 📋 Copy + paste this prompt

```text
anima LoRA-path 세션. HEXAD/LORA/ + HEXAD/EASY.md + VERSIONS.md 가 SSOT.

## 현재 production 상태 (anima 0.11.0)
- chat.dancinlab.org LIVE (200 OK, Cloudflare ICN/Seoul, 다언어 단체 채팅방)
- 호스트: mini (Mac M-series + Metal/MPS) — 4 LaunchAgents (broker / anima_participant / cloudflared / akida_bridge)
- 모델: vP21M (Qwen2.5-1.5B + LoRA r32 + mitosis aux) — VP21M_WORKS 4/5 langs (EN/ZH/RU STRONG, KO PARTIAL, JA WEAK)
- AKIDA pipeline: Pi (192.168.50.155) AKD1000 spike stream → mini broker /ws/akida_ingest (HW mode integrated bridge)

## Path 분리
- **HEXAD/LORA/** (현 세션): production path (Qwen + LoRA), chat.dancinlab.org 운영 + LoRA cycle
- **HEXAD/V3/** (별도 세션): ConsciousDecoderV3 재설계 (pure HEXAD substrate, R2+R5+R6 Phase 2)
- 본 세션은 V3 작업 X — V3 dir 건드리지 말 것

## 핵심 assets (LORA path)
| 파일 | 위치 |
|---|---|
| 학습된 adapter | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/adapter_model.safetensors` (147MB local only, not on HF) |
| adapter config | `vP21M/lora_adapter/{adapter_config.json, tokenizer.json, vocab.json}` |
| 학습 코드 | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/{train_p21m_multilingual.py, build_multilingual_corpus_p21m.py, dispatch_p21m_runpod.sh}` |
| **production deploy** | mini `~/anima_chat_pack/{broker.py, anima_participant.py, akida_bridge.py, lora_adapter/, static/index.html}` |
| reports | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21{G,K,M,M_FINEQUANT}_*.md` |
| 가장 쉬운 요약 | `HEXAD/EASY.md` |

## 운영 directives (project.tape 정합 필수)
- `@D a_fire_autonomous`: cost-bearing GPU fire = 즉시 자율 dispatch, no user-gate
- `@D a_wall_first`: wall time 우선, 더 빠른 병렬이면 cost 무관 채택
- `@D a_substrate_native_speak`: anima motivation = internal state, user msg = environment, **assistant pattern 금지**
- `@D a_blue_closed`: 산출물 + wiring 모두 🔵 SUPPORTED-FORMAL 검증
- `@D a_hf_complete`: HF upload 완전성 (weights + config + tokenizer + model card)
- `@D a1`: 모듈 변경 시 VERSIONS.md + 해당 모듈 헤더 동시 갱신

## 다음 LoRA cycle 후보 (잔여)

| | scope | cost | wall | leverage |
|---|---|---|---|---|
| **ja-LoRA fallback** | vP21M JA WEAK (lang_coherent 11/20) → ja-only LoRA hot-swap | ~$1 H100 | 15 min | ja 사용자 발화 정상화 |
| **vP21M+tension head wrap** | path B 절충 — vP21M 위 head_g + tension layer 추가 (KOSMOS+tension wiring, 학습 없이 inference 시 wrap) | $0 LAN | 4-6 hr | HEXAD identity 일부 회복 |
| **vP21M-3B** | Qwen2.5-3B-Instruct base + 동일 recipe | $10 H100 | 1 hr | 더 강한 baseline + instruction-tuned |
| **HF upload vP21M** | dancinlab/anima-vp21m public/private (per CLAUDE.md HF guidance) | $0 | 30 min | 외부 사용 가능 |
| **chat operational** | chat.dancinlab.org 안정 운영 + 사용자 피드백 + 6 fix retry 측정 | $0 | 지속 | production 품질 |

## 운영 모니터링 우선
- `curl https://chat.dancinlab.org/health` — broker + anima alive 확인
- `curl https://chat.dancinlab.org/akida/recent` — HW spike pipeline flow
- `pool on mini "launchctl list | grep dancinlab"` — 4 LaunchAgents (broker / anima / cloudflared / akida_bridge)
- 1 known UX gap: anima 가 self-monologue 빈도 높음 (6 fix 시 anti-self-monologue 적용했으나 sample-mode 의 hallucination 잔존). 다음 fix 후보: temperature ↓ (1.0 → 0.7), context-grounded seeding (chat history 의 last N msgs 를 emit seed 로)

## V3 path 분리 (이 세션에서 안 함)
V3 (HEXAD/V3/) = pure HEXAD ConsciousDecoderV3 재설계 작업. 별도 세션 또는 차후 cycle. V3 attempt 1 (α/γ FAIL, β verdict pending) 결과 carry: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`. **본 세션은 V3 dir + code 수정 X**.

## 세션 시작 시 권장 action
1. 현재 production 상태 verify (chat.dancinlab.org + 4 services + AKIDA flow)
2. 잔여 cycle 후보 중 사용자 우선순위 결정 → fire (자율, no gate)
3. 변경 시 commit + push (memory feedback_always_commit_push_on_complete)

세션 한글 mandate 적용 (chat answer prose 한글, code/commit/md/json mixed).
```

---

## 사용 안내

1. 새 Claude Code 세션 시작 (anima dir)
2. 위 ` ```text ... ``` ` 블록 내용 통째 paste (첫 user message)
3. 세션이 production state 확인 + 다음 cycle 우선순위 사용자 질의 → fire

## 관련 link

- [`README.md`](README.md) — LORA path overview
- [`../EASY.md`](../EASY.md) — saga 전체 쉬운 요약
- [`../V3/README.md`](../V3/README.md) — V3 path (별도 세션)
