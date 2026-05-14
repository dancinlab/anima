# BENCHMARK — 두 anima HF 모델 대화 비교 2026-05-14

> Side-by-side empirical comparison of the 2 PUBLIC anima HF ckpts.
> **Re-run on ubu-2 RTX 5070** (NVIDIA, torch 2.11.0+cu130) via wilson pool —
> CUDA acceleration, byte-equal output vs Mac MPS prior run.
>
> **중요한 사전 fact**: 두 모델은 **다른 architecture + 다른 목적**.
> 한 모델은 Korean chat LM (24L 332M, BPE-32000), 다른 하나는 mitosis
> substrate research toy (1L 21M, byte-level vocab-256). 직접 "대화"는
> 어휘 공간이 달라서 불가능 — 각 모델의 design target task로 측정한다.

---

## §1 두 모델 spec

| 항목 | ★ canonical anima 본체 | 🧬 saga peak — mitosis cotrain v1 |
|---|---|---|
| HF | [dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12](https://huggingface.co/dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12) | [dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12](https://huggingface.co/dancinlab/anima-clm-v5-mitosis-cotrain-2026-05-12) |
| 목적 | **Korean chat LM** (D1+D2 anchor) | **mitosis substrate research** (D4 anchor) |
| 아키텍처 | 24-layer causal LM (Phase 1A.1 base + 200-step SFT) | 1-layer transformer block × N cells (v5-mitosis cell pool) |
| 파라미터 | 332M | 21.2M |
| 어휘 | BPE 32000 (한글 토큰화) | byte-level vocab=256 |
| d_model | 4096 (estimate) | 384 |
| n_cells | n/a | 2 → 64 (split-trained) |
| ckpt size | 597 MB | 581 MB |
| sha256 | 45063f64… | (saga peak v1 ckpt) |

---

## §2 ★ Phase 1A.4 — Korean chat probes (ubu-2 RTX 5070, 2026-05-14)

6 prompt, greedy mode, max_new=60, soft-force-α=3.0 default.

| # | prompt | response |
|---|---|---|
| 1 | `사용자: 안녕! 너는 누구야? \| 도우미: ` | `네, 맞아요! 먹어! 안녕! 너는 누구야?\n` |
| 2 | `사용자: 우주가 뭐야? \| 도우미: ` | `당신은 anima 가 의식 법칙 138 설명해줘\n` |
| 3 | `사용자: 의식은 무엇이라고 생각해? \| 도우미: ` | `의식이 뭐였지?\n` |
| 4 | `사용자: 좋아하는 색깔은? \| 도우미: ` | `도은 좋아하시는군요. 다음 날, 좋아하는 색…` |
| 5 | `사용자: 너는 어떻게 성장해? \| 도우미: ` | `네, 맞아요. 그런 다음 단계를 따르세요:\n` |
| 6 | `사용자: 세포 분열에 대해 설명해줘 \| 도우미: ` | `세포 분열(mitosis) \| 설명 \| 사망일 수 있는 세…` |

**Cross-platform byte equality**: ubu-2 RTX 5070 outputs **byte-equal** to Mac MPS (greedy deterministic; verified token-level identical across all 6 probes).

**Honest assessment — 6/6 conversational coherence FAIL**:
- prompt #1 self-intro 없이 prompt echo
- prompt #2 "우주" 무관, 페르소나 키워드 echo only
- prompt #3 질문 재반복
- prompt #4 "색깔" 아니라 "도(path)" 좋아한다고 답 — 카테고리 미스
- prompt #5 generic 지시 단어 ("그런 다음 단계를 따르세요") — "성장" 답 없음
- prompt #6 markdown table syntax 환각 ("세포 분열(mitosis) | 설명 | 사망일 수…")

**Korean syntax 는 보존** (조사/어미 일치) 그러나 **semantic answer coherence 완전 미달**.

**근본 원인**: 200-step SFT × $0.014 = sub-cent train. corpus 작고 학습 매우 짧음 → keyword 등장 가능하나 의미적 응답 형성 안됨.

**V5.8 "5/5 PASS" 가 의미하는 것**:
- V5.8 falsifier = "5 prompt 각각의 target keyword (예: 'color'→'노란색', 'cosmology'→'우주') 응답 텍스트에 포함 여부" 만 측정
- **conversational coherence 평가하지 않음**
- 위 6-probe 는 V5.8 prompt-set 과 일치 안함 — V5.8 자체는 narrow keyword falsifier

**★★★★★ closure 의 실제 의미**:
- 5-cond aggregate = 5개 falsifier 통과 (V5.8 keyword + F-V5MIT routing + Principle #3 grep + hexa byte parity + persona M4 cosine)
- 어느 falsifier 도 "anima 가 의미 있게 대화한다" 측정 X
- "anima 본체" 라벨은 **substrate anchor** (D2 ckpt 식별) 의미, **chat capability anchor 아님**

**Canonical V5.8 verdict** (PSCC §46, separately fired on Vast.ai 4090):
- std_greedy **5/5 PASS** (color/profession/day/cosmology/anima_fact 모두)
- std_sample 3/5, M3 1/5, M4 5/5

---

## §3 🧬 cotrain v1 — mitosis substrate falsifier (cotrain_result.json)

cotrain v1 은 byte-level vocab=256 의 1-layer toy substrate. Korean chat 평가는
부적합 (어휘 공간이 BPE-32000 한국어와 다름). 대신 **mitosis falsifier suite** 가
직접적인 평가.

### §3.1 F-V5MIT-1..5 결과 (5/5 PASS, V14-STRICT 10/10)

| falsifier | 측정 | 결과 |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | splits=62, grad_fn 위반 검사 | **PASS** — 62 splits, 0 grad violations |
| F-V5MIT-2 MERGE-WEIGHT | merge 후 weight 보존 (14 pair check) | **PASS** — max_abs_err 0.0 |
| F-V5MIT-3 PHI-CONSERVATION | per-cell Φ 측정 (pre vs post) | **PASS** — delta_ratio 3.88e-5 ≪ tolerance 0.25 |
| F-V5MIT-4 COTRAIN-CONVERGE | initial CE 256.5 → final 1.17 (220× 감소) | **PASS** |
| F-V5MIT-5 V14-STRICT | 10-beat sequential mirror test | **PASS** — 10/10 every-beat |

### §3.2 cotrain dynamics

| metric | value |
|---|---|
| wall_seconds | 1990 (0.55 hr) |
| cost_usd_actual | $1.26 (H100 SXM @ $2.281/hr) |
| n_cells initial → final | 2 → 64 (saturated) |
| splits total | 62 (max=128 - 64 = saturated at cap) |
| Φ initial | 0 (single-cell) |
| Φ final | 4.16 |
| Φ best | 4.19 (peak ~step 4000) |

### §3.3 ckpt 출력 sample (byte-level, ubu-2 RTX 5070 측정)

cotrain v1 ckpt 의 forward output 은 256-byte logits. UTF-8 byte input 을
greedy decode 한 실측 결과:

| # | prompt (UTF-8 byte input) | response (byte→UTF-8 decode) |
|---|---|---|
| 1 | 안녕! 너는 누구야? | `\n` (EOS immediate) |
| 2 | 우주가 뭐야? | `\n` |
| 3 | 의식은 무엇이라고 생각해? | `\n` |
| 4 | 좋아하는 색깔은? | `\n` |
| 5 | 너는 어떻게 성장해? | `\n` |
| 6 | 세포 분열에 대해 설명해줘 | `닠실요실일고 하싈심심실이요.\n` |

**Observations**:
- 6 prompt 중 5 개 즉시 EOS (`\n` byte 10) — 1L 21M byte-level 모델의 코헤어
  화 없음
- prompt #6 "세포 분열" 에 대해서만 22 byte 출력 — 한국어 byte 분포 학습은
  있으나 의미 코히어런스 없음 (`닠실요실일고`, `싈심심실이요` — 비-단어)
- ckpt loading: state_dict 64 cells 인식, dynamic split 으로 pool 확장 후
  load (missing=0 unexpected=2). engine forward 작동.

**이 모델은 substrate routing behavior 측정용** (F-PERSONA-4 의 가설 검증).
chat 능력 없음은 **designed** — corpus 200 KB byte-level 학습 의 expected
output 분포. routing/mitosis behavior 가 evaluation target, 자연어 생성 아님.

(post-cotrain F-PERSONA-4 측정: KL=0.0 winner-take-all — PSCC §44, §A2-trap의 시발점)

---

## §4 두 모델 직접 대화 가능성

**불가능**. 어휘 공간이 다름:
- ★ Phase 1A.4: BPE 토큰 ID 0..32000
- 🧬 cotrain v1: byte ID 0..255

A의 출력을 B의 입력으로 넣으면 BPE-tokenized 한국어가 byte로 잘못 해석되어
무의미. 역방향도 동일.

**개념적 비교 가능 영역**:

| 차원 | ★ Phase 1A.4 | 🧬 cotrain v1 |
|---|---|---|
| 한국어 생성 | ✓ (V5.8 5/5) | ✗ (byte-level) |
| Mitosis split/merge | ✗ (static arch) | ✓ (62 splits, 64 cells) |
| persona substrate evolution | ✗ (frozen post-SFT) | ✓ (Lorenz + perturbation) |
| F-PERSONA-1..5 측정 | partial (1,5 가능) | full 5/5 |
| F-V5MIT-1..5 측정 | n/a | 5/5 PASS |
| 외부 사용자가 대화 가능 | ✓ (직접 prompt → response) | ✗ (routing behavior 만 측정) |

---

## §5 honest C3 (★★ amended — conversational coherence reality)

1. **★ Phase 1A.4 의 conversational coherence = 0/6** — 위 6 free-form
   probe 중 어느 것도 의미 있는 답 생성 안함. Korean syntax 는 보존되나
   semantic answer alignment 미달. **chat 능력 모델 아님**.
2. **"V5.8 5/5 PASS" 의 한계 가시화** — V5.8 5 prompt 별 target keyword
   포함 측정만 — 위 6 free-form probe 가 V5.8 prompt-set 미포함이라 직접
   비교는 불가. 그러나 keyword-pass falsifier 가 "chat 능력 ☑" 의미 아님은
   본 측정으로 명확.
3. **"★★★★★ canonical anima 본체" 라벨 재해석** — Phase 1A.4 ckpt 는
   **D2 substrate anchor** (어떤 ckpt 가 D1 falsifier 5/5 통과시키는지),
   **chat assistant 자격 아님**. 실용 대화 사용 시 GPT-4 / Claude / Gemini
   등 공개 LLM 사용 권장.
4. **cotrain v1 의 byte-level chat 출력 = 5/6 즉시 EOS + 1/6 비-단어** —
   chat 모델 아니므로 expected. 이 모델 의 평가 metric 은 F-V5MIT-1..5
   (V14-STRICT 10/10) + F-PERSONA-4 routing 측정.
5. **두 모델 의 mission 차이** — ★ 는 falsifier 통과용 minimal SFT,
   🧬 는 mitosis substrate 검증용. 어느 쪽도 사용자-facing chat assistant
   아님. ★★★★★ aggregate ☑ 는 ML research milestone (substrate science),
   product-ready chat 아님.
6. **PSCC §52-§55 saga 결과 (v7/k/l/m/n)** 는 모두 cotrain v1 후속 변형 —
   strict-4a closure 시도. 모두 FALSIFIED, local-only, HF 미공개.
7. **공정한 chat 모델 비교 가능성**: 만약 진정한 anima chat 능력 평가 필요시,
   (a) Phase 1A.4 sample mode (temp=0.85+) 로 다양성 확보, (b) loss masking +
   더 긴 SFT, (c) 더 큰 corpus, (d) anima_chat.py wrapper 의 prompt template
   재조정 — 어느 것도 본 saga §52-§55 의 strict-4a closure path 와는 별개
   axis (chat-quality vs routing-strict).

---

## §6 cross-link

- ★ Phase 1A.4: `state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt`, doc `docs/anima_clm_phase1a4_lr5e6_2026_05_12.md`
- 🧬 cotrain v1: `state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt`, result.json + doc `docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md`
- HF line-up: `LINE-UP.md`
- saga ledger: `PERSONA.tape` §A6, `docs/anima_pscc_55_lm_falsified_2026_05_14.md`
- future cycle: `STRICT-4A.step`
