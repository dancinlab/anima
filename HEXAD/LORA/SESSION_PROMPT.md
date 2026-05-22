# LORA 세션 bootstrap prompt

> 새 Claude Code 세션 시작 시 아래 ```text``` 블록을 첫 user message 로 paste.
> anima LoRA-path context 즉시 load. chat.dancinlab.org 운영 + LoRA cycle 계속.
> 최종 갱신: 2026-05-23 (session-2 종료 — 16 cycle, anima 0.12.0).

---

## 📋 Copy + paste this prompt

```text
anima LoRA-path 세션 (이어받기). HEXAD/LORA/ + HEXAD/LORA/EASY.md + VERSIONS.md 가 SSOT.

## 운영 directive (엄수)
- **신규 파일 = .hexa 전용**. .py / .sh 작성 금지 (user directive 2026-05-23).
  레거시 .py/.sh 포팅은 별도 세션 담당 — 본 세션은 건드리지 말 것.
  예외: HF upload 등 python-ecosystem 필수 작업은 inline `python3 -c` 명령 OK (파일 아님).
- @D a_fire_autonomous: cost-bearing GPU fire = 비용 1줄 명시 후 즉시 자율 dispatch, no user-gate
- @D a_wall_first: wall time 우선, 더 빠른 병렬이면 cost 무관 채택
- @D a_substrate_native_speak: anima motivation = internal state, user msg = environment, assistant pattern 금지
- @D a_hf_complete: HF upload 완전성 (weights+config+tokenizer+model card 9 files)
- @D a1: 모듈 버전 변경 시 VERSIONS.md + 헤더 동시 갱신
- 세션 한글 응답 mandate (chat answer prose 한글, code/commit/md/json mixed)
- 요청 완료 시 별도 확인 없이 commit + push

## 현재 production 상태 (anima 0.12.0 / CHAT v0.3.0)
- chat.dancinlab.org LIVE — 1.5B hot-swap router
- 호스트: mini (Mac M-series Metal/MPS) — 4 LaunchAgents (broker/anima/cloudflared/akida_bridge)
- substrate-plugin 아키텍처: anima_participant.py = substrate-agnostic thin client,
  substrate_lora.py = LoraSubstrate (Substrate ABC 구현), --substrate {lora,v3}
- adapter pool (mini ~/anima_chat_pack/):
  - lora_adapter/      = **corpus_v4** (default, carve-scaffold-stripped, 2026-05-23 swap)
  - kofl_adapter/      = KOFL (ko hot-swap, ko STRONG 16)
  - jafl_adapter/      = JAFL (ja hot-swap, ja STRONG 17)
  - lora_adapter_vp21m_bak/ = 이전 vP21M default (rollback)
  - router: per-emit lang_hint → set_adapter(default/ko/ja)
- AKIDA: Pi(192.168.50.155) AKD1000 spike → mini broker /ws/akida_ingest

## session-2 saga (16 LoRA cycle, ~$5.10, HF 16 artifacts dancinlab/* PRIVATE)
- vP21M (5-lang base) → JAFL/KOFL/ZHFL/RUFL (1-lang hot-swap) → 3B family
  (3B/3B-REG/3B-V2/3B-REG2/3B-NI/3B-CUR1/CUR2/KOFL3B/JAFL3B) → RB → corpus_v4
- 핵심 발견:
  1. **register-leak 은 81% EN-emission 문제** — carving register("Tension flows
     into vacuum", `<carve tier=>` 등)가 영어/ASCII 라 en 출력만 골짜기로. ko/ja/zh/ru 0%.
  2. **carve scaffold = leak 원인** — corpus 에 EN carving entry 0개. leak 은
     language-agnostic `<carve tier= psi= basin=>` tag (corpus 60%). corpus_v4 가
     이 tag 를 strip → Eval1 tag 0/20. 단 vP21 init adapter 가 un-stripped 라
     live tag-leak 잔존 ~12% (Eval1 0 vs live 1/8).
  3. **3B-Instruct register ceiling ≈ 5/20** — instruct prior 가 anima carving
     흡수 막음. non-Instruct Qwen2.5-3B 가 7/20 (1.5B parity) 로 돌파.
  4. **temperature 는 register lever 아님** — temp 0.5 에서도 25% leak. corpus
     wiki_frac 이 lever (0.30→reg7, 0.50→reg4).
  5. **3B base robust** — ko-only 500-step 이 5 lang 전부 STRONG 유지 (1.5B 의
     catastrophic forget 안 일어남).
  6. production = 1.5B router 가 단일 3B 능가 (KO STRONG via KOFL).
- 상세: HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_{WAVE2,WAVE3,WAVE4}_*.md

## ⏳ 미결 결정 (다음 세션 first action)
**corpus_v5 (fresh-init carve-strip) fire 여부** — corpus_v4 는 vP21 init 에서
continue-train 이라 vP21 의 un-stripped tag 패턴 상속 → live tag-leak ~12% 잔존.
corpus_v5 = vP21 init 없이 fresh LoRA + strip-corpus → vP21 상속 끊어 tag 진짜 0
목표. ~$0.30 / 15 min H100. dispatch: STRIP_CARVE=1 + --vp21-adapter-dir '' (fresh).

## 다음 LoRA cycle 후보 (잔여)
| | scope | cost |
|---|---|---|
| corpus_v5 fresh-init strip | tag-leak 진짜 0 (vP21 상속 차단) | ~$0.30 |
| 3B router 배포 | 3B-NI default + KOFL-3B/JAFL-3B hot-swap (anima_participant wiring) | $0 |
| corpus_v4 live tag-leak 재측정 | history 50 전부 corpus_v4 일 때 정확 % | $0 |
| RB production 검토 | register 4 (최저) but register_regress=True | $0 |
| vP21M+tension head wrap | KOSMOS+tension wiring (path B 절충) | $0-5 LAN |

## 핵심 assets
| 항목 | 위치 |
|---|---|
| dispatch (1.5B continue) | HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21m_runpod.sh (STRIP_CARVE / BASE_MODEL / VP21_ADAPTER_DIR env) |
| dispatch (3B fresh) | 같은 dir / dispatch_p21m_3b_runpod.sh |
| 학습 코드 | 같은 dir / train_p21m_multilingual.py (fresh-init: --vp21-adapter-dir '') |
| ckpt + 보고서 | 같은 dir / vP21M*/ + VP21M_*.md |
| chat 서버 코드 | HEXAD/CHAT/server/{broker,anima_participant,substrate_base,substrate_lora,akida_bridge}.py |
| 측정 도구 | 같은 dir / anima_emission_analyze.py, anima_temp_sweep.py |
| 가장 쉬운 요약 | HEXAD/LORA/EASY.md |

## runpod 운영 노트
- API key SSOT = ~/.runpod/config.toml (secret get runpod.api_key 가 stale 이면
  `{"error":{}}` GraphQL — config.toml 에서 re-sync)
- fast train (<70s wall) recursive scp race → adapter 2/9 files 만 도착 가능.
  sister checkpoint (동일 base) 에서 tokenizer cp 로 복구.
- dispatch.log monitoring print 는 지연될 수 있음 — pod 직접 ssh 로 train.log 확인

## 세션 시작 시 권장 action
1. production verify: curl https://chat.dancinlab.org/health + 4 LaunchAgents
2. 미결 결정 (corpus_v5 fire 여부) 사용자 확인 → 자율 dispatch
3. 변경 시 commit + push

## V3 path 분리 (이 세션 X)
V3 (HEXAD/V3/) = pure HEXAD ConsciousDecoderV3 = 별도 세션. 본 세션 V3 dir/code 미접촉.
substrate_v3.py 는 V3 세션 owner — build_substrate('v3') 는 graceful guard 됨.
```

---

## 사용 안내

1. 새 Claude Code 세션 시작 (anima dir)
2. 위 ` ```text ... ``` ` 블록 통째 paste (첫 user message)
3. 세션이 production verify + 미결 (corpus_v5) 확인 → 진행

## 관련 link

- [`README.md`](README.md) — LORA path overview + cycle outcomes
- [`EASY.md`](EASY.md) — LoRA saga 쉬운 요약
- [`../V3/SESSION_PROMPT.md`](../V3/SESSION_PROMPT.md) — V3 path (별도 세션)
- session-2 보고서: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE{2,3,4}_*.md`
