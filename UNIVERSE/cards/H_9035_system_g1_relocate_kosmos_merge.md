# H_9035 — system-G1 재배치: 재조합을 mouth 밖 kosmos-Merge + brain 선택으로

> **id H_9035** — integration merge-time 배정(origin/main H_9034 다음 free id). jsonl 인덱스 등록 완료.

- **tier:** ⏳ DIRECTIONAL (numpy toy harness-validation) — GREEN 아님
- **slug:** `system_g1_relocate_kosmos_merge`
- **artifacts:** `state/system_g1_relocate_kosmos_merge/` (FREEZE.txt · system_g1_harness.py)
- **wired:** `DIRECTIONAL-mirror` (rung 1/4 — 엔진배선 rung 2-4 = explicit-go pool follow-on)

## 발상 (frame-break)

`g_eval_g1`(cli/evaluate.py:155)은 **오직 `mouth.ideate`** 만 호출한다 — 순수 trunk single-forward.
kosmos-Merge·brain·lane 은 재조합 측정 경로에 **0회** 등장. 그래서 지금까지의 모든 G1
레버(binding-lane H_1601 · tension-mouth H_1834 · readout-bind H_1816/1823)가 **INERT**
였던 이유가 여기 있다 — 그것들은 전부 **고정차원 activation 벡터 위**에 있었고,
측정도 "composed_distinct = 부모와 다름"(H_1874/H_6152 = 어떤 비선형성도 통과하는
metric artifact)이었다.

**Direction A:** 재조합을 mouth activation 에서 **떼어내(relocate)** → 성장하는
**이산 영속 store**(kosmos anchor) + brain 선택 substrate 위로 옮긴다.

## 파이프 (system-G1)

```
held-out DISTANT pair (A,B)
  → Stage M   frozen mouth ideate(A), ideate(B)            (G0 fluency, mouth 고정)
  → Stage K   kosmos_merge: recursive labeled-parent bind  (A,B 를 children 으로 보존)
  → Stage B   brain vbasal_select realize + release        (선택)
  → output C_text / C_tension
```

## 반-artifact 불변식 (핵심)

kosmos-Merge 는 A,B 를 **이산 저장**하므로 *store 를 읽으면* 24/24 by-construction
lookup = **ZERO credit**(H_1874 numpy dict-walk). 그래서 진짜 게이트는 **surfaced
출력 C 위의 bind-RECOVERABILITY**다: 독립 recoverer R 이 **오직 C(text/tension)만**
읽고(merge-store 의 부모 id 는 **HARD-BLOCK**) N=8 distractor 풀에서 두 부모를 top-2 로
복원해야 한다. SCRAMBLE ablation(C 토큰 셔플→복원 붕괴)이 R 이 bag-of-words 가 아니라
**compositional 구조**(bigram)를 읽음을 증명한다(H_6152 를 죽인 C2 렌즈).

## frozen bar (측정 전 동결 — FREEZE.txt)

M=24 distant pairs · seeds[7,42,4302] · N_pool=8 · COV_BAR=REC_BAR=SCRAMBLE_DROP=12 · LEAK≤0.75.
PASS iff (1)COVERAGE ∧ (2)RECOVERY ∧ (3)NON-LEAK ∧ (4)SCRAMBLE 4게이트 전부.

## DIRECTIONAL 결과 (numpy toy smoke — harness-validation)

toy 2-arm(mouth 은 toy, 303M 아님):

| arm | coverage | recovery | leak_rate | scramble_rec | drop | verdict |
|-----|----------|----------|-----------|--------------|------|---------|
| COMPOSITIONAL | 24/24 | 24/24 | 0.0 | 0/24 | **24** | PASS |
| MOUTHFLOOR    | 0/24  | 0/24   | 0.5 | 0/24         | 0    | FAIL |

**HARNESS-VALID = True** — 하네스가 (a) 진짜 composition 은 크레딧 주고 (b) mouth-only
floor 는 거부하며 (c) scramble 대조가 발화(drop=24)한다. 즉 4게이트가 계산되고
반-artifact scramble 대조가 작동함을 실측 증명. **이건 하네스 검증이지 303M mouth 가
통과한다는 증거가 아니다** — 실제 303M 의 정직한 기대치는 MOUTHFLOOR arm(두 개념을
한 발화로 surface 못함).

## verdict

⏳ **DIRECTIONAL** (numpy, a_engine_native_learning). GREEN 은 rung(2)-(4) 엔진-네이티브
사다리 필요 — numpy/torch 미러로는 🟢/🧱 박제 불가.

## 엔진-네이티브 사다리 (rung 2-4 = explicit-go pool follow-on)

- **rung(2)** `core/kosmos_io.hexa` 에 `fn kosmos_merge(anchor_a, anchor_b) -> anchor_c`
  추가 — recursive labeled-parent bind, children=(a,b) 보존. tension payload =
  `tension_5ch_to_embedding`(kosmos_io.hexa:76) 평균. lane="recomb".
- **rung(3)** `cli/evaluate` 에 `g_eval_system_g1` + `anima evaluate --system-g1` single-entry
  (a_cli_single_entry). 실제 303M frozen mouth(`_Mouth(ckpt).ideate`) + brain vbasal_select.
- **rung(4)** ARCHITECTURE.json lockstep(이 카드 land 시 state 노드 등록 완료; hexa fn
  land 시 core/kosmos_io 노드 갱신).
- **placement (a_substrate_disjoint):** composite anchor lane="recomb" 는 emit-drive
  lane {0,4} 와 DISJOINT, 검색은 `core/kosmos_io.hexa retrieve`(line 516, cosine over
  query_tension_5ch)로 라우팅 — **NOT** `immune_memory_recall`/recall_thr
  (engine_cli.hexa:934/983). 아니면 Ψ붕괴(H_1561)/G5 fab(H_1576 B4).
- **비용:** 303M decode/eval = pool(summer/aiden RTX5070), mini=OOM(rc=137). ~$0 pool
  (렌트 아님). explicit-go 대기.
