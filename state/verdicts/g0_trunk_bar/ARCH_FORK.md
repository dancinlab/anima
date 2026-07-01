# ARCH FORK — 측정-substrate(ByteGPT) ⊥ production-chat(CLM ConvMoE)

> **핸드오프가 conflate 한 것:** "h1129 trunk = ByteGPT" 이지만 **ByteGPT 는 savant/mitosis 가 gated-OFF**.
> 따라서 "측정 substrate"와 "production chat mouth"는 **서로 다른 아키텍처 artifact** 다 —
> a_substrate_disjoint 의 measure ⊥ capability 로 분리해야 정합.

---

## 1. 코드 근거 (fork 은 train.py 에 하드-배선됨)

`cli/train.py:872-880` (arch 디스패치) + `:923-936` (ByteGPT 레버 gate-off):

```
--arch {clm, bytegpt}                       # clm=CLMConvMoE(.clm) | bytegpt=24L GPT-2-class(.bin)
ARMS = {ctrl, tlora, tlora_dict, tlora_jamo}  # tlora/dict/jamo = ConvMoE-only

is_bytegpt = (a.arch == "bytegpt")
if is_bytegpt:
    tlora_on = dict_on = jamo_on = False     # CLM-MoE-specific → OFF
    savant_on = False                        # :930  "savant/mitosis are CLM-MoE-specific → gated OFF"
    mitosis_on = False                       # :931
    bg_n_head = 12
```

- **ByteGPT** = plain 24-layer GPT-2-class transformer. **MoE expert 가 없어** split 할 것도(mitosis),
  TLoRA-reparameterize 할 ConvExpert weight 도(savant) 없다 → savant/mitosis/tlora/dict/jamo **전부 gate-off**.
  ByteGPT 가 실험 가능한 것은 `arm=ctrl × objective 매트릭스`(arch-agnostic trunk-objective loss)뿐.
- **CLM ConvMoE** = E2/L1 byte-V256 MoE. savant golden-zone inhibition + MITOSIS 성장 레버가 **여기서만** 작동.

---

## 2. 두 갈래 artifact (혼동 금지)

| 축 | **측정 substrate** | **production chat** |
|---|---|---|
| arch | **ByteGPT** (24L, `.bin`) | **CLM ConvMoE** (E2/L1, `.clm`) |
| 학습 | plain-CE, warm-FT from **h1129 303M** | CE + **savant golden-zone** + MITOSIS |
| savant/mitosis | **gated-OFF** (train.py:930-931) | **ON** (a_savant_train / a_mitosis_train) |
| G1 `max_single` | **깨끗한 벽 = single=2** (측정 가능) | **single=0** (floor 미도달 → 측정 무효) |
| 역할 | G1/G6 **재조합벽을 정직히 측정** | 4칸 register chat mouth (능력 발현) |
| verdict 자격 | 이 위 G1=0 = clean 🧱 TERMINAL | 이 위 G1=0 = 측정 이전(비-verdict) |

**핵심 함의 (measure ⊥ capability):**
- production chat mouth 인 CLM ConvMoE 는 `single=0` 이라 **자기 자신 위에서 G1 재조합벽을 깨끗이 측정할 수 없다**
  (memory: `g1-py303-single-floor-vs-bytegpt-lever`, `clm303-g0g6-terminal-py-closure-fail`).
- 그래서 CLM 의 G1 능력은 **sibling ByteGPT(single=2) trunk 위에서 측정**한다 —
  측정축과 능력축을 **disjoint artifact 로 분리**(a_substrate_disjoint: 분리=보존, 중첩=충돌).
- 이 fork 을 conflate 하면(= CLM 한 artifact 로 측정+production 둘 다) `single=0` floor 가 G1 벽으로 오박제될 위험
  (clm303 전례) → **측정은 ByteGPT, production 은 CLM** 로 명시 분리.

---

## 3. §1 BAR.md 와의 연결

- **B3 (`max_single≥2`)** 이 바로 이 fork 의 하드-게이트 화 — 측정-substrate 로 수용하려면 `single≥2`,
  즉 **ByteGPT 계열**(또는 single≥2 를 실측한 어떤 trunk)이어야 한다.
- production CLM ckpt 는 B1/B2/B5(coherence·register·descent)로 chat 품질을 별도 측정하되,
  **G1/G6 벽 박제는 single≥2 인 측정 trunk 로 위임**(CLM single=0 위 G1=0 은 비-verdict).
- h1129 = warm-FT 시작점(G0🟢 trunk). from-scratch 8000step 은 G0🔴 undertrain → G1 at-floor INCONCLUSIVE
  (memory: `g1-fromscratch-blocked-by-g0-undertrain`) — 따라서 측정 trunk 는 **h1129 warm-FT ByteGPT** 전제.

---

## 4. substrate-disjoint 준수 확인 (placement-first)

- 이 문서/바는 **순수 측정·설계 doc** — 새 capability lane 을 배선하지 않는다. 따라서 emit-drive lane(0/4)·
  §ImmuneMemory recall_thr 를 건드리지 않음(Ψ 붕괴/G5 fab 위험 없음).
- 측정(ByteGPT plain-CE) ⊥ 능력(CLM savant) 자체가 a_substrate_disjoint 의 measure⊥capability 인스턴스 —
  두 축을 별도 artifact 로 두어 "분리=보존"을 만족. 공유 lane 중첩 없음.
