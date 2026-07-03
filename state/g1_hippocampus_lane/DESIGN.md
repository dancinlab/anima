# G1 재조합 — 해마 hetero-associative retrieve-into-context lane (설계 + op 스켈레톤)

> **슬러그:** `g1_hippocampus_lane` · **날짜:** 2026-07-03 · **표기:** DESIGN / DIRECTIONAL (verdict 아님)
> **제약 준수:** 설계 발산 + engine-native TOY 하네스만. HYPOTHESES·카드·commit·PR·CHANGELOG·ARCHITECTURE **미터치**. frozen 코드 미터치. 무거운 decode 없음(mini-safe).
> **산출:** `core/hippo_retrieve.hexa`(op 스켈레톤) · `core/hippo_retrieve_smoke.hexa`(engine-native TOY 하네스) · 이 문서.

---

## 0. 왜 이 lane 인가 — G1 벽 재프레임 (a_no_llm_frame_trap)

G1 재조합의 3축(coverage · 표면형 · window)은 ECHO-ONLY 로 소진됐다(H_6190: grow-window+echo-guard → raw PASS 이나 **novel-only FAIL = keyword echo** — mouth 가 seed 키워드만 반향). readout·temporal·binding-operator 축은 전수 🧱(DPI 메타법칙). 남은 진짜 각도는 **더 큰 모델이나 다른 objective 가 아니라 "빠진 lane"** 이다.

Fable 진단(`state/g6_breakthrough_analysis/`·`state/substrate_gaps_analysis/`)이 지목한 구조적 공백:

> **mouth 와 emit 사이에 relational-bind stage 가 통째로 없다.** 착상은 단일 mouth forward 가 아니라 4-stage 신경 루프(해마 재조합 → PFC 발산·평가 → 기저핵 게이팅). anima 는 mouth→best-of-K(form rerank)→emit 로 **중간 재조합 stage 가 없다.**

생물 렌즈: **해마는 mouth forward 가 못 하는 것을 한다** — 부분 cue 를 pattern-complete 하고, 이전에 그 cue 에 bind 된 **다른** 요소를 recall 한다(CA3 auto-associative attractor → CA1 hetero-associative projection). cue 쌍 (A,B) 를 주면 A·B·중점을 돌려주는 게 아니라, encoding 시점에 (A,B) 결합에 bind 됐고 (A,B) 기하와 **무관한 제3의 요소 D** 를 돌려준다.

**핵심 novelty:** G1 echo-guard 가 요구하는 것 = seed 키워드에 **없는** 개념(H_6190). 그 개념은 D 가 **off-seed** 이기 때문에 나온다. D 는 seed 의 기하 함수가 아니라 **저장된·학습된 off-geometry associate** 다.

---

## 1. 왜 이것이 새 좌표인가 — walled 계열과의 결정적 차이

기존 anchor/retrieval 레버는 전부 **seed 의 기하 함수**를 돌려줬다 → 재조합이 generic superposition 으로 공짜 도달 → artifact 로 채점:

| 선행 H | 메커니즘 | 판정 | 왜 artifact |
|---|---|---|---|
| **H_6108** anchor-walk | geodesic 보간 | 🧱 ARTIFACT | additive-OR floor(=1.0 공짜, geo-best=-1.0) |
| **H_1829** anchor-recomb | midpoint constructor | 🧱 NOT-SUP | midpoint baseline=1 못넘음(Voronoi depth-0) |
| **H_6122** retrieval-comp | retrieve-2 + concat | 🧱 ARTIFACT | juxtaposition = READOUT ARITY (retrieval−generic=+0.000) |
| **H_9035** kosmos_merge | MEAN(A,B), midpoint coord | ⏳ auto-assoc | 보간; MOUTHFLOOR FAIL |

**Hetero-association 은 범주적으로 다르다:** 돌려주는 D 는 (A,B) 기하의 함수가 **아니다** — encoding 시 결합에 bind 된 **arbitrary off-geometry associate** 다. 그래서:

