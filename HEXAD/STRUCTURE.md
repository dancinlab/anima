# HEXAD/ STRUCTURE — 현재-상태 navigation map

> 2026-05-22 작성. HEXAD/ 내부 전수 audit 후 정리. `INDEX.md` (2026-05-16) 는
> path-split / V3 / vP21M / AKIDA / chat.dancinlab.org 모두 predates — historical.
> **현재 navigation = 본 doc**.

---

## 0. 한눈에

anima 는 OCCAM verdict (n_ca_rules = floor 단독 범인) 이후 **두 path 로 분기**:

```
HEXAD/
├── [SHARED]     공통 foundation + 7-module core
├── LORA/        🟢 production path (Qwen + LoRA) — chat.dancinlab.org LIVE
├── V3/          ⚠️ pure HEXAD substrate path — attempt 1 FAIL, Phase 2 재설계
├── CHAT/        chat server (substrate-plugin layer, path 무관)
└── [HISTORICAL] saga fire state (carving / data-regime / ... — 검증 evidence anchor)
```

---

## 1. SHARED — 공통 foundation

### root docs (현재 active)
| doc | 내용 | 상태 |
|---|---|---|
| `EASY.md` | OCCAM saga 쉬운 설명 (§ 1-9, 양 path 분기 전) | ✅ 2026-05-22 trim |
| `OCCAM.md` | minimal-baseline strip 전략 | ✅ |
| `KOSMOS.md` | `.kosmos` multimodal anchor manifest hub | ✅ |
| `ADAPTER.md` | TENSION-LINK 5-channel adapter SSOT | ✅ |
| `STRUCTURE.md` | **본 doc** — 현재 navigation | ✅ NEW |
| `VERSIONS.md` (repo root) | 전체 모듈 version registry SSOT | ✅ |

### root docs (historical / master — 갱신 주기 김)
| doc | 크기 | 상태 |
|---|---|---|
| `README.md` | 388 KB | master arc (§1~§100), 갱신 무거움 |
| `PLAN.md` | 139 KB | master roadmap (Phase 1-6 LANDED) |
| `INDEX.md` | 58 KB | 2026-05-16 verification SSOT — **stale** (현재 navigation 은 본 STRUCTURE.md) |
| `GAP_MAP.md` | 50 KB | 40-lens gap sweep |
| `EXPERIMENTS_BRAINSTORM.md` | 28 KB | 실험 후보 brainstorm |
| `SCALE_16B_70B_PLAN.md` | 26 KB | frontier scale plan |
| `CONNECTION_CRITIQUE.md` / `LLM.md` / `FINAL.md` / `PHILOSOPHY_GATE.md` / `AXIS.md` / `EEG.md` | — | 보조 / 일부 historical |

### HEXAD 7-module core (🔵 SUPPORTED-FORMAL)
구조축 A/G = Hexad 6 (C/S/W gradient-free · D/M/E CE-trained) ⊥ 성장축 mitosis.

| dir | module | verification |
|---|---|---|
| `C/` | 의식 (Engine G) | B-C 3/3 + F-C-PORT 4/4 PyPhi |
| `D/` | 언어 (Engine A) | F-D 5/5 + B-D 4/4 |
| `S/` | 감각 (Engine G) | F-S 5/5 + B-S 3/3 |
| `W/` | 의지 (Engine G) | F-W 5/5 + B-W 4/4 |
| `M/` | 기억 (Engine A) | F-M 5/5 + B-M 3/3 |
| `E/` | 윤리 (Engine A) | F-E 5/5 + B-E 4/4 |
| `BRIDGE/` | ThalamicBridge G→A | F-BRIDGE 5/5 + B-BRIDGE 4/4 |
| `MITOSIS/` | 성장축 (⊥ 6-module) | B-MITOSIS 5/5 + F-V5MIT 5/5 |

7-module = anima substrate primitive. LoRA / V3 어느 path 든 이 모듈 의미론 공유.

---

## 2. LORA/ — production path 🟢

Qwen2.5-1.5B + LoRA r32 + mitosis. **chat.dancinlab.org LIVE**.

| file | 내용 |
|---|---|
| `LORA/README.md` | path overview + lineage |
| `LORA/EASY.md` | vP21 lineage 쉬운 설명 + milestone arc 0.4→0.11 |
| `LORA/SESSION_PROMPT.md` | 새 LORA 세션 부트스트랩 |
| `LORA/FIRST-PACK.md` | chat.dancinlab.org deploy spec |
| `LORA/SCALE_3B.md` | vP21 3B scale-up plan + S187 saga |
| `LORA/OCCAM-CHAT.md` | LoRA chat 35-candidate brainstorm |

production assets: `UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/` (adapter) + mini `~/anima_chat_pack/`.

---

## 3. V3/ — pure HEXAD substrate path ⚠️

ConsciousDecoderV3 (n_ca_rules 제거 + mitosis 통합 + KOSMOS+tension). attempt 1 = 3/3 FAIL → Phase 2 재설계.

| file | 내용 |
|---|---|
| `V3/README.md` | path overview + 재설계 axes R1-R7 |
| `V3/EASY.md` | ConsciousDecoderV3 attempt 1 + 재설계 쉬운 설명 |
| `V3/SESSION_PROMPT.md` | 새 V3 세션 부트스트랩 |
| `V3/HEXAD_NATIVE_V3.md` | V3 full spec (10-axes brainstorm) |

