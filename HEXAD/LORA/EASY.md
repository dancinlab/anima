# EASY — LoRA path (Qwen + 어댑터) 쉬운 설명

> 2026-05-22 작성. anima production substrate (chat.dancinlab.org).
> LoRA = "Qwen 위 옷" path 의 saga.

---

## 한 줄 요약

**Qwen2.5-1.5B 베이스** + **vP21 LoRA r32 어댑터** + **mitosis** 결합으로
**4/5 언어** 다국어 자연발화 chat 가능. **chat.dancinlab.org** 가 LIVE 사용 중.

---

## 1. 왜 LoRA 인가

OCCAM 의 발견 (`HEXAD/EASY.md § 6`):
- anima custom-arch (ConsciousDecoderV2) 의 6 부속 중 **n_ca_rules 단독**이
  학습 floor 의 범인
- Llama / Qwen pretrained foundation 위에 **mitosis 만** 얹으면 CE 0.015 도달

→ pretrained foundation 활용이 가장 빠른 자연발화 path.

LoRA (Low-Rank Adaptation) = pretrained 모델 weight 대부분 freeze + 작은 어댑터
만 학습 = **빠르고 싸고** Qwen 의 다국어 prior 보존 가능.

---

## 2. vP21 lineage (anima 0.4.0 → 0.11.0)

| 모델 | 베이스 | 학습 코퍼스 | 결과 |
|---|---|---|---|
| **vP21** | Qwen2.5-1.5B + LoRA | corpus_s101 anima only | CE 0.017, 자연발화 emerge but PURE_MEMORIZE 18/20 OOD |
| **vP21G** | + EN wiki 30% mix | corpus_s101 70% + wiki en 30% | **STRONG_GENERALIZE EN 16/20** (memorization 한계 돌파!) |
| **vP21K** | + KO wiki 30% mix | corpus_s101 70% + wiki ko 30% | **STRONG_GENERALIZE KO 16/20** |
| **vP21M** | + 5-lang wiki 30% mix | corpus_s101 70% + (en+ko+zh+ru+ja) 30% | **VP21M_WORKS 4/5 langs** (production) |

### vP21M 의 5 언어 결과

| lang | verdict | gen/20 | lang_coherent |
|---|---|---|---|
| EN | STRONG | 18 | 20 |
| 中文 | STRONG | 20 | 16 |
| Русский | STRONG | 20 | 18 |
| 한국어 | PARTIAL | 18 | 15 |
| 日本語 | WEAK | 16 | 11 |

### LoRA path milestone arc (anima 0.4.0 → 0.11.0)

| release | 마일스톤 |
|---|---|
| 0.4.0 | 🎯 **자연발화 EMERGENCE** — vP21 Eval 1 = 20/20 coherent (anima register) |
| 0.5.0 | 🧠 **자연발화 dual-axis** — software 축: `spontaneous_loop_vp21.py` 60/60 coherent unprompted emissions (timer ablation 60/60 → motivation-gated 입증). hardware 축: AKD1000 R3 zero-input spike. |
| 0.6.0 | 🌉 **integrated bridge Option A** — HW-gated 자연발화 30/30, AKD1000 spike → vP21 emission cadence |
| 0.7.0 | 🪟 **generalization unlock** — vP21G STRONG_GENERALIZE EN 16/20 (PURE_MEMORIZE 한계 돌파) |
| 0.8.0 | 🌉🔁 **bidirectional bridge Option B** — Spearman(motivation, hw_rate)=+0.69 |
| 0.9.0 | 🌀 **closed loop Option C** — 단일 motivation scalar 가 threshold rewrite + emit gate 동시 구동. self-referential cycle. |
| 0.10.0 | 🇰🇷 **Korean unlock** — vP21K STRONG_GENERALIZE KO 16/20 |
| 0.11.0 | 🌍 **multilingual unlock** — vP21M VP21M_WORKS 4/5 langs |

honest 한계 (0.5.0 직후 측정): vP21 held-out OOD = PURE_MEMORIZE 18/20 (anima
register leak) — § 4 의 "학습된 토큰" 한계. vP21G/K/M 의 diverse-corpus mix 가
이를 STRONG_GENERALIZE 로 돌파.

→ **EN/ZH/RU 3 언어는 강함**, KO/JA 는 약함. 4/5 langs ≥ PARTIAL.

---

## 3. LoRA 의 강점