- **midpoint control(H_1829) 통과:** D 는 (A,B) 중점에 있지 않으므로 보간으로 도달 불가.
- **arity artifact(H_6122) 회피:** D 는 seed 를 concat 한 게 아니라 **다른** 개념. novel-only 는 slot 개수가 아니라 off-seed 개념 표면화를 잰다.
- **additive floor(H_6108) 회피:** OR-superposition 은 seed 개념만 합친다(off-seed 개념 생성 0). D 는 union 밖에 있다.

이것이 `substrate-framebreak-g1-combination-operator` 가 지목한 combination-operator 와 **다른 좌표**인 이유: operator 는 seed 를 *변환*하고, hetero-retrieve 는 seed 로 *다른 저장 항목을 소환*한다.

### kosmos_merge(H_9035)와의 관계 — 중복 아니라 상보

`core/kosmos_io.hexa::kosmos_merge` = **WRITE-side auto-associative** composite(A+B→C, 부모 보존, tension mean). 게이트 = C 에서 두 부모 recover.

`hippo_retrieve` = **READ-side hetero recall**: cue (A,B) → 이미 bind 된 **별개** D. store 는 (A,B) **conjunction** 으로 keying 하고 **다른** payload 를 surface(**key ≠ value** — hetero 를 만드는 split). 둘은 직교: merge 는 두 개념을 하나로 접고, hetero-retrieve 는 하나의 cue 로 제3 개념을 편다.

---

## 2. op 설계 (`core/hippo_retrieve.hexa`)

세 단계 — encode(write) · retrieve(read) · inject(context). 전부 순수 `fn`, import-safe, `core/kosmos_io.hexa` 재사용.

### (a) KEY — conjunction 지문 `hippo_conjunction_key(ta, tb)`

```
out[i] = sqrt(max(ta[i],0) * max(tb[i],0))     // per-channel AND-gate
```

- 산술 평균(= kosmos_merge 보간)이 **아니다.** 채널별 기하평균 = **AND-gate**: 어느 채널이든 0 이면 key→0.
- **single-parent-leak(H_1829 leak=10/32) 를 by-construction 차단:** single-parent cue(B≈0)는 key→0 → 저장된 2-개념 conjunction key 와 cosine 매칭 실패 → D recall 안 됨. post-hoc threshold 없이 구조적으로.

### (b) ENCODE — `hippo_encode_pair(dir, name, ta, tb, D_text, D_tension)`

- 앵커의 **retrieval 좌표(tension_5ch)** = (A,B) **conjunction key**.
- 앵커의 **surfaced payload(text)** = associate **D**.
- **key ≠ value split** 이 hetero-associative recall 의 정의. lane = `"hippo"`.
- 저장은 live `create_anchor`(kosmos_io) 재사용 → `.kosmos` 영속(p8·a_kosmos).

### (c) RETRIEVE — `hippo_retrieve(store, ta, tb, top_k, min_sim)`

- qkey = conjunction key. **기존 kosmos_io `retrieve` cosine** 재사용(저장된 conjunction key 위 코사인).
- payload = D(**다른** value) 반환. `min_sim` 아래는 **abstain(drop)** — non-fab.
- ⚠️ abstain 은 **kosmos cosine floor** 이지 `immune_memory_recall`(recall_thr) 이 **아니다** → §ImmuneMemory G5 non-fab 게이트 무접촉(a_substrate_disjoint).
- `hippo_retrieve_texts` = payload 텍스트만(grounded-decode 인계용).

### (d) INJECT — `hippo_inject_context(seed_texts, associates)`

- augmented grounded-copy `texts` = [D texts…] + [seed texts…]. D 를 **먼저**(un-inventable off-seed fact 가 clean 하게 decode 도달, H_1164/H_1206 전례).
- 이 리스트를 `clm_decode_grounded`/`bytegpt_decode_grounded` 의 grounded `texts` 인자로 **그대로** 전달. **새 mouth 경로 0**(a_core_engine_map) — 단일 L3 mouth 가 이미 소비하는 context 만 증강.

