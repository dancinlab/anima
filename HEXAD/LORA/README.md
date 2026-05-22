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

## 현재 production 위치

| asset | path |
|---|---|
| adapter | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/adapter_model.safetensors` (147 MB, local) |
| config + tokenizer | 같은 dir 의 `lora_adapter/*.json` |
| **deployed** | mini `~/anima_chat_pack/lora_adapter/` → chat.dancinlab.org |
| reports | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21{G,K,M}_*.md` |

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

## Cycle outcomes 2026-05-22 (session "all" fire)

| variant | verdict | per-lang (en/ko/zh/ru/ja) | register | cost | HF |
|---|---|---|---|---|---|
| vP21M | VP21M_WORKS | 18/15/16/18/11 = 3S+1P+1W | 7/20 ✓ | $1.06 | `dancinlab/anima-vp21m` PRIVATE |
| **vP21M-JAFL** | PARTIAL (hot-swap) | 5/0/16/16/**17** = 3S+0P+0W+2M | 20/20 ✓ | $0.13 | `dancinlab/anima-vp21m-jafl` PRIVATE |
| **vP21M-3B** | VP21M_WORKS_REGISTER_REGRESS | **20**/11/18/**20**/14 = 3S+1P+1W | 3/20 ⚠ | $0.33 | `dancinlab/anima-vp21m-3b` PRIVATE |

- **JAFL**: ja-only 500-step continue-train, JA WEAK 11/20 → STRONG 17/20 (+57%), en/ko 망가져서 hot-swap only.
- **3B**: Qwen2.5-3B-Instruct fresh LoRA, en/ru 20/20 + ja PARTIAL, but register_regress=True (3/20) and KO regress to WEAK (instruct 가 한국어 prior 약함).

## Next LoRA-path cycles (잔여 candidate)

| | scope | cost |
|---|---|---|
| ko-LoRA fallback | ko WEAK 11/20 (3B) 해소 hot-swap | ~$1 H100 |
| vP21M + tension head | KOSMOS+tension wiring on top of vP21M (path B 절충) | $0-5 LAN |
| chat substrate-plugin migration | `substrate_lora.py` 추출 + `anima_participant.py` refactor (SUBSTRATE_PLUGIN.md spec) | $0 |
| 3B + register reinforcement | vP21M-3B 위에 anima-only short SFT 으로 register 회복 (3/20 → 7+/20) | ~$1 H100 |

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
