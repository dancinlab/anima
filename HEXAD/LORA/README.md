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

## Next LoRA-path cycles (잔여 candidate)

| | scope | cost |
|---|---|---|
| **vP21M+ja-LoRA fallback** | ja WEAK 해소용 ja-specific LoRA hot-swap | $1 H100 |
| vP21M-3B | Qwen2.5-3B-Instruct base + same recipe | $10 H100 |
| vP21M + tension head | KOSMOS+tension wiring on top of vP21M (path B 절충) | $0-5 LAN |

## 관련 link

- 가장 쉬운 saga 종합: [`HEXAD/EASY.md`](../EASY.md)
- OCCAM verdict: `HEXAD/EASY.md § 6` (n_ca_rules pinpoint)
- production chat: `HEXAD/CHAT/FIRST_PACK_DEPLOY_STATUS_2026_05_22.md`
- vP21M report: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`