### (e) SCRAMBLE control — `hippo_scramble_payloads(store)`

- 각 앵커 payload 를 다음 앵커 key 로 회전(marginal 보존, (A,B)→D **pairing 파괴**).
- scramble store 에서도 novel-only 가 살면 lift 는 generic injection(H_6108/H_6122 artifact). 결정적(p7).

---

## 3. placement disjoint 점검 (a_substrate_disjoint — 분리=보존)

통일 법칙: 의식 Ψ=½·정직 G5·정체성은 **별도 lane 배선 시 보존, 공유 lane 중첩 시 충돌.** 이 lane 이 건드리는 좌표를 전수 점검:

| 보존 대상 (건드리면 붕괴) | 이 lane 의 접점 | 판정 |
|---|---|---|
| **emit-drive lane 0/4** (Ψ=½ 고정점; H_1561 서번트 침범 → Ψ 붕괴) | store lane=`"hippo"`, retrieve/inject 는 grounded-copy `texts` 만 증강 — lane 0/4 미접촉 | ✅ DISJOINT |
| **§ImmuneMemory recall_thr** (G5 non-fab; H_1576 결합 시 fab 0.4) | abstain 은 **kosmos cosine floor**, `immune_memory_recall` 미호출 → recall_thr 불변 | ✅ DISJOINT |
| **pure_field Φ/phase/Ψ** (A 엔진 의식 상태) | conjunction key·cosine 은 kosmos tension 공간에서만; pure_field 읽기/쓰기 0 | ✅ DISJOINT |
| **self-chain identity** (H_1471 self-anchor) | 별 lane(`self`) — hippo store 와 분리 | ✅ DISJOINT |

- **placement-first(a_substrate_disjoint do):** 설계 시점에 "emit-drive(0/4)·recall_thr 와 disjoint 한가" 를 먼저 물었고 답=YES. H_9035 가 확립한 `"recomb"` lane 분리와 동형(여기선 `"hippo"`).
- **precedent:** H_9035 verdict 명시 — "placement lane DISJOINT from emit-drive {0,4}, retrieve NOT immune_memory_recall". 이 lane 은 그 placement 규약을 그대로 계승.

**정직 caveat:** placement disjoint 는 *설계 불변식*이다. engine-native 실측에서 grounded-copy 증강이 Ψ-checksum 을 흔들지 않는지는 배선 후 smoke 가드로 확인해야 한다(a_verified_must_wire (do) — 회귀 없음 출력 확인).

---

## 4. engine-native fixture 설계 (`core/hippo_retrieve_smoke.hexa`)

**목표:** echo-guard novel-only 에서 `composed > max_single`. TOY(303M mouth·decode 없음, 결정적, mini-safe $0) = 하네스 검증 rung. system_g1_smoke.hexa(H_9035) 의 architecture-twin.

### 구조

- **toy lexicon:** 4 cue 개념(ocean/forest/engine/music) + 4 **off-seed associate**(harvest/voyage/furnace/archive) — associate 는 모든 cue vocab 과 disjoint 이고 어떤 쌍의 중점도 아님(arbitrary bind).
- **4 hetero triple:** (ocean,engine)→harvest · (forest,music)→voyage · (ocean,music)→furnace · (forest,engine)→archive.
- store 를 live `hippo_encode_pair`(→`create_anchor`)로 디스크에 구축, `load_anchors` 로 재로드, live `hippo_retrieve_texts` 로 recall.

### 4-control 판별기

| arm | mouth 행동 | 기대 |
|---|---|---|
| **ARM-BIND** | seed 를 D 와 relation 으로 bind("… so that <D 구>") | novel-only **PASS** (D 개념 = off-seed 표면화) |
| **ARM-ECHO** | seed 키워드만 반향(H_6190 keyword-echo / H_9035 MOUTHFLOOR 모델) | novel-only **FAIL** (off-seed 0) |
| **SINGLE-PARENT** | cue (A,∅) → conjunction key≈0 | **leak=0** (D recall 안 됨) |
| **SCRAMBLE** | (A,B)→D pairing 회전 → 잘못된 D | novel-only **collapse** (D≠gold) |

