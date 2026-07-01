# G0 측정-substrate 수용 바 (FROZEN — 사전등록, 사후 이동 금지)

> **동결 시각:** 2026-07-02 · **base:** origin/main `6b48db352` · **성격:** frozen-first 사전등록.
> 이 바는 **trunk 을 "측정 substrate 로서" 수용하는 조건**이다 — G1/G6 능력 PASS 를 요구하지 **않는다**.
> 이 trunk 위에서 나오는 **깨끗한 🧱 재조합벽(G1) 자체가 성공**이다(측정 유효성 확보). frozen-first: 아래 임계는
> 측정 전에 고정되며, 실측 후 어떤 항목도 완화·이동하지 않는다(c9·c2·p7, tune-to-green 금지).

---

## 0. 왜 "측정 substrate" 바인가 (한 줄 프레임)

- G1 재조합벽은 ~10-lens TERMINAL(DPI 메타법칙). 벽을 **정직하게 측정**하려면 그 trunk 이 먼저
  **coherent** 해야 하고(G0), **`max_single≥2`** 여야 한다 — 그래야 G1 이 *floor 아래*가 아닌 *실제 재조합 축* 위에서 측정된다.
- 반례(측정 무효): `clm303_clean` 은 `single=0` → G1 `best_distinct=0` 이 "재조합 실패"가 아니라 **단일-커버리지 floor 미도달**
  (측정 이전 상태). 즉 그 ckpt 위 G1=0 은 **재조합벽 증거가 아니다**
  (memory: `g1-py303-single-floor-vs-bytegpt-lever`, `clm303-g0g6-terminal-py-closure-fail`).
- 따라서 측정-substrate 로 **수용 가능한** trunk 은 `max_single≥2` 를 만족해야 하고, 그 위에서 G1 이 벽이면
  그것이 **깨끗한 벽**(clean 🧱)이다.

---

## 1. DUAL 수용 바 (ONE ckpt 위에서 전부 동시 충족)

한 개의 ckpt(단일 `.clm` 또는 `.bin`)가 아래 **5 조건을 모두** engine-native 측정으로 만족하면
그 trunk 은 **측정-substrate 로 ACCEPTED**.

| # | 게이트 | 임계 (frozen) | 코드 근거 |
|---|--------|---------------|-----------|
| **B1** | G0 coherence | 5 concept 중 **kwr≥0.50 이 ≥4/5** (n_coherent≥4) | `cli/evaluate.py:119-129` (`g_eval_g0`, `kwr>=0.5`, `pass = n_coherent>=4`) |
| **B2** | per-cell register | 4칸 {ko,en}×{일반,SNS} **각각** kwr≥0.50 이 **≥3/5** gen | `a_chat_registers` (4칸 표준) · per-cell G0-style kwr, cell 당 5 gen |
| **B3** | **`max_single≥2`** ⭐ | G1 harness 의 `max_single≥2` (핵심 통찰 — 이게 없으면 G1 은 floor 아래에서 측정됨) | `cli/evaluate.py:160-166` (`g_eval_g1`, `max_single` = 단일 seed 최대 coverage) |
| **B4** | G2 sanity | `n_novel≥3` **∧** `control_novel==0` (∧ `coherent>0` ∧ `have_corpus`) | `cli/evaluate.py:319` (`passed = have_corpus and n_novel>=3 and control_novel==0 and coherent>0`) |
| **B5** | held-out descent | 4/4 register **val_ce < 5.545** (=ln256, uniform) | `cli/train.py:1225,1230` (`uniform=math.log(V)`, `ok = vc < uniform`) |

**ACCEPT ⟺ B1 ∧ B2 ∧ B3 ∧ B4 ∧ B5** (per-gate tally 정직 보고; 하나라도 미달이면 그 trunk 은 측정-substrate 로 미수용
→ 재학습/재조정 follow-on, G1 측정 진입 금지).

