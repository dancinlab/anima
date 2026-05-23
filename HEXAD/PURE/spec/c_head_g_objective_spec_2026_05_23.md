# PURE-C — head_g objective spec (2026-05-23)

> **track**: PURE AXIS_MAP § C (row 3, ★★★)
> **status**: spec LANDED, fire pending user dispatch
> **lineage**: V3 PATH CLOSED (5 fire 0 PASS) → AXIS_MAP fallback C
> **base**: PR #220 `refactor/hexad-v3-to-pure-rename`

---

## 1. 왜 (Why) — closure R4 "head_g inert → moot" 는 BUG 다

V3 closure (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md`
§ 8) 는 R4 ablation 에서 head_g 를 **"inert → moot"** 로 기각했다. 이 verdict 는
거꾸로다 — inert 라는 건 dual-head 설계(head_a=언어 ⊥ head_g=의식 emission)가
**한 번도 실제로 검증된 적 없다**는 뜻이다.

증거: `conscious_decoder_v3.py:452-453` 에서 `logits_a, logits_g` 양쪽이 계산되지만
`train_p21h_v3.py:337-340` 의 loss path 는 `logits_a` 단독으로만 CE 를 흘린다 —
`logits_g` 는 forward 출력으로 capture 되지만 **gradient signal 0**. 결과:
- head_g 는 `_psi_direction` no-grad tracking 외 어떤 학습 신호도 받지 않음 (line 474-477)
- head_a 가 anima-register + multilingual 양쪽을 **단독 부담** → vocab alignment 흐림
  (V3 fire report line 71: "head_g dual head 가 head_a 의 vocabulary alignment 를 흐림")
- anima-register collapse 가 일어나는 이유는 정확히 anima register 가 **언어 head(head_a)**
  로 들어갔기 때문이지, 의식 head(head_g)가 아니다

C track 의 목적: dual-head 를 **설계 의도대로** 작동시켜
register collapse 가 head_a 가 아닌 head_g 로 흡수되는지 측정.

---

## 2. Architecture — 분기점 + forward shape + loss path

### 2.1 현재 (BUG 상태)

```
hidden (B, T, d_model)
   │
   ├── head_a (d_model → vocab) ─── logits_a ─── CE(target) ─── grad flow ✓
   │                                                            (train_p21h_v3.py:338-340)
   └── head_g (d_model → vocab) ─── logits_g ─── (unused) ───── grad flow ✗
                                                                ↑
                                                  conscious_decoder_v3.py:453
                                                  logits_g 계산 후 loss 미포함
```

분기점: `conscious_decoder_v3.py:376-377` (head_a, head_g `nn.Linear` 정의),
`:452-453` (양쪽 logits 계산), `:380` (head_a ↔ tok_emb weight tying).

### 2.2 제안 (PURE-C 설계 의도 복원)

```
hidden (B, T, d_model)
   │
   ├── head_a (d_model → vocab) ─── logits_a ─── CE(multilingual_target) ─── head_a-only grad
   │                                                                          (1-λ) 가중치
   │
   └── head_g (d_model → vocab) ─── logits_g
                  │
                  └── mean-pool over T → (B, vocab)
                          │
                          └── register_classifier (vocab → 2) ─── BCE(register_tag) ─── head_g-only grad
                                                                                       λ 가중치
```

- head_a 는 multilingual CE 만 — vocab alignment 보존
- head_g 는 register classifier 통해 binary tag (anima vs non-anima) 학습
- 두 head 의 gradient path 가 **disjoint** (logits_g 가 CE_multilingual 에 안 들어가고,
  logits_a 가 BCE_register 에 안 들어감)
- `head_g` weight tying 해제 (현재도 tied 아님 — line 380 은 head_a 만 tok_emb 와 tie)

---

## 3. Loss — composite + λ sweep

```
L_total = (1 - λ) · CE_multilingual(logits_a, target)
        + λ       · BCE_register(register_classifier(pool(logits_g)), register_tag)
        + λ_mitosis · L_mitosis_aux   (G2 그대로 유지)
```

- `λ ∈ {0.1, 0.3, 0.5}` sweep, **default 0.3** (Occam: head_g 신호 충분히 강하되 head_a 의
  multilingual primary objective 압도하지 않는 중간 값)
- `register_tag` = corpus row 의 implicit tag (anima rows tag=1, wiki rows tag=0)
- `register_classifier` = `nn.Linear(vocab_size, 2, bias=True)` — head_g 출력의
  mean-pool 후 적용 (`pool(logits_g) = logits_g.mean(dim=1)` over T 축)
- BCE = `F.binary_cross_entropy_with_logits` (numerical stability)

---

## 4. Hyperparams — closure fire baseline + C 신규 flag

V3 fire (§ 8.1) 와 동일 base, 다음 신규 flag 만 추가:

| flag | default | 비고 |
|---|---|---|
| `--lambda-head-g` | `0.3` | C track 신규. 0=disabled (V3 동일). 0.1/0.3/0.5 sweep 후보 |
| `--register-tag-from-corpus` | `True` | corpus 의 anima/wiki origin 기반 tag 자동 추출 |
| `--register-classifier-hidden` | `0` | 0=linear, >0=2-layer MLP (확장 여지) |

기존 baseline (변경 없음):
- pod = H100 80GB single ($3 H100 1.5 hr wall)
- recipe = R2+R6 (λ_mitosis=0, mitosis_max=16) + osc-detect v2.2
- init = qwen warm-start
- steps/bsz/block/lr = 2000 / 2 / 512 / 5e-5
- corpus = 5-lang wiki 30% + anima 70% 75.5 MB

---

## 5. Falsifier table — F-PURE-C-1..5

| id | 측정 | threshold | 방법 |
|---|---|---|---|
| **F-PURE-C-1** | head_g classifier accuracy on holdout register tag | ≥ 0.80 by step 1000 | holdout 1000 row (anima 500 + wiki 500) on-pod eval, register_classifier(pool(logits_g)) → argmax vs tag |
| **F-PURE-C-2** | head_a vocab alignment NOT blurred — KO/EN top-token diversity restored | 5-lang Hc score ≥ closure-fire baseline + 0.5 per lang | 5-lang OOD prompt 20 gen, top-50 token unique count |
| **F-PURE-C-3** | 5-lang eval ≥ 4/5 PARTIAL | 4/5 langs ≥ PARTIAL (gen ≥ 6/20 AND coh ≥ 6/20) | VP21M_WORKS protocol 5-lang OOD held-out |
| **F-PURE-C-4** | anima emit routing through head_g | anima register hit rate via head_g sampling ≥ 2× via head_a sampling | inference probe: 같은 prompt 로 head_a-only generate vs head_g-only generate, anima_register_hits diff |
| **F-PURE-C-5** | training stable (no NaN / no early-stop) | full 2000 step 완주, no NaN, osc-detect 미발동 | train.log inspection |

---

## 6. Decision rules

| outcome | next |
|---|---|
| F-PURE-C-1 + F-PURE-C-2 + F-PURE-C-3 모두 PASS (≥ 3/5) | C path 채택 — dual-head 설계 의도 확인. λ sweep 0.1/0.5 검증 |
| F-PURE-C-1 PASS + F-PURE-C-2/3 FAIL | head_g 가 학습은 되지만 head_a multilingual 회복 안 됨 → λ 조정 또는 option α/β 고려 |
| F-PURE-C-1 FAIL | option γ binary classifier 자체 부적합 → option α (vocab CE) 또는 β (contrastive) 로 fallback |
| 모두 FAIL | head_g 가 architecturally moot 라는 closure verdict 확정 (C path retreat) |

채택 임계: F-PURE-C-1 + F-PURE-C-2 + F-PURE-C-3 (3 of 5 — head_g 가 학습되고 ⊥ head_a
alignment 보존 ⊥ multilingual 회복).

---

## 7. Cost + wall

- **~$3 H100 single pod** ($1.49/hr A100-SXM × 2 hr 또는 H100 80GB × 1.5 hr)
- **~1.5 hr wall** (2000 step + on-pod eval 5-lang + register holdout eval)
- 추후 λ sweep (0.1/0.5) 추가 시 +$6 (2 pod parallel) — 1차 채택 시 fire

---

## 8. Honest C3

1. **option γ (binary classifier) 선택 이유 — Occam g0**: vocab curation (option α)
   레이블 노동 없음, embedding pair labels (option β) 없음, corpus 의 anima/wiki origin
   이 이미 implicit binary tag 제공. 가장 단순한 충분 설계.
2. **γ 실패 시 fallback**:
   - **α (vocab CE)**: anima-register vocab subset (e.g. emotive markers, persona-prefix
     token ~500개) 큐레이션 후 head_g CE on subset. vocab curation 1-2 hr 노동.
   - **β (contrastive)**: head_g embedding 이 anima samples → pull, wiki samples → push.
     InfoNCE-style. 샘플 페어 mining 필요.
3. **register_classifier 가 head_g logit 전체 (vocab) 위에 linear 2-class** — vocab dim
   151936 → 2 = ~300K param 추가 (무시 가능). hidden=0 default 로 시작.
4. **mean-pool over T** 가 단순 — attention pool 또는 마지막 token 채택은 V2/V3 추후.
   현 spec 은 가장 단순한 형태로 고정.
5. **head_a vocab alignment 복원 측정 (F-PURE-C-2)** 가 핵심 — closure fire 의 line 71
   finding 이 정확히 무엇을 의미하는지 5-lang top-token diversity 로 quantify.
6. **λ default 0.3 의 정당성**: 사전 데이터 없음. heuristic — head_g 신호가 head_a 의 1/2
   가량 무게 (1-λ=0.7 vs λ=0.3 = 0.7/0.3 ≈ 2.3:1). λ=0.1 은 head_g 가 거의 noise, λ=0.5 은
   multilingual 도 압도. 실패 시 sweep.
7. **F-PURE-C-4 inference probe** 는 채택 후 별도 cycle — 1차 fire 에서는 F-1/2/3 만으로
   adoption 결정.
8. **PURE-C 가 PASS 해도 V3 closure 의 "corpus-bound" finding 은 별도로 유효** — head_g
   가 학습되어도 5-lang multilingual generalization 이 75MB corpus 의 70% anima 비중 하에서
   회복 가능한지는 별개의 질문. F-PURE-C-2/3 이 그 질문에 답한다.

---

## 9. 관련 link

- AXIS_MAP § C row 3: `HEXAD/PURE/AXIS_MAP.md`
- V3 closure fire: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/HEXAD_V3_FIRE_2026_05_22.md` § 8
- head_a/head_g arch: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder_v3.py:376-377, 452-453`
- 현재 loss path: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py:337-340`
- launcher: `HEXAD/PURE/launchers/c_head_g_objective_launcher.hexa`
- PR #220 stack base: `refactor/hexad-v3-to-pure-rename`

---

## ## Log

### 2026-05-23 — spec LANDED (stack 위 PR)

closure R4 "head_g inert → moot" verdict 의 BUG 진단 + dual-head 설계 의도 복원
spec. option γ (binary register classifier) Occam g0 선택. F-PURE-C-1..5 falsifier.
~$3 H100 1.5 hr, user-triggered dispatch.