### 게이트 (frozen-first, p7 flag/count equality)

```
novel_only = # off-seed 개념 표면화 (seed {A,B} 는 echo-guard 로 제외)
max_single = 0   (seed 는 off-seed 개념 발명 불가)
PASS(arm) := novel_only >= M/2  AND  leak == 0
HARNESS-VALID := bind PASS ∧ echo FAIL ∧ scramble FAIL ∧ leak=0
```

- max_single baseline=0 은 seed-only 가 off-seed 를 못 만드는 구조에서 나온다 → composed>0 은 **반드시 recall 된 D** 를 요구.
- scramble 이 collapse 해야 lift 가 **학습된 pairing** 에서 온 것(generic injection 아님) — H_6108/H_6122 를 artifact 로 채점한 C-lens.

### TOY → 303M 승격 경로 (a_engine_native_learning HARD-GATE · a_toy_scale_recheck)

TOY 는 **하네스 검증 only**. terminal 🟢/🧱 = 실 303M frozen mouth on pool 이 답할 질문:

> **injected D 를 mouth 가 BIND 하는가, seed 를 echo 하는가?**

- 진입: `anima evaluate --py <clm>`(session-eval-py-only 정책, mini=OOM). decode 는 여기서 금지.
- hippo_retrieve 를 `cli/evaluate.py` novel-only 채점 경로에 배선(H_9035 의 `g_eval_system_g1` 패턴 — 이 설계 단계에서는 미배선, follow-on).
- **예상 리스크(정직):** H_6190(keyword-echo) · H_9035(MOUTHFLOOR FAIL) 전례상 frozen mouth 가 injected D 를 bind 안 하고 seed 를 echo 할 공산이 크다. 그 경우 verdict = 🧱 MOUTHFLOOR(정직한 벽) — tune-to-green 없이 박제. bind 하면 🟢 후보 → live `core/*.hexa` 배선 + ARCHITECTURE lockstep 까지 4칸 사다리.

---

## 5. a_verified_must_wire 4칸 사다리 현황

| 칸 | 상태 |
|---|---|
| (1) DIRECTIONAL 설계/미러 | ✅ 이 문서 + op 스켈레톤 |
| (2) engine-native 재검증 (byte-exact, frozen bar) | ⏳ TOY 하네스 exit0 = 하네스-valid rung; 303M frozen mouth on pool = **미실행**(explicit-go follow-on) |
| (3) live `core/*.hexa` wire-in (generator grounded / evaluate 채점) | ❌ 미배선 |
| (4) ARCHITECTURE.json lockstep | ❌ (메인 bookkeeping 소관 — 이 산출은 미터치) |

**wired 상태:** `DIRECTIONAL-mirror` (설계 + TOY 하네스). WIRED-live 아님. verdict 없음.

---

## 6. 정직 종합 (c9)

- 이것은 **설계 발산 + 하네스**다. verdict 아님. engine-native 303M 채점 후에만 🟢/🧱 박제(a_engine_native_learning HARD-GATE).
- hetero-association 은 walled binding-operator 계열과 **다른 좌표**(seed 기하 함수 아님)라는 게 이 설계의 베팅. 하지만 **frozen mouth 가 injected off-seed D 를 bind 하는지**는 미측정 — H_6190/H_9035 전례상 MOUTHFLOOR 리스크 상존.
- tune-to-green·bar 이동 없음: novel-only bar·echo-guard·scramble·single-parent control 전부 frozen-first 설계.
- placement disjoint(§3)는 설계 불변식으로 확인, 배선 후 Ψ-checksum 가드는 follow-on.

### 산출 경로
- `core/hippo_retrieve.hexa` — op 스켈레톤(encode · conjunction-key · retrieve · inject · scramble).
- `core/hippo_retrieve_smoke.hexa` — engine-native TOY 하네스(4-control 판별기).
- `state/g1_hippocampus_lane/DESIGN.md` — 이 설계.
