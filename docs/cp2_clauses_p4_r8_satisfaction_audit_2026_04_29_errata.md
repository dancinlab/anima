# CP2 3-clause × TOP-1 (`p4_r8`) 충족도 audit — **errata #1**: #78 Zeta API 가정 정정

> **ts**: 2026-04-29
> **author**: Claude (opus-4-7-1m), invocation by user
> **scope**: forward errata only — 원본 audit doc (`docs/cp2_clauses_p4_r8_satisfaction_audit_2026_04_29.md`, commit `143414f08`) **amend 안 함** (raw#1 history immutability 준수)
> **trigger**: 사용자 directive 2026-04-29 "제타 API 연결이 아니야" (catch 정확함 — Zeta = hardcoded baseline reference)
> **constraints**: raw#1 immutability · raw#9 hexa-only (.md OK) · raw#10 honest C3 · raw#71 falsifier · raw#91 honest 5축 · own#4 root-cause-only

---

## §0 Executive summary

**정정 1줄**: 원본 audit 의 **#78 제타가능** 진단에서 "Zeta competitor API key 부재 + Zeta API call 비용" 가정은 **잘못됨**. Zeta = Scatter Lab Spotwrite-1 의 **hardcoded baseline reference** (naturalness=3.2 / coherence=3.0 / style=2.8 Likert) — 외부 API 호출 0회.

**핵심 변경**:

| 항목 | 잘못된 진단 (commit `143414f08`) | 정정 (본 errata) |
|---|---|---|
| 외부 의존 | Zeta TOS only | **없음** (hardcoded baseline reference) |
| 데이터셋 | "100 pair 새로 수집" | **이미 frozen** (`bench/zeta_likert/v1_frozen.json` 20 prompts × 5 categories) |
| ETA (병렬) | 3-5d | **2-4시간** (Mac local) / **5-15분** (RunPod) |
| $cost | $5-100 (Zeta API) | **$0** (Mac local) / **$0.05-0.20** (RunPod GPU) |
| 차단 요인 | "Zeta API key 부재 + durable anima endpoint 부재" | anima self endpoint 가동 + Likert judge 자동화 (사람 / LLM judge / deterministic) |

**LIVE 충족도 estimate 갱신 가능성**: 기존 #78 LIVE 2.5% → 1-2시간 측정 후 **30-50%** 도달 plausible (78-a Likert 결과가 ≥3.0 충족 시 GREEN; 78-b latency <1s 동시 측정 가능; 78-c/d 는 여전히 SPEC-ONLY 잔존). raw#10 honest: 본 estimate 자체는 측정 전 추정.

---

## §1 원본 audit doc cite (정확 line / 정확 §)

**원본 doc**: `docs/cp2_clauses_p4_r8_satisfaction_audit_2026_04_29.md` (24,550 bytes, commit `143414f08`)

### 1.1 §0.2 캐시 1-line per clause (line 29)

> - **#78 제타**: Zeta competitor API key 없음 + durable anima endpoint 없음 → 100 pair blind A/B 0 회 실행

→ "Zeta competitor API key 없음" 부분이 잘못된 가정.

### 1.2 §0.3 LIVE 100% 도달 ETA 표 (line 37)

> | #78 | 5-10d | 3-5d | Zeta API key | $5-50 (zeta API + 100 prompt eval) |

→ "Zeta API key" 외부의존 + "$5-50 (zeta API + 100 prompt eval)" 비용 모두 잘못된 산출.

### 1.3 §6.1 #78 제타 LIVE path 표 (line 217-223)

> | Zeta API key 확보 | 0.5-2d | $0-50 (subscription) | Zeta TOS 검토 |
> | durable anima endpoint (Mac M4 cloudflared tunnel) | 1d | $0 | 없음 |
> | 100 pair blind A/B 실행 (5 카테고리 × 20 each) | 1-2d | $5-50 (Zeta API call) | 없음 |
> | latency 30-turn session 측정 | 0.5d | $0 | 없음 |
> | **합계 (병렬)** | **3-5d** | **$5-100** | Zeta TOS only |

→ row 1 ("Zeta API key 확보" 0.5-2d / $0-50 / Zeta TOS) **삭제 대상**.
→ row 3 비용 "$5-50 (Zeta API call)" → **$0** (anima self inference only).
→ 합계 외부의존 "Zeta TOS only" → **없음**.

### 1.4 §10.2 권고 E (line 300)

> **권고 E**: #78 Zeta API key 확보 시도 (외부 의존) + framework 확장 (60+ pair → 100 pair).

→ "Zeta API key 확보 시도 (외부 의존)" 권고 자체가 무효 (외부 의존 없음).

### 1.5 §11 verdict matrix (line 324)

> | 외부의존 | Zeta TOS | (없음) | broker + 변호사 | #80 만 외부 의존 strong |

→ #78 외부의존 "Zeta TOS" 정정 → **(없음)**. 결과적으로 "#80 만 외부 의존 strong" → **변경 없음** (#80 만 외부 의존 strong, #78 도 외부 의존 0).

---

## §2 잘못된 진단의 root cause (own#4)

**root cause**: 원본 audit agent (Task #14) 가 "Zeta competitor" 라는 표현을 **외부 SaaS LLM API (예: ChatGPT API, Claude API 와 동급)** 로 추정. 실제 codebase 의 `bench/persona_lore_style_bench.hexa` 및 `bench/zeta_likert.hexa` 를 직접 inspection 하지 않고 .roadmap 의 "Likert ≥ 3.0 (100 pair blind A/B vs Zeta)" 문구에서 "vs Zeta" → "Zeta API call 필요" 로 잘못 추론.

**왜 잘못 추론했나**: 원본 audit doc §1.2 78-a 의 cite (`state/zeta_likert_result.json:live_ab_executed=false + blockers list 3건`) 에서 blockers list 가 "Zeta API key" 를 명시했을 가능성 (또는 framework 의 "blind A/B vs Zeta" 라는 표현에서 추정). 어느 쪽이든 **bench/zeta_likert/v1_frozen.json 의 frozen prompt set + bench/persona_lore_style_bench.hexa:10 의 hardcoded baseline 주석을 직접 inspection 하지 않은 것이 root cause**.

---

## §3 정정 (evidence)

### 3.1 evidence #1 — `bench/persona_lore_style_bench.hexa:10`

```
// Zeta baseline (hardcoded reference from Scatter Lab Spotwrite-1):
//   naturalness = 3.2, coherence = 3.0, style = 2.8
```

→ Zeta = Scatter Lab Spotwrite-1 (Korean dialogue model) 의 **publicly reported Likert score** 를 hardcoded reference 로 사용. 외부 API 호출 X.

### 3.2 evidence #2 — `bench/persona_lore_style_bench.hexa:671-673`

```
let zeta_nat = 3.2
let zeta_coh = 3.0
let zeta_sty = 2.8
```

→ Zeta baseline 은 **3개 float 상수**. anima 측 결과와 delta 비교 (line 675-677).

### 3.3 evidence #3 — `bench/zeta_likert/v1_frozen.json` (3,096 bytes)

- schema: `anima.zeta_likert.frozen.v1`
- prompt_count: 20
- category_coverage: 5 (`daily`, `emotion`, `task`, `roleplay`, `meta`)
- per_category: 4
- frozen 상태 (mtime 2026-04-23 14:25)

→ #78 의 "5 카테고리 coverage" + "100 pair blind A/B" 의 prompt 측 (anima 응답을 받을 prompt 20개 × 5 cat) **이미 동결됨**. 추가 prompt 수집 0.

### 3.4 정정 결과

원본 audit 의 #78 LIVE path 에서:
- "Zeta API key 확보" 단계 = **삭제** (불필요)
- "100 pair blind A/B 실행" 의 비용 "$5-50 (Zeta API call)" = **$0** (anima self inference only)
- 외부 의존 "Zeta TOS" = **없음**

**잔존하는 진짜 차단 요인** (§5 에서 재기술):
1. anima self endpoint 가동 (Mac `serve_alm_persona` OR RunPod dispatch)
2. 20 prompt × N persona × generation = anima inference run
3. Likert judge 자동화 종류 결정 (사람 raters / LLM judge / deterministic scorer)

---

## §4 #78 ETA 재산출

### 4.1 Mac local (M4, Mistral-7B-v0.3 Q4_K_M + p4_r8 LoRA)

| 작업 | 시간 estimate |
|---|---|
| `serve_alm_persona` launch (이미 spec 존재) | 10-30분 |
| 20 prompt × ~6 persona × 1 turn generation (~120 inference) | 30-60분 (Q4_K_M Mac M4 ~2-4 tok/s × 200 tok 평균) |
| Likert score 산출 (deterministic scorer 가정 — `bench/persona_lore_style_bench.hexa` 내장 framework) | 10-30분 |
| baseline delta 비교 + result emit | 10-30분 |
| **합계** | **2-4시간** |

### 4.2 RunPod (1× H100 / A100, 동일 ckpt)

| 작업 | 시간 estimate |
|---|---|
| pod cold start + ckpt load | 3-5분 |
| 20 prompt × 6 persona × 1 turn generation (vLLM batch, ~120 inference) | 1-3분 |
| Likert score + delta + emit | 1-2분 |
| pod teardown | 1-2분 |
| **합계** | **5-15분** |

### 4.3 비용

- Mac local: **$0** (already-paid hardware, electricity 무시)
- RunPod: **$0.05-0.20** (H100 ~$2-3/hour × 5-15분 / 60)

---

## §5 차단 요인 재기술 (잔존)

원본 audit 의 #78 차단 요인 ("Zeta API key 부재 + durable anima endpoint 부재") 정정 후 **실제 잔존 차단**:

### 5.1 anima self endpoint 가동 (잔존, 진짜 차단)

- Mac local: `tool/serve_alm_persona*.hexa` (또는 동등 launcher) 가동 — 0.5-1시간
- RunPod: dispatch (이미 다른 task 에서 정착) — 5-10분

### 5.2 Likert judge 자동화 종류 결정 (잔존, 진짜 차단)

`bench/persona_lore_style_bench.hexa` 의 deterministic scorer 가 어떤 measure 를 사용하는지에 따라:

- **Option α**: deterministic scorer (token / lexicon / structural) — auto, 즉시 가능
- **Option β**: LLM judge (e.g. Claude / GPT-4 self-judging Likert) — auto, $1-5 cost
- **Option γ**: 사람 rater (≥3 raters per item × 20 prompts × 6 persona × 5 dim = 1,800 ratings) — 5-20시간 사람 노력

(다른 inspection agent 가 본 errata 와 race-isolated 로 `docs/zeta_likert_inspection_*` 를 정확화 진행 중 — 본 errata 는 그 결과 의존하지 않음. judge 종류는 #78 LIVE path 의 다음 결정 사항.)

### 5.3 외부 의존

**없음** — Zeta API 호출 0, broker 0, 변호사 0, regulatory 0. 모든 측정이 anima 자체 + (선택적으로) LLM judge 1개 API key 정도.

---

## §6 LIVE 충족도 estimate 갱신

원본 audit §0.1 표:

| clause | raw 충족도 | LIVE 충족도 | 임시공개 verdict |
|---|---:|---:|---|
| **#78 제타** | 22.5% | 2.5% | NOT-OK |

### 6.1 본 errata 적용 후 가능 update (사용자 직접 측정 후)

**가정**: §4 의 2-4시간 (Mac) OR 5-15분 (RunPod) 측정 1회 실행 + 결과가 anima Likert ≥ Zeta baseline (즉 nat ≥ 3.2, coh ≥ 3.0, sty ≥ 2.8) 충족.

| criterion | 이전 classification | 측정 후 가능 classification | 가중 |
|---|---|---|---|
| 78-a Likert ≥ 3.0 (100 pair blind A/B) | RED MISSING (0.0) | **GREEN** (1.0) — 측정 ≥3.0 충족 시 OR **RED MISSING** (0.0) — 미달 시 |
| 78-b 응답 latency <1s | RED MISSING (0.0) | latency 동시 측정 가능 → **GREEN/RED** decisive |
| 78-c 30 turn 세션 유지 | GREY SPEC-ONLY (0.2) | 변동 없음 (별도 30-turn run 필요) |
| 78-d 5 카테고리 coverage | GREY SPEC-ONLY (0.2) | **GREEN** (1.0) — frozen v1 이미 5 cat × 4 prompt 충족 |

raw 충족도 estimate (Likert ≥3.0 가정):
- (1.0 + 1.0 + 0.2 + 1.0) / 4 = **0.80 → 80%** (이전 22.5% 대비 +57.5%p)

LIVE 충족도 estimate:
- 78-a/b/d LIVE 측정 충족 + 78-c SPEC-ONLY: (1.0 + 1.0 + 0 + 1.0) / 4 = **0.75 → 75%** (이전 2.5% 대비 +72.5%p)

**raw#10 honest C3**: 본 estimate 는 **측정 전 추정**. 실제 anima Likert 결과가 Zeta baseline 미달이면 78-a 는 RED MISSING 잔존 → raw 충족도 ≤ 30% 가능 (78-d GREEN 만 추가). 본 errata 는 ETA / 외부의존 / cost 정정만 확정, 충족도 % 갱신은 측정 후 별도 doc.

---

## §7 raw#10 honest C3 disclosure (errata 자체에 대한)

1. **본 errata 는 원본 doc 을 amend 하지 않음** — raw#1 history immutability 준수. forward errata 만 (commit `143414f08` 그대로 유지).
2. **§4 의 ETA 추정 (2-4시간 / 5-15분) 은 측정 전 estimate** — Q4_K_M Mac M4 throughput, vLLM RunPod throughput, deterministic scorer cost 모두 추정값. 실측 후 ±50% 변동 가능.
3. **§5.2 의 Likert judge 종류 (α/β/γ) 결정은 본 errata scope 외** — 다른 inspection agent (`docs/zeta_likert_inspection_*` 정착 중) 의 결과로 확정.
4. **§6 의 충족도 estimate (raw 80% / LIVE 75%) 는 "Likert ≥ Zeta baseline 충족" 가정 의존** — Likert 결과 미달 시 raw ≤ 30%.
5. **78-c "30 turn 세션 유지" 는 본 errata 정정 대상 아님** — 별도 30-turn run 필요 (frozen prompt set 은 single-turn 20 prompts).
6. **본 errata 는 .roadmap #78 entry 정정 commit 을 직접 수행하지 않음** — §10 권고만, 사용자 승인 후 별도 commit.
7. **Zeta = Scatter Lab Spotwrite-1 baseline source 의 attribution 정확성** 자체 (3.2/3.0/2.8 이 Spotwrite-1 의 실제 published score 인지) 는 본 errata 가 검증 X — `bench/persona_lore_style_bench.hexa:10` 주석 만 cite.
8. **본 errata 의 root cause 추정 (§2)** — 원본 audit agent 의 추론 경로는 본 agent 의 reconstruction. Task #14 agent log 직접 검토 X.

---

## §8 사용자 catch 인정 (한 줄)

사용자 directive 2026-04-29 "제타 API 연결이 아니야" — **정확함**. 원본 audit doc commit `143414f08` 의 Task #14 agent 가 Zeta = 외부 SaaS API 로 추정한 것은 코드 본인 (`bench/persona_lore_style_bench.hexa:10` + `bench/zeta_likert/v1_frozen.json`) 을 직접 inspection 하지 않고 .roadmap 표현에서 추측한 결과. 사용자 catch 가 본 errata 를 trigger.

---

## §9 raw#71 falsifier 3건 preregister (errata 자체 대상)

본 errata 의 정정 ("Zeta = hardcoded baseline + ETA 2-4시간 + 외부의존 0") 을 falsify 할 수 있는 측정/이벤트:

1. **F1 — 실측 ETA > 4시간 (Mac) OR > 15분 (RunPod)**: §4 estimate 가 throughput 추정 오류일 가능성. 실측 후 ETA 1.5x-3x 초과 시 §4 표 갱신 필요.
2. **F2 — Likert deterministic scorer 가 사람 rater 만 가능 (Option γ enforced)**: `bench/persona_lore_style_bench.hexa` 내부 scorer 가 human annotation 의존 코드 (예: 사전 annotated reference 만 비교) 이면 §5.2 의 Option α 자동화 가능 가정 무효 → ETA 5-20시간 사람 노력 가산.
3. **F3 — `bench/zeta_likert/v1_frozen.json` 의 prompt set 이 100 pair criterion 미달**: 20 prompts × 5 cat = 100 pair 인지 OR 20 prompts only (5 cat 분포만) 인지 ambiguity. 100 pair 미달이면 prompt 추가 수집 0.5-2일 필요. (검증: §6 의 "blind A/B" semantics 에서 1 pair = (anima 응답, Zeta baseline) 비교이므로 20 prompt × 5 dim × ? = 적합성 재확인 필요.)

falsifier 발생 시 본 errata doc 갱신 (chflags noschg → 수정 → chflags uchg) 필요.

---

## §10 권고

### 10.1 본 errata commit 적용 (즉시)

본 doc 만 add. `.roadmap` / 원본 audit doc / `state/` mutation 0.

### 10.2 .roadmap #78 entry 정정 (사용자 승인 후 별도 commit)

원본 .roadmap line 1218 #78 exit_criteria 자체는 변경 불필요 ("Likert ≥ 3.0 (100 pair blind A/B vs Zeta)" — Zeta 가 hardcoded baseline 이라는 정정만으로 criterion 의미 변동 0).

다만 `.roadmap` 또는 `state/zeta_likert_result.json` 의 `blockers` 필드에 "Zeta API key" 항목이 있으면 **삭제** 필요 (해당 blocker 는 허위). 사용자 승인 후 별도 commit.

### 10.3 #78 LIVE 측정 즉시 실행 권고 (본 errata 의 후속)

§4 의 Mac local 2-4시간 OR RunPod 5-15분 path 중 하나 선택 → 측정 1회 실행 → §6 의 충족도 estimate 확정. ETA / 비용 모두 매우 낮으므로 임시공개 path 의 highest-ROI step.

(별도 #78 실측 agent 가 race-isolated 로 `state/zeta_likert_p4_r8_*` 정착 중 — 본 errata 와 동시 실행 가능.)

---

## §11 race-avoidance

- 본 errata 는 `docs/cp2_clauses_p4_r8_satisfaction_audit_2026_04_29_errata.md` (신규) 만 추가
- 원본 audit doc (`docs/cp2_clauses_p4_r8_satisfaction_audit_2026_04_29.md`) mutation 0 (raw#1 immutability)
- `.roadmap` / `state/` / `bench/` / `anima-agent/` mutation 0
- 동시 실행 agents 와 race-isolated:
  - Task #16 의식 fix-cycle — 분리 (state path 다름)
  - zeta inspection agent (`docs/zeta_likert_inspection_*`) — 분리 (다른 doc)
  - #78 실측 agent (`state/zeta_likert_p4_r8_*`) — 분리 (state path 다름)

---

## §12 raw#91 honest 5축 요약

- **counter (반대 측정)**: 본 errata 의 ETA estimate (2-4h Mac / 5-15min RunPod) 은 throughput 추정값. 실측이 1.5x-3x 초과 가능 (F1 falsifier).
- **write-barrier**: 본 errata doc 만 추가, 원본 audit + .roadmap + state mutation 0.
- **no-fab**: §4 ETA / §6 충족도 estimate 모두 측정 전 추정 명시 (raw#10 disclosure §7).
- **citation**: 모든 evidence file:line cite (`bench/persona_lore_style_bench.hexa:10`, `:671-673`, `bench/zeta_likert/v1_frozen.json` schema/prompt_count/category_coverage 모두 verbatim).
- **verdict-options**: errata 정정 = ETA / 외부의존 / cost 만 확정, 충족도 % 갱신은 측정 후 별도 doc (§7-4 disclosure).

---

end of errata #1.
