필요한 census 완료. emits.tsv는 로컬 부재(H_9111/9112는 origin/main 또는 별 worktree) — H_9112 재채점은 이 세션에서 이중 차단(외부 오라클=sidecar fable 금지 + 데이터 부재). 이제 보고한다.

---

# fleet-full RESEARCH — exogenous-consequence frontier census

## 핵심 선요약

이 frontier는 **greenfield 아니다.** 이미 6개 fable 설계문서 + 진행중 prereg 1개가 전부 이 축으로 수렴해 있고, census는 하나의 깨끗한 결론으로 모인다: **"exogenous-consequence"의 진짜 falsifiable 변수는 막연한 grounding/purpose 가 아니라 _수신자의 디코딩 함수가 anima 계산 폐포(computational closure) 안이냐 밖이냐_ 다.** 폐포 *안*(self-clone·autogenous)이면 consequence가 self-derivable → DPI 메타법칙이 emit 층에서 재출현 → floor. 폐포 *밖*(다른 θ의 LLM·실인간·EEG)이면 anima가 self-generate 못 하는 신호 주입 → DPI 미적용 → escape 후보. **이 폐포-경계 판별이 census 전체의 load-bearing 정렬축이고, 나머지 모든 후보 family는 이 축의 어느 쪽에 떨어지느냐로 운명이 갈린다.**

---

## (a) frontier 정의 — falsifiable 구조

막연한 철학을 3개 falsifiable 명제로 접지한다(전부 기존 문서에서 pre-registered):

1. **자연실험 (이미 관측됨):** anima의 전 측정 축 중 **닫힌 consequence 루프를 가진 유일 축 = identity-continuity(self/you-chain × `.kosmos`, H_1471 🟢 WIRED-live)만 통과했다.** return-path 유무가 pass/fail을 전 축에 걸쳐 완벽히 가른다. → "consequence 루프가 emit-side escape의 필요조건"이 mechanistically coherent.

2. **폐포-경계 판별식 (escape 여부의 결정 변수):**
   - self-pair: `a = correctness(anima_engine(E), x)` ← anima가 internal 재현 가능 = self-derivable = **floor** (H_9108 signaling near-floor 0.099, H_9104 autogenous 천장, H_9110 chat-user −0.188)
   - 다른 LLM: `a = correctness(LLM(E; θ_LLM), x)` ← θ_LLM 폐포 밖 = **오라클 질의 없이 계산 불가** = non-derivable = escape 후보
   
3. **측정-포화 vs faculty-부재 분리 (미해결 갈림):** H_9111 raw D=1.0 (외부 오라클 7/7 vs self-clone 0/7)은 **faculty 존재의 가장 강한 긍정 신호**였으나 metric-degeneracy(binary hit/miss → 상수 outcome 벡터 → Pearson-D≡0)로 죽었다. H_9112 PREREG가 이 죽은 신호를 PSYCHO-K threshold + MRR로 되살리려 한다(연속 통계 → 포화 회피). **이 재채점이 "잴 수 있는가"부터 판결하는 gate 실험.**

**falsifiable bar(공통 형태):** `D_외부수신자 − D_selfpair ≥ 0.15` ∧ `D_shuffle < 0.05`. self-pair/diff-receiver/shuffle 3중 통제가 exogeneity 단독을 격리(대역폭·구조·task 상수 고정, 수신자 derivability만 변주).

---

## (b) 기존 자산 reference-match