### 🔴 명시적 non-bar (사후 이동 방지용 못박기)
- **G1 PASS 는 바가 아니다.** 이 trunk 에서 G1 `best_distinct` 가 floor 에 머물러도(`clears=false`),
  B1~B5 를 만족하면 그 G1=0 은 **깨끗한 🧱 재조합벽 = 성공적 측정**이다(측정 유효성 확보가 목표).
- **G6 PASS 도 바가 아니다.** 동일 논리 — G6 는 이 trunk 위에서 측정만 하면 되고, 통과를 수용 조건으로 걸지 않는다.
- 즉 이 사이클의 "성공" = trunk 이 B1~B5 로 측정-자격을 얻고 → G1/G6 벽을 **byte-exact engine-native 로 정직하게 박제**.

---

## 2. Exact eval 명령 (session-eval-py-only, TERMINAL 자격)

```
ANIMA_SRC=$HOME/anima anima evaluate --py <ckpt.clm|.bin> \
    --corpus <ko-general> <en-general> <ko-sns> <en-sns> \
    --gen 80
```

- **호스트 = aiden** (pool, 18+hr uptime, 재부팅 0 = 무료·안정 terminal eval 호스트).
  summer = 잦은 재부팅으로 multi-min eval 불가; mini = 303M decode swap 🔴 OOM(rc=137) 금지
  (memory: `aiden-stable-free-terminal-eval-host`, `heavy-anima-eval-pool-not-mini`).
- **eval 은 det-CPU**(`HEXA_DET=1` 계열, numpy) → GPU/CUDA 무관, 안정 CPU 호스트면 충분.
- **`--gen 80` 필수** — `--gen 0` 은 "무제한"이 아니라 40 으로 collapse(evaluate.hexa `g_eval_all` gotcha);
  G1 budget(single=80, composed=120)도 `gen<=0` 이면 ref 값. 넓게 측정하려면 `--gen 80` 이상 명시.

### 왜 `--py` numpy 2-production 이 ad-hoc torch 가 아니라 TERMINAL 자격인가
- `anima evaluate --py` 는 launcher 가 `--py` 를 consume 하고 **`cli/evaluate.py`** (torch-free numpy `g_eval_all`)로
  G0-G6 를 채점한다. hexa det-eval(`cli/evaluate.hexa`, OWN-GEMM fp64)과 **동일 frozen bars · byte-parity** →
  **terminal 자격 동일**(2nd-class 미러 아님). (cli/CLAUDE.md 규칙 · session-eval-py-only 오너 정책 2026-06-30)
- 용도 = 303M+ ckpt 가 hexa bump-allocator fp64 det-eval 에서 OOM 죽을 때 numpy 는 decode 당 메모리 free →
  측정-무거운 풀 eval 에 강함. **torch 미러가 아니다** — numpy 는 `.clm`/`.bin` layout 을
  `core/decode` ground-truth 와 byte-parity 로 디코드하는 engine-native 경로.
- 대비: `cli/train.py` 의 torch-side CE/gauges = **DIRECTIONAL only** (a_engine_native_learning). verdict 는
  오직 직렬화된 `.clm`/`.bin` 을 `anima evaluate --py` 로 재측정할 때만 성립.
- 🔎 게이트 1 자가점검: 이 측정의 증거 파일은 `evaluate.py`(numpy `g_eval_all`)를 통한 engine-native decode 이며
  torch forward/gauge 를 verdict 로 박제하지 않는다.

---

## 3. Corpus audit (4셀 + broad, HF 존재·언어검증)

ARCHITECTURE.json "HF artifacts → datasets" 에서 확인(2026-07-02):