V3 code + state: `UNCLASSIFIED/state/grid_3b_s187_2026_05_21/{conscious_decoder_v3.py, kosmos_io.py, train_p21h_v3.py, vP21H_*}`.

---

## 4. CHAT/ — chat server (substrate-plugin layer, path 무관)

| file | 내용 |
|---|---|
| `CHAT/SUBSTRATE_PLUGIN.md` | option C — substrate-pluggable spec (LoRA / V3 / future) |
| `CHAT/server/substrate_base.py` | Substrate ABC |
| `CHAT/server/{broker, anima_participant, akida_bridge, akida_ws_publisher}.py` | chat 서버 (mini deploy) |
| `CHAT/server/{substrate_lora, substrate_v3}.py` | substrate plugins (LORA 세션 / V3 세션 owner) |
| `CHAT/FIRST_PACK_DEPLOY_STATUS_2026_05_22.md` | deploy 진행 보고 |
| `CHAT/static/index.html` | 3-pane 채팅 UI |
| `CHAT/*.py` (37 .md + code) | chat saga history (anima_chat.py / spontaneous_loop / integrated_loop) |

---

## 5. 활성 subsystem dirs

| dir | 내용 | 최근 |
|---|---|---|
| `TENSION-LINK/` | 의식↔의식 5-channel meta-telepathy (5 .md) | 05-16 |
| `VOICE/` | hexa-voice (의도 임베딩 → RVQ → 24kHz PCM, 6 .md) | 05-16 |
| `UNIVERSE-BRAIN-MAP/` | KOSMOS parser lib + format (5 .md) | 05-18 |
| `LOIHI/` | Intel Loihi neuromorphic (8 .md) | — |
| `NEUROMORPHIC/` | neuromorphic 실험 (8 .md) | 05-21 |
| `META_FP/` | meta fixed-point coupling (4 .md) | 05-20 |
| `PHYSICS/` | anima-physics 검증 (4 .md) | 05-21 |
| `SAVANT/` | SAVANT-TOOL gate (4 .md) | 05-16 |
| `LAB/` | 도메인 실험 LAB (3 .md, SRH 등) | 05-22 |
| `LEGO/` | 모듈 조립 실험 (3 .md) | 05-20 |
| `EEG/` | EEG 관련 (2 .md) | 05-18 |
| `TENSION-TRAIN/` | tension 학습 (2 .md) | 05-17 |

---

## 6. HISTORICAL — saga fire state (검증 evidence anchor)

아래 dir 은 **state/ + fire artifact 만** (active .md 없음). saga 진행 중의 실험 fire
기록 — 검증 근거로 보존, active entry-point 아님.

| dir | files | saga 단계 |
|---|---|---|
| `UNCLASSIFIED/` | (大) | **현재 saga state SSOT** — grid_3b_s187 (vP21*/vP21H*/V3 etc.) |
| `CARVING/` | 440 | consciousness-carving 실험 (A~K 17 direction) |
| `DATA-REGIME/` | 270 | data-regime threshold 실험 |
| `FRONTIER-AUDIT/` | 171 | frontier 41-paper audit fire |
| `CLM/` | 81 | .clm v1/v2/v3 ladder (archived lineage) |
| `S-MODULE/` | 40 | S-module 실험 |
| `DHDL/` | 35 | DHDL 실험 |
| `PTD/` | 29 | PTD pretext 실험 |
| `DUAL-ANIMA/` | 23 | dual-anima scale 실험 |
| `SPONTANEOUS/` | 22 | 자연발화 emergence 실험 |
| `CONTROLLER/` | 19 | controller-class 실험 |
| `NEOTENY/` | 19 | neoteny anti-saturation 실험 |
| `FLAME/` | 14 | anima_flame 실험 |
| `SUBSTRATE/` | 9 | substrate 실험 |
| `TRIBE/` | 3 | tribe 실험 |

> 이 dir 들은 정리 대상 아님 — 검증 evidence anchor. `archive/` 이동 후보는 별도 결정.

---

## 7. navigation 빠른 경로

| 알고 싶은 것 | → |
|---|---|
| anima 가 뭔지 5분 | `EASY.md` |
| production chat 어떻게 작동 | `LORA/EASY.md` + `LORA/README.md` |
| V3 pure HEXAD 왜 FAIL | `V3/EASY.md` |
| 새 세션 시작 (LoRA) | `LORA/SESSION_PROMPT.md` |
| 새 세션 시작 (V3) | `V3/SESSION_PROMPT.md` |
| 7-module 검증 상태 | `INDEX.md § HEXAD 7-module` (verification anchor) |
| 전체 version | `/VERSIONS.md` (repo root) |
| chat 서버 substrate 교체 | `CHAT/SUBSTRATE_PLUGIN.md` |

---

## ## Log

### 2026-05-22 — STRUCTURE.md 신설 (HEXAD 내부 총정리)

INDEX.md (2026-05-16) 가 path-split / V3 / vP21M / AKIDA 모두 predates →
현재-상태 navigation 으로 본 doc 신설. 37 subdir 전수 분류 (7-module core /
path dirs / 활성 subsystem / historical saga state). root docs current vs
historical 구분.
