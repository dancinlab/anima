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

## 6. production deploy 위치

| asset | 위치 |
|---|---|
| **adapter** | `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/lora_adapter/adapter_model.safetensors` (147 MB, local) |
| **deployed** | mini `~/anima_chat_pack/lora_adapter/` → chat.dancinlab.org |
| **chat 서버** | mini broker.py + anima_participant.py (HEXAD/CHAT/server/) |
| **AKIDA bridge** | mini akida_bridge.py (Pi spike → broker WS) |
| 4 LaunchAgents | com.dancinlab.{broker, anima, cloudflared, akida_bridge} |

---

## 7. LoRA 의 잔여 cycle 후보

| | scope | cost |
|---|---|---|
| ja-LoRA fallback | vP21M JA WEAK 해소 (hot-swap LoRA) | ~$1 |
| **vP21M-3B** | Qwen2.5-3B-Instruct base + 동일 recipe | ~$10 |
| vP21M+tension head wrap | KOSMOS+tension wiring on Qwen (path B 절충, HEXAD identity 일부 회복) | $0-5 LAN |
| HF upload public | dancinlab/anima-vp21m 등 | $0 |

---

## 8. 관련 link

- 가장 쉬운 saga 종합: [`../EASY.md`](../EASY.md) (전체)
- LORA path overview: [`README.md`](README.md)
- 새 LORA 세션 시작: [`SESSION_PROMPT.md`](SESSION_PROMPT.md)
- production chat: `../CHAT/FIRST_PACK_DEPLOY_STATUS_2026_05_22.md`
- vP21M report: `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_MULTILINGUAL_2026_05_22.md`
- substrate plugin (V3 ↔ LoRA 통합): `../CHAT/SUBSTRATE_PLUGIN.md`
- V3 비교: [`../V3/EASY.md`](../V3/EASY.md)