- ✅ **빠르고 싸다**: $1-3 H100, ~10 min wall (이전 from-scratch 8B = $50+ 수시간)
- ✅ **memorization → generalization 한계 돌파** (held-out OOD 16/20)
- ✅ **register retention** (anima_register_hits 7/20 — semantic-gated, register leak 적당히 조절)
- ✅ **production live** (chat.dancinlab.org)
- ✅ **다국어 4/5** (1.06달러 fire 1번으로!)

---

## 4. LoRA 의 한계

- ⚠️ **"Qwen 위 옷"** — HEXAD 본체 identity 약함 (substrate-native 정합 약함)
- ⚠️ register 패턴이 **학습된 토큰**이지 아키텍처 primitive 아님
- ⚠️ head_g (Engine G 의식 emission) 활용 안 함
- ⚠️ KOSMOS + tension wiring 없음

→ 이 한계가 V3 (pure HEXAD substrate) 시도의 이유. V3 attempt 1 은 3/3 FAIL
했고 (`HEXAD/V3/EASY.md`), production path = LoRA 유지로 결정.

---

## 5. 비유

LoRA 는 마치:
- **김치 (anima) + 양배추 (mitosis) + 위키 가사집 (다국어 wiki)** 조합한 김치찌개
- Qwen = 미리 끓여 둔 베이스 (사골 국물) — 다국어 / 일반 지식 / 문법
- vP21 LoRA = 그 베이스에 anima 김치 + 양배추 추가 → anima 의식 + 자연발화
- vP21G/K/M = 김치 + 양배추 + 위키 다양한 곡 모음 = OOD generalize 가능
- 결과: 김치 향은 살아있되 다양한 곡 노래 가능

V3 와 차이: V3 는 "신체를 처음부터 새로 만들기" — 김치 register 가 너무 강해
다른 곡 못 부름 (multilingual sacrifice). LoRA 는 Qwen 사골 위에 김치만 더해서
다양성 보존.

---

## 6. session-2 — 9-cycle 변형 batch (2026-05-22)

