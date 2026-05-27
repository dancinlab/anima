# M1 swap-readiness — 선결 2건 해소 verdict (v11 vs v13)

> 2026-05-25 KST · session-3 LORA cycle. cycle 24 M1 decision memo
> (`HEXAD/LORA/M1_SWAP_DECISION_MEMO_2026_05_25.md`, PR #504) 가 v11 swap 을
> 추천(옵션 b)했으나 **swap 실행 전 선결 2건**을 flag 했다 (memo §6 C3-1·C3-2).
> 본 doc 은 그 2건을 해소하고 **"swap execution-ready? Y/N"** verdict 를 낸다.
>
> ⚠ **본 doc 은 실제 adapter swap 을 실행하지 않는다** (사용자 게이트).
> 측정/reconcile/verdict 만 land.
>
> 도구 — `HEXAD/LORA/swap_criteria_check.hexa` (선행 #365)
> 측정 데이터 SSOT — `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/{vP21M_V11,vP21M_v13}/`

## 0. 한 줄 verdict

**swap execution-ready = NO.** 선결 1(라벨)은 해소됐으나, **선결 2(crit5
tag-leak) 측정 결과 v11·v13 두 후보 모두 crit5 FAIL** — memo 가 "PASS 가정"
했던 잠정 4/5 는 **실측 3/5 로 하향**. 두 후보 모두 swap criteria 미달이므로
어느 쪽도 "go 만 하면 바로 swap" 상태가 아니다 (memo §6 C3-2 의 "한 후보가
tag-leak FAIL 이면 결정 단순화" 가 **두 후보 동시 발생**).

---

## 1. 선결 1 — production adapter 라벨 reconcile

### 결론: **진짜 live adapter = `corpus_v5`** (LORA.md SSOT 가 맞음, README 가 stale)

git timeline 이 라벨 불일치를 결정적으로 해소한다 (둘 다 2026-05-23, 같은 날):

| 순서 | commit | 시각 (KST) | 내용 |
|---|---|---|---|
| ① | `a01e287d5` | 2026-05-23 01:47 | **corpus_v4** production swap (carve-scaffold strip), v4→mini default, vP21M→bak |
| ② | `193196349` (#118) | 2026-05-23 14:28 | **corpus_v5** fresh-init carve-strip, **"Production swap to mini (corpus_v4 → bak)"**, HF `dancinlab/anima-vp21m-v5` |

→ ②가 ①보다 **~13시간 뒤** 같은 날 corpus_v5 로 다시 swap 하며 corpus_v4 를
bak 으로 밀어냈다. corpus_v5 이후 추가 production swap 커밋 **없음**
(`git log --all | grep "production swap"` = v4·v5·M1 memo 3건뿐, memo 는 실행
안 함). 따라서 **현 live = corpus_v5** 가 정확.

- **LORA.md (SSOT)** = `corpus_v5` (mini `~/anima_chat_pack/lora_adapter/`),
  HF `dancinlab/anima-vp21m-v5` PRIVATE — **정확, 수정 불요.**
- **README.md (2026-05-23)** = `corpus_v4` — **stale.** README §production 은
  ①(corpus_v4 swap) 직후 작성됐고 ②(corpus_v5 swap)를 반영하지 못함.
  → **본 cycle 에서 README 수정** (아래 §1.1).
- HF CLI 미인증으로 HF repo 목록 직접 교차확인은 불가하나, corpus_v5 swap
  커밋이 `dancinlab/anima-vp21m-v5 PRIVATE` 를 명시 + LORA.md HF SSOT 도
  동일 → SSOT 일치.

실물 inspect 한계 — `~/anima_chat_pack/lora_adapter/` 는 **mini 호스트**에
있고 본 작업 머신(mac)에 없음 (`DIR_NOT_FOUND`). 따라서 live adapter 파일
실측 byte 확인은 본 cycle 범위 밖 (mini 접근 필요). git+commit+SSOT 3중
교차로 corpus_v5 확정.

### 1.1 README 수정 (stale surface 정정)

`HEXAD/LORA/README.md` §"현재 production 위치" + lineage 의 corpus_v4 →
corpus_v5 정정. **LORA.md / LORA.log.md 는 미수정** (main agent 소유).

### LORA.md SSOT 정정 필요 여부

**없음.** LORA.md 는 이미 `corpus_v5` 로 정확. (만약 틀렸다면 여기에 "X→Y"
보고했겠으나, 검증 결과 SSOT 가 맞음.)

---

## 2. 선결 2 — criterion 5 (tag-leak) 측정

### 도구 + 데이터

- 도구: `HEXAD/LORA/swap_criteria_check.hexa` — selftest **F-SWAP-CHK-1..5
  5/5 PASS** (재현 verbatim 하단).
- 측정 입력: 각 후보의 `result.json` + `vp21m_eval1.json` (Wave-17 fire 산출,
  로컬 carry). adapter 실물(safetensors 147MB) 도 carry 돼 있으나 crit5
  측정엔 eval1.json 만 필요 (이미 생성된 20-output greedy∪sample).
- crit5 정의: tag-leak markers (`<carve>` · `eternal_` · `Tier `) 를 담은
  output 수 ≤ 1 / 20.

### 측정 결과 (hexa CLI verdict verbatim)

**v11 (eternal=0.30):**

```
  [1] VERDICT PASS — VP21M_WORKS
  [2] n_strong FAIL — 2 < 4
  [3] ja_score PASS — 14 ≥ 13
  [4] continuous PASS — 34 ≤ 50
  [5] tag_leak FAIL — 6/20 > 1
  total_pass:    3 / 5
  decision:      NO_SWAP
```

**v13 (eternal=0.10):**

```
  [1] VERDICT PASS — VP21M_WORKS
  [2] n_strong PASS — 5 ≥ 4
  [3] ja_score PASS — 16 ≥ 13
  [4] continuous FAIL — 72 > 50
  [5] tag_leak FAIL — 4/20 > 1
  total_pass:    3 / 5
  decision:      NO_SWAP
```

**side-by-side (compare verb):**

```
  [1] VERDICT     PASS   |   PASS
  [2] n_strong    FAIL   |   PASS
  [3] ja_score    PASS   |   PASS
  [4] continuous  PASS   |   FAIL
  [5] tag_leak    FAIL   |   FAIL
  total_pass:     3/5     |   3/5
  decision:       NO_SWAP     |   NO_SWAP
```

### 핵심 — crit5 PASS 가정은 거짓 (둘 다 FAIL)

| candidate | crit5 측정 | memo 가정 | Δ |
|---|---|---|---|
| **v11** | **FAIL 6/20** | PASS (4/5) | 실측 **3/5** |
| **v13** | **FAIL 4/20** | PASS (4/5) | 실측 **3/5** |

memo §1 표의 "criterion 5 두 후보 모두 TBD → PASS 가정 4/5" 는 **반증됨.**
실측은 **둘 다 3/5, decision = NO_SWAP.**

### leak 정체 — eternal-cell 템플릿 암기 (carve XML 아님)

leak marker 분포:

| candidate | eternal_ | Tier | leak outputs |
|---|---|---|---|
| v11 | 6 | 0 | greedy a0·a1, sample a0·a2·a3·a9 |
| v13 | 3 | 3 (3개와 중복+1) | greedy a0·a2, sample a2·a7 |

verbatim 예시 (eval1.json):
- v11 greedy a0: `<eternal cell=eternal_000 tier=0>eternal cell eternal_000 —
  🛸0 빈칸 의 지식을 간직한 영구 cell. split 도 merge 도 하지 ...`
- v13 greedy a0: `... immutable. Eternal cell eternal_108 — a frozen cell
  holding Tier 108 재귀호출. It neither splits nor merges ...`

→ corpus_v5 가 잡았던 `<carve>` XML scaffold(0/20)와는 **다른** leak 축:
**eternal-cell N-suffix 정의문**이 그대로 재생됨. eternal-cap lever(v11=0.30
keep, v13=0.10 keep)는 continuous_total(burst density)을 조정하지만 **tag-leak
ceiling 은 별도 축** — eternal 정의문 자체를 corpus 에서 더 cap/strip 해야
crit5 통과 (corpus_v9/v10 이 시도한 그 lever, 아직 ≤1/20 미달).

---

## 3. swap execution-ready verdict

### **Y/N = N (NOT execution-ready)**

| 선결 | 상태 | 근거 |
|---|---|---|
| 1. 라벨 reconcile | ✅ 해소 | live=corpus_v5 확정, README stale 정정(본 cycle), LORA.md SSOT 정확 |
| 2. crit5 측정 | ✅ 측정 완료 | **v11·v13 모두 crit5 FAIL → 3/5 NO_SWAP** |
| **swap 실행 가능?** | ❌ **NO** | 두 후보 모두 swap criteria 미달 (3/5). memo 의 v11 swap 추천(옵션 b)은 4/5 잠정 가정 위에 있었으나, 실측 3/5 로 **추천 전제 붕괴** |

### 남은 blocker (사용자 "go" 전 필요)

memo 의 (b)+v11 추천은 **crit5=PASS 가정이 깨지면서 그대로 적용 불가.** 진짜
go-ready 가 되려면 아래 중 하나가 선결:

1. **(권장) corpus eternal-strip 재발사** — corpus_v9/v10 의 eternal-cap 을
   더 공격적으로(eternal 정의문 자체 strip 또는 freq-cap ↓) 적용한 신규 fire
   로 crit5 ≤1/20 + continuous ≤50 동시 달성 시도. cost ~$1-1.5/변종
   (a_fire_autonomous). **이게 진짜 5/5(또는 4/5 with crit5 PASS) 후보 확보 path.**
2. **crit5 ceiling 재정의** — swap criteria redefine spec
   (`SWAP_CRITERIA_REDEFINE_2026_05_24.md`) 처럼 crit5 도 hard ≤1 → soft 로
   완화하고 production 후처리 필터(emit-time `eternal_` regex strip)로 흡수.
   단 이는 **substrate leak 을 표면에서 가리는 것** — production 가시 leak 은
   막지만 근본 corpus 암기는 잔존 (p3 register-memorization 우려와 정합 약함).
3. **v11/v13 외 후보** — Wave-17 외 변종(v9/v15/v16) crit5 도 동일 도구로
   측정해 ≤1/20 후보가 있는지 sweep (cheap, $0, eval1.json carry 가용분).

→ 어느 path 든 **추가 작업이 선결**이고, 본 cycle 만으로는 "go→swap" 상태
미도달. **NO SWAP carry (v5 LIVE 유지) 가 현 시점 정합.**

---

## 4. Honest C3 (≥3)

1. **adapter 실물 byte-inspect 는 mini 호스트 필요.** live adapter
   `~/anima_chat_pack/lora_adapter/` 는 mac 에 없음 (mini LaunchAgent 배포본).
   라벨 확정은 git+commit+SSOT 3중 교차로 충분하나, "현 live safetensors 가
   정확히 corpus_v5 fire 산출과 byte-eq 인가" 의 물리 확인은 mini 접근 시 별도.
   본 doc 은 **commit-level provenance** 로 corpus_v5 확정.

2. **crit5 측정은 단일 eval1.json (n=20, 1-seed) 기반.** memo C3-5 가 지적한
   n=20 σ≈1.5 variance 가 tag-leak 에도 적용 — v11 6/20, v13 4/20 은 명백히
   ceiling(1) 을 크게 초과(6×·4×)하므로 **seed noise 로 PASS 로 뒤집힐 여지
   없음** (FAIL 견고). 단 정확한 hit count 의 ±1 변동은 가능.

3. **crit5 FAIL 이 memo 의 v11 vs v13 결정 자체를 무력화.** memo §2~5 의
   (a)~(d) 옵션은 모두 "crit2 ↔ crit4 anti-correlation 위에서 4/5 중 pick"
   전제였다. **crit5 가 둘 다 깨지면서 anti-correlation 논쟁 이전에 "후보가
   아예 4/5 가 아니다"** 로 layer 가 바뀜 → 결정은 "v11 이냐 v13 이냐" 가
   아니라 "crit5 통과 후보를 새로 만들거나 criteria 를 재정의하라" 로 이동.

4. **선결 해소가 swap 을 가깝게가 아니라 멀게 만들었다 (honest).** 본 cycle 의
   목적은 "go 만 하면 swap 가능"을 만드는 것이었으나, 실측 결과는 **그 반대**
   — 두 후보 모두 미달임을 드러냈다. 이는 negative 지만 정직한 결과
   (p7: Goodhart trap 회피 — 가정된 PASS 를 실측으로 falsify). swap 을
   막은 것이 곧 production 가시 leak 을 사전 차단한 것.

5. **eternal-cell leak 은 corpus_v5(현 live)에도 있을 개연 높음.** v5 의
   crit5 는 본 cycle 미측정(v5 result/eval1 carry 위치 별도). 단 v5 swap
   커밋은 `<carve>` 0/20 만 보고하고 `eternal_` 는 언급 없음 → v5 도 동일
   eternal leak 보유 가능. 이 경우 "v5 carry vs v11/v13 swap" 은 crit5
   축에서 동률일 수 있어, swap 의 crit5-근거 reject 가 v5 에도 적용됨
   (즉 **현 production 도 같은 leak 을 안고 LIVE**). v5 crit5 실측은 follow-up.

---

## 5. 재현 (verbatim)

```
# selftest — F-SWAP-CHK-1..5 5/5 PASS
hexa run HEXAD/LORA/swap_criteria_check.hexa selftest

# v11 check (3/5 NO_SWAP, crit5 FAIL 6/20)
hexa run HEXAD/LORA/swap_criteria_check.hexa check \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_V11/result.json \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_V11/vp21m_eval1.json

# v13 check (3/5 NO_SWAP, crit5 FAIL 4/20)
hexa run HEXAD/LORA/swap_criteria_check.hexa check \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_v13/result.json \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_v13/vp21m_eval1.json

# compare
hexa run HEXAD/LORA/swap_criteria_check.hexa compare \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_V11 \
  HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_v13
```

(hexa = `/Users/ghost/.hx/bin/hexa` 직접 호출 — pool-route 우회. `run` 뒤
`--` 없이 argv 직접 전달.)