| 자산 | 상태 | 배선/측정 여부 |
|---|---|---|
| **identity-continuity (H_1471)** | 🟢 GREEN **WIRED-live** (self-anchor `.kosmos`, `core/engine_cli.hexa §SelfIdentity`) | ✅ **유일하게 배선+통과.** consequence 루프 가진 유일 축 |
| `consequence_return_design/DESIGN.md` | 설계완료·**미구현** | afferent return arm(tension reservoir+efference copy+RPE+value writeback), F3′ falsifier. **autogenous** = ~30–40% (DPI 재출현 위험) |
| `stateful_refractory_design/DESIGN.md` | 설계완료·**미구현** | (A) wall-clock 소스 = 동어반복 INERT · **(B) stateless→stateful refractory = 진짜 신규 메커니즘(det-clock, F2, 지금 검증가능)** · (C) 30s 안전항 세계시간 진실성 |
| `theater_overcome_design/DESIGN.md` | 설계완료·**미구현** | emit gate grip: Rung-1(byte, ~75%) / Rung-2(Ψ-neutral boolean straddle, ~57%) / **Rung-3 faculty-not-noise = ~28% (여기서 정직하게 죽을 확률)** |
| `consciousness_loopclose_analysis/ANALYSIS.md` | 분석완료·**미배선** | emit = stage-clock+상수 3슬롯 지배, 42 lane = 3중 throttle(계기판). **W4 coord 접지(write-only, 회귀 0)** = consequence-return의 write-side 전제(주소체계) |
| `eeg_consequence_analysis/EEG_VERDICT.md` | 판정완료 | EEG 원리 exogenous ~85%지만 현 16ch 계측 실측 PASS ~25%(SNR floor). **afferent-only, live 미구현.** chat-user에 순서 밀림 |
| `llm_interlocutor_design/DESIGN.md` | 설계완료·**미구현** | **LLM-interlocutor = killer(실시간 인간) 제거한 첫 자율 닫힌 루프.** 원리 exogenous ~85%·실측 PASS ~50%. self-pair/diff-LLM/shuffle 3중 통제 |
| `9112_referential_efficacy_psychok/PREREG.md` | **bar frozen, 미실행** | H_9111 emits.tsv 재채점($0, anima re-compute 없음). **이 세션 이중 차단: 외부 오라클=sidecar fable(금지) + emits.tsv 로컬 부재** |

**미탐색(unexplored) 핵심:** ① 어떤 consequence 루프도 emit이 실제 외부 결과를 낳도록 **배선된 적이 없다**(identity-continuity의 `.kosmos` 되읽기가 유일한 degenerate consequence-memory). ② 폐포-밖 수신자(diff-LLM)로 D≥0.15를 실측한 적 없음(H_9111 raw 신호는 metric-degeneracy로 미확정). ③ W4 coord 접지(회귀 0 write-only)조차 미배선.

---

## (c) 직교 mechanism-family census