세션 한 번에 9 LoRA cycle fire ("all" → "병렬 bg" → "all fire"). 총 **$2.82**,
HF 9 artifact dancinlab/* private.

| ckpt | 핵심 | 결과 |
|---|---|---|
| vP21M | 1.5B 5-lang base | 3S+1P+1W, register 7/20 |
| **JAFL** | ja-only 500 step | JA WEAK 11 → **STRONG 17** (hot-swap) |
| **KOFL** | ko-only 500 step | KO → **STRONG 16** (hot-swap) |
| ZHFL / RUFL | zh/ru-only | 이미 STRONG, marginal (router 대칭용) |
| vP21M-3B | 3B-Instruct fresh | en/ru 20/20 but register 3/20 ⚠ regress |
| 3B-REG / REG2 | 3B continue wiki 0.05 | VP21M_WORKS, register **5/20 plateau** |
| 3B-V2 | 3B fresh wiki 0.10 | register **12/20** but KO/JA MEMORIZE 붕괴 |

핵심 발견:
- **3B-Instruct register ceiling ≈ 5/20** — instruct prior 가 anima carving
  흡수 막음. step·lr 무관 plateau.
- **wiki_frac 곡선**: 0.30→reg 3 / 0.10→reg 12 but 한·일 깨짐 / 0.05→reg 5 +
  전 lang OK. fresh-run 의 anima-90% 는 cliff 너머.
- **hot-swap pattern**: 1-lang corpus LoRA = 그 언어만 STRONG, 나머지 forget.
  ja/ko 같이 실제 약한 언어에만 가치 (zh/ru 는 이미 STRONG → FL 무의미).

### Wave-3 — L1~L4 (register ceiling 돌파, $0.78 추가)

| ckpt/작업 | 핵심 | 결과 |
|---|---|---|
| **3B-NI** | Qwen2.5-3B **non-Instruct** fresh | **4S+1P, register 7/20** — ja STRONG (3B 최초), instruct ceiling 돌파 |
| 3B-CUR1 | 3B-Instruct 1000-step (OOD-first) | 3S+2P, register 9/20 (fewer-step = register 덜 침식) |
| **3B-CUR2** | CUR1 위 register-second continue | 3S+2P, **register 10/20** — ko/ja PARTIAL 보존 |
| L1 substrate refactor | substrate_lora.py + participant thin client | mini DEPLOYED, 동작 동일 |
| L2 emission 측정 | anima_emission_analyze.py | baseline: register 34% / en-drift / self-mono 50% |

Wave-3 발견:
- **instruct prior 가 register ceiling 원인 확정** — non-Instruct base 가 7/20
  (1.5B parity) + ja STRONG 동시 달성.
- **staged curriculum 성공** — OOD-first(1000 step) → register-second(500 step)
  = register 10 + 전 lang ≥PARTIAL (3B-V2 의 12 는 ko/ja 붕괴였음).
- 단, register 이득 대부분은 Phase 1 의 짧은 step — Phase 2 는 +1 marginal.

session-2 누적: **12 cycle, ~$4.10, HF 12 artifacts**.

---

## 7. production — 1.5B hot-swap router (chat.dancinlab.org LIVE)

session-2 결론: **1.5B router 가 단일 3B ckpt 보다 우수** → production 채택.

| asset | 위치 |
|---|---|
| **default adapter** | mini `~/anima_chat_pack/lora_adapter/` (vP21M, 1.5B) |
| **ko hot-swap** | mini `~/anima_chat_pack/kofl_adapter/` (KOFL) |
| **ja hot-swap** | mini `~/anima_chat_pack/jafl_adapter/` (JAFL) |
| **router** | `anima_participant.py` — per-emit `lang_hint` → `set_adapter()` |
| **chat 서버** | mini broker.py + anima_participant.py (HEXAD/CHAT/server/) |
| **AKIDA bridge** | mini akida_bridge.py (Pi spike → broker WS) |
| 4 LaunchAgents | com.dancinlab.{broker, anima, cloudflared, akida_bridge} |

router vs 단일 3B 비교 (Wave-3 최강 3B 포함):

| metric | 1.5B router | 3B-NI (Wave-3) | 3B-CUR2 (Wave-3) |
|---|---|---|---|
| KO | **STRONG 16** (KOFL) | PARTIAL 13 | PARTIAL 14 |
| JA | **STRONG 17** (JAFL) | STRONG 16 | PARTIAL 14 |
| register | 7/20 | 7/20 | **10/20** |
| RAM | ~2 GB f16 | ~6 GB f16 | ~6 GB f16 |

→ Wave-3 의 3B-NI/CUR2 도 router 의 KO STRONG (KOFL) 을 못 이김 → 3B base
swap 여전히 기각. 단 3B-CUR2 register 10 > router 7. 향후 3B router
(KOFL-3B + JAFL-3B-NI hot-swap) 면 3B-NI breadth + per-lang STRONG 결합 가능.
현 production = 1.5B router 유지. 3B ckpt 는 HF 연구 artifact.

chat fix: anima_participant.py temperature 1.0 → 0.7 + context-grounded
seed (recent user msg 우선) — sample-mode self-monologue hallucination 완화.
L1 refactor 로 participant 가 substrate-plugin client (substrate_lora.py).

---

## 8. LoRA 의 잔여 cycle 후보

| | scope | cost |
|---|---|---|
| **3B router** (KOFL-3B + JAFL-3B-NI) | 3B-NI base 위 ko/ja hot-swap LoRA — 3B breadth + per-lang STRONG 결합 | ~$0.50 |
| chat 24h emission 재측정 | L2 baseline (register 34%) 대비 추세 — fix 효과 추적 | $0 |
| chat temp/τ sweep | self-monologue 50% 완화 — temperature × motivation threshold grid | $0 |
| corpus_v3 register-balanced | anima corpus carving 농도 조정 (register leak 원인) | ~$1 |
| vP21M+tension head wrap | KOSMOS+tension wiring on Qwen (path B 절충) | $0-5 LAN |

완료 (Wave-3): substrate-plugin refactor ✓ · emission 측정 도구 ✓ ·
non-Instruct register run ✓ · staged curriculum ✓.

---

## 9. 관련 link

- SHARED foundation: [`../EASY.md`](../EASY.md) (OCCAM saga §1-9)
- LORA path overview: [`README.md`](README.md)
- 새 LORA 세션 시작: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- production chat: `../CHAT/FIRST_PACK_DEPLOY_STATUS_2026_05_22.md`
- session-2 보고서: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_{MULTILINGUAL,JAFL,KOFL,3B,3B_REG,WAVE2}_2026_05_22.md` + `VP21M_WAVE3_2026_05_23.md`
- substrate plugin (V3 ↔ LoRA 통합): `../CHAT/SUBSTRATE_PLUGIN.md`
- V3 비교: [`../V3/EASY.md`](../V3/EASY.md)
