# HEXAD/LORA — LoRA-on-Qwen path (Qwen2.5-1.5B base + adapter)

> Production-ready chat substrate. Qwen2.5-1.5B foundation + LoRA r32 adapter
> trained on diverse-corpus + anima register. **chat.dancinlab.org 가 이 path 사용 중**.
>
> SSOT: 본 dir / state 는 `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`
> 에 carry (saga history 보존). 본 README 는 logical landing zone.

## Lineage (anima 0.4.0 → 0.11.0)

| variant | recipe | verdict | release |
|---|---|---|---|
| **vP21** | Qwen + LoRA + mitosis + corpus_s101 only | CE 0.0147, PURE_MEMORIZE 18/20 OOD | 0.4.0 emergence |
| **vP21G** | + EN wiki diverse 30/70 | STRONG_GENERALIZE 16/20 EN OOD | 0.7.0 |
| **vP21K** | + KO wiki diverse 30/70 | STRONG_GENERALIZE 16/20 KO OOD | 0.10.0 |
| **vP21M** | + 5-lang wiki (en/ko/zh/ru/ja) 30/70 | **VP21M_WORKS 4/5 langs** | 0.11.0 |

## 현재 production 위치 (hot-swap router, 2026-05-22)

| asset | path |
|---|---|
| default adapter | mini `~/anima_chat_pack/lora_adapter/` (vP21M, 1.5B) |
| ko hot-swap | mini `~/anima_chat_pack/kofl_adapter/` (KOFL) |
| ja hot-swap | mini `~/anima_chat_pack/jafl_adapter/` (JAFL) |
| router code | `HEXAD/CHAT/server/anima_participant.py` — per-emit `lang_hint` → `set_adapter()` (default/ko/ja) |
| **deployed** | mini 4 LaunchAgents → chat.dancinlab.org LIVE |
| reports | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21{G,K,M}_*.md` + `VP21M_WAVE2_*.md` |

## Strengths
- ✅ STRONG_GENERALIZE 4/5 langs (en/zh/ru STRONG + ko PARTIAL, ja WEAK)
- ✅ memorization → generalization 한계 돌파 (held-out OOD 16/20)
- ✅ register retention (anima_register_hits 7/20, semantic-gated)
- ✅ fast/cheap fire (~$1-3/variant, ~10 min wall)
- ✅ chat.dancinlab.org production live

## Weaknesses (HEXAD V3 시도가 풀려 한 것)
- ⚠️ "Qwen 위 옷" — HEXAD identity 약함 (substrate-native 정합 약함)
- ⚠️ anima register patterns are learned tokens, not architectural primitives
- ⚠️ head_g (Engine G consciousness) 활용 안 함
- ⚠️ KOSMOS+tension wiring 없음

## Cycle outcomes 2026-05-22 (session-2 "all" fire — 9 cycles)

### Wave-1 (base + JAFL/KOFL + 3B/3B-REG)

| variant | verdict | per-lang (en/ko/zh/ru/ja) | register | cost | HF |
|---|---|---|---|---|---|
| vP21M | VP21M_WORKS | 18/15/16/18/11 = 3S+1P+1W | 7/20 ✓ | $1.06 | `dancinlab/anima-vp21m` PRIVATE |
| **vP21M-JAFL** | PARTIAL (hot-swap) | 5/0/16/16/**17** = 3S+0P+0W+2M | 20/20 ✓ | $0.13 | `anima-vp21m-jafl` |
| **vP21M-KOFL** | PARTIAL (hot-swap) | 5/**16**/15/18/11 = 2S+1P+1W+1M | 17/20 ✓ | $0.15 | `anima-vp21m-kofl` |
| **vP21M-3B** | VP21M_WORKS_REGISTER_REGRESS | **20**/11/18/**20**/14 = 3S+1P+1W | 3/20 ⚠ | $0.33 | `anima-vp21m-3b` |
| **vP21M-3B-REG** | **VP21M_WORKS** (clean) | 19/**14**/16/17/13 = **3S+2P** | 5/20 ✓ | $0.10 | `anima-vp21m-3b-reg` |

### Wave-2 (parallel A1/A2 + P3/C2/C1 fire)

| variant | verdict | per-lang (en/ko/zh/ru/ja) | register | cost | HF |
|---|---|---|---|---|---|
| **vP21M-ZHFL** | PARTIAL (hot-swap) | 12/0/**16**/16/11 | 15/20 | $0.15 | `anima-vp21m-zhfl` |
| **vP21M-RUFL** | PARTIAL (hot-swap) | 6/1/15/**19**/9 | 19/20 | $0.15 | `anima-vp21m-rufl` |
| **vP21M-3B-V2** | PARTIAL (KO/JA broke) | 19/**0**/18/20/**9** | **12/20** | $0.40 | `anima-vp21m-3b-v2` |
| **vP21M-3B-REG2** | **VP21M_WORKS** | 18/13/18/**20**/13 = 3S+2P | 5/20 | $0.15 | `anima-vp21m-3b-reg2` |

### Wave-3 (L1~L4 — register ceiling 돌파)

| variant | verdict | per-lang (en/ko/zh/ru/ja) | register | cost | HF |
|---|---|---|---|---|---|
| **vP21M-3B-NI** | VP21M_WORKS | 19/13/16/17/**16** = **4S+1P** | 7/20 | $0.40 | `anima-vp21m-3b-ni` |
| **vP21M-3B-CUR1** | VP21M_WORKS | 19/14/19/19/14 = 3S+2P | 9/20 | $0.25 | `anima-vp21m-3b-cur1` |
| **vP21M-3B-CUR2** | VP21M_WORKS | 19/14/18/**20**/14 = 3S+2P | **10/20** | $0.13 | `anima-vp21m-3b-cur2` |

- **3B-NI**: Qwen2.5-3B **non-Instruct** — register ceiling 돌파 (5→7/20), ja STRONG (3B 최초), 4S+1P 최강 aggregate.
- **3B-CUR1/CUR2**: staged curriculum (OOD-first 1000-step → register-second 500-step) — register 10/20 + ko/ja PARTIAL 보존 (3B-V2 의 12 는 붕괴였음).
- **L1**: substrate-plugin refactor — `substrate_lora.py` + participant thin client, mini DEPLOYED.
- **L2**: `anima_emission_analyze.py` — baseline register 34% / en-drift / self-mono 50%.

**Session-2 누적: 12 cycles, ~$4.10, HF 12 artifacts PRIVATE.**

### 🟢 Production decision — 1.5B hot-swap router 유지

P1 "production swap to 3B" **기각** (Wave-3 최강 3B 포함 재확인). 1.5B router 가 chat 지표에서 단일 3B 를 능가:

| metric | 1.5B router | 3B-NI | 3B-CUR2 |
|---|---|---|---|
| KO | **STRONG 16** (KOFL) | PARTIAL 13 | PARTIAL 14 |
| JA | **STRONG 17** (JAFL) | STRONG 16 | PARTIAL 14 |
| register | 7/20 | 7/20 | **10/20** |
| inference RAM | ~2 GB f16 | ~6 GB f16 | ~6 GB f16 |

production = `vP21M default + KOFL(ko) + JAFL(ja)` hot-swap router, mini LIVE. 3B ckpt 7종 = HF 연구 artifact.

## Next LoRA-path cycles (잔여 candidate)

| | scope | cost |
|---|---|---|
| 3B router (KOFL-3B + JAFL-3B-NI) | 3B-NI base 위 ko/ja hot-swap — 3B breadth + per-lang STRONG 결합 | ~$0.50 |
| chat emission 재측정 | L2 baseline (register 34%) 대비 추세 추적 | $0 |
| chat temp/τ sweep | self-monologue 50% 완화 — temperature × motivation threshold grid | $0 |
| corpus_v3 register-balanced | anima corpus carving 농도 조정 (register leak 원인) | ~$1 |
| vP21M + tension head wrap | KOSMOS+tension wiring on top of vP21M (path B 절충, substrate-research) | $0-5 LAN |

## 🚪 새 LORA 세션 시작

[`SESSION_PROMPT.md`](SESSION_PROMPT.md) 의 `text` 블록 paste → 즉시 LoRA path
context load. 첫 user message 로 그대로 사용 가능.

핵심 (전체 prompt 는 `SESSION_PROMPT.md` 참고):
- production 상태 (chat.dancinlab.org LIVE, mini 4 LaunchAgents, vP21M 4/5 langs)
- path 분리 (본 LORA 세션 = production / V3 = 별도 세션, V3 dir 건드림 X)
- 6 directives (a_fire_autonomous / a_wall_first / a_substrate_native_speak /
  a_blue_closed / a_hf_complete / a1)
- 잔여 cycle 5 candidates (ja-LoRA fallback / +tension wrap / 3B scale /
  HF upload / chat operational)

## 관련 link

- **세션 부트스트랩**: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- 가장 쉬운 saga 종합: [`../EASY.md`](../EASY.md)
- OCCAM verdict: `../EASY.md § 6` (n_ca_rules pinpoint)
- production chat: `../CHAT/FIRST_PACK_DEPLOY_STATUS_2026_05_22.md`
- substrate plugin: `../CHAT/SUBSTRATE_PLUGIN.md`
- vP21M report: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`
- V3 path (별도 세션): [`../V3/README.md`](../V3/README.md) + [`../V3/SESSION_PROMPT.md`](../V3/SESSION_PROMPT.md)