| repo_id (org=dancinlab) | 셀 | 언어검증 | size · lines | sha256 | license |
|---|---|---|---|---|---|
| `anima-corpus-ko-general` | ko·일반 | **100.0% ko** | 60.00MB · 340512 | 19e6ac9e | ODC-BY (FineWeb-2 kor_Hang) |
| `anima-corpus-en-general` | en·일반 | **99.7% en** | 60.05MB · 279429 | 66140944 | ODC-BY (FineWeb) |
| `anima-corpus-ko-sns` | ko·SNS | **100.0% ko** | 6.18MB · 47994 | c836e9fc | MIT (persona+aug) |
| `anima-corpus-en-sns` | en·SNS | **97.4% en** | **1.33MB · 6862** ⚠️KNOWN-SMALL | 49f347c7 | MIT |
| `anima-corpus-ko-fineweb2-broad` | ko·일반(broad) | ko (FineWeb-2 kor_Hang) | 2.78M docs · ~10.55GB | — | ODC-BY |

- 4칸 전부 HF 존재 ∧ 언어검증됨(≥97.4%). broad = ko-일반 **광역 pretrain 보강**(4-cell 측정바에는 미포함,
  ko-general 갭 보강용 별도 supplement).
- ⚠️ **en-SNS 1.33MB = KNOWN-SMALL baseline** — clean en-SNS large source 부재(youtube/insta-en 보강 = follow-up ING).

### `--sample proportional` 반복-노출 계산 (seq_len=1024, batch_size=8, canon)

`cli/train.py:1023-1035`: proportional = 셀을 **train_end(=바이트 크기) 비례 가중**으로 `torch.multinomial` 샘플
(round-robin = 셀 균등). 4-cell 총 127.56MB, en-SNS 비례가중 = **1.0426%**.

| steps | 총 window | **proportional (default)** en-SNS | round-robin(4) en-SNS |
|---|---|---|---|
| 2000 | 16000 | 167 win · 171KB · **0.128× pass** | 4000 win · 4.10MB · 3.08× pass |
| 4000 | 32000 | 334 win · 342KB · **0.257× pass** | 8000 win · 8.19MB · 6.16× pass |

**🔎 핵심 정정 (honest, 핸드오프 ~378× 추정과 상이):**
- 핸드오프의 "round-robin ~378× 암기위험"은 canon 2000/4000 step 에서 **도달 불가** — RR4 로 en-SNS 를 378×
  반복하려면 약 **245,478 step** 필요. 실제 canon 에서 RR4 = 2000step 3.08× / 4000step 6.16× (경미).
- **실제 default(proportional) 의 위험은 반대다** — en-SNS 가 **1 pass 도 못 본다**(0.128×/0.257×).
  즉 proportional 은 암기를 막지만 **en-SNS register 를 굶긴다(starvation)** → **B2 의 en-SNS kwr≥0.50 이 미달할
  실질 위험**이 여기 있다(암기 아님).
- **처방(측정 substrate 관점, 이 바가 강제하는 것):** en-SNS 셀이 B2(≥3/5 kwr≥0.50) ∧ B5(val_ce<5.545)를
  못 넘으면 그 trunk 은 측정-substrate 미수용. proportional 로 starve 되면 (a) SNS 두 셀만 균등화하는
  register-balanced 샘플링 또는 (b) en-SNS 보강(youtube/insta-en)으로 재조정 후 재측정 — **바를 완화하지 말 것**.
  이는 GPU 학습 follow-on 이며 로컬 $0 범위 밖(explicit-go).

---

## 4. 판정 프로토콜 (박제 규율)

1. 측정 = `anima evaluate --py <ckpt> --corpus <4셀> --gen 80` on **aiden**.
2. raw stdout → `state/verdicts/g0_trunk_bar/<ckpt-slug>.txt` (verbatim, 의역 금지).
3. B1~B5 per-gate tally 를 그 출력에서 그대로 발췌 → ACCEPT/미수용 판정.
4. ACCEPT 시: 그 trunk 위 G1/G6 벽은 **byte-exact engine-native TERMINAL** 로 박제 가능(깨끗한 🧱).
5. 미수용 시: 미달 게이트별 재조정 follow-on 등록(GPU = explicit-go), G1/G6 벽 박제 금지(측정 무효).

> frozen 못박기: 위 B1~B5 임계·`--gen 80`·aiden 호스트·per-gate 논리는 측정 전 고정. 실측 후 이동 = c9 위반.