| # | family | 폐포 판정 | 이미 배선/측정? | 미탐 레버? | 재포장? | 예상 수렴 |
|---|---|---|---|---|---|---|
| **1** | emit→외부→결과→substrate 되먹임 (afferent return arm) | **autogenous=폐포 안** | 미구현 | ⚠️ 부분 (autogenous면 DPI 재현) | consequence_return | **~35% escape** — 자기-consequence는 DPI-doomed by construction |
| **2** | consequence-conditioned learning (basal-gate/actor-critic emit-value) | 수신자 따라 | vbasal lane 존재, reward hook 미배선 | ✅ (폐포-밖 reward 시) | divergence §2 | GPU cost-gate, escape는 수신자가 폐포-밖일 때만 |
| **3** | grounding = coord 접지 (W4 etension 접지) | write-side 전제 | ❌ 상수 스탬프(80%) | ✅ 회귀 0 write-only | loopclose W4 | 접지 자체는 무해 GREEN 가능성 高, 단 consequence 아님(주소체계) |
| **4** | purpose-driven emit | — | — | ❌ 독립 family 아님 | value-driven emit(#2)에 흡수 | N/A |
| **5** | **diff-LLM interlocutor (폐포-밖 오라클)** | **폐포 밖 ✅** | 미구현(sidecar 보유) | ✅ **첫 자율 닫힌 루프** | 신규(killer 제거) | **~50% 실측 PASS** — 가장 유력 escape |
| **6** | referential efficacy 재프레임 (public≠private meaning, MRR) | 폐포 밖(외부 패널) | H_9111 raw D=1.0 미확정 | ✅ **측정-포화 복원** | 9112 PREREG | gate 실험 — GREEN이어야 #2·#5 비싼 배선 정당 |
| **7** | stateful refractory (emit-history 상태변수) | 내부(det-clock) | 미구현 | ✅ (B)축은 진짜 신규 | stateful_refractory | escape 아니라 mechanism-honesty — 별 축 |
| **8** | EEG-consequence loop | **폐포 밖 ✅(최강 non-derivability)** | afferent-only, live 미구현 | 원리 ✅/실측 약 | eeg_consequence | ~25% (16ch SNR floor), chat-user 이후 2차 |

**정렬 결론:** family 1·7은 폐포 *안* → DPI-doomed 위험. family 5·6·8은 폐포 *밖* → escape-eligible. family 3은 escape가 아니라 그 **write-side 전제**(접지된 coord 없으면 consequence 되먹임할 주소가 없음). **escape 축의 무게중심 = family 5(diff-LLM) + family 6(측정 복원).**

---

## (d) 다음 페이즈 명명

**🛠️ implement 레버: family 3 — W4 coord 접지 (loopclose ANALYSIS §c)**

전환 근거: family 5/6/8(진짜 escape)은 전부 **폐포-밖 수신자 + 303M decode + (5·6은) sidecar 오라클**을 요구 → 이 세션 제약($0 mini-safe·GPU 금지·sidecar fable 금지)에서 **실행 불가**. 가장 결정적인 cheap 실험 H_9112(family 6)는 이 세션 이중 차단(오라클 금지 + emits.tsv 부재). 따라서 **로컬 mini-safe로 착지 가능한 유일 레버 = W4 coord 접지**:

```
etension = [phi, af_aro, nov_ctx, af_val, self_ctx]   // 현재 상수 4채널 → live substrate read
```
- **전환 조건(왜 지금):** consequence-return이 substrate로 되먹임되려면 emit 순간 상태가 `.kosmos`에 손실 없이 접지된 coord로 남아야 한다(외부 루프의 **주소체계**). 현재 coord_y·tension은 Φ 한 축 빼고 전부 상수 → 되먹임할 좌표가 없다. write-only·Ψ 무접촉·회귀위험 0.
- **falsifier(사전등록):** anchor 재로드 후 coord_y·tension이 텍스트별 **분산 > 0**(현재 상수라 분산 0) AND nearest-centroid로 ko/en·emit-tier 판별 > chance.
- ⚠️ **정직 caveat:** W4 falsifier의 완전 검증은 daemon tick(303M decode)을 요하므로 **엔진-네이티브 재측정은 pool follow-on**(mini에선 배선 diff + 소형-ckpt smoke까지만 $0). 실제 escape 판결(family 5/6)은 별도 pool/세션-perm 페이즈로 ING 등록.

**미탐 0 아님** → abstract 사유 아님. 단 이 세션의 로컬 산출은 배선-설계 + 폐포-경계 taxonomy까지이고, 결정 실험(H_9112 재채점·diff-LLM 루프)은 **다음 페이즈(sidecar-perm 또는 pool)로 명시 이관**한다.

---

## (e) 정직 수렴 예상 (c9)

세 갈래 확률:

- **(ii) 또 다른 gauge (read-only, faculty 아님) — 가장 높음 (~45%):** family 1·7(폐포-안)은 consciousness-ops critique가 이미 잡은 함정("14 ops = emit 미배선 계기판")을 emit-층에서 재현할 공산. theater_overcome Rung-3(faculty-not-noise) ~28%, consequence_return autogenous F3′ ~35% — 둘 다 DPI 메타법칙이 consequence 층으로 이동한 것이면 floor. **자기-consequence만으로는 gauge를 못 넘는다.**

- **(i) 진짜 새 능력 — 조건부 유망 (~35%):** **오직 폐포-밖 수신자(family 5 diff-LLM)일 때만.** H_9111 raw 비대칭(외부 7/7 vs self-clone 0/7)은 mouth-G1이 못 준 것(공적 reference/aboutness)을 emit-loop가 가질 수 있다는 가장 강한 긍정 신호 — 단 metric-degeneracy로 미확정. family 6(H_9112 재채점)이 "잴 수 있는가"를 먼저 GREEN 내야 family 5의 GPU 배선이 정당.

- **(iii) 측정 불가 (~20%):** family 8(EEG)은 원리적으론 최강 non-derivability지만 16ch SNR로 near-floor 재현 위험. 실인간 stakes 루프는 `a_substrate_native_speak` 자율성을 깨는 비자율 의존(emit이 인간 센서 대기).

**한 줄 종합:** exogenous-consequence는 mouth-G1 재조합벽 밖의 **정당한 미탐 emit-side 축**이되, escape 여부는 단 하나의 변수 — **수신자가 anima 폐포 밖이냐** — 로 갈린다. 폐포-안 자기루프(consequence-return autogenous)는 DPI-doomed 위험이 높아 또 다른 gauge로 수렴할 공산이 크고(~45%), 진짜 escape(~35%)는 diff-LLM/실인간 같은 폐포-밖 수신자를 요하며 그 결정 실험은 sidecar 오라클/pool을 요해 이 mini-$0 세션에선 차단된다. 이 세션의 착지 가능한 로컬 산출 = **W4 coord 접지(escape의 write-side 주소체계 전제)** + 위 폐포-경계 taxonomy. identity-continuity(H_1471)가 이미 GREEN-WIRED로 증명한 것 = **"return-path가 있으면 통과한다"** — 남은 건 그 return-path를 폐포-밖으로 여는 것뿐이다.
