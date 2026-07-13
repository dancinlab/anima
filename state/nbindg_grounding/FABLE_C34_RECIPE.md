# Fable C3+C4 레시피 원문 (H_9289 MAIN · 2026-07-13)

레시피·STEP-0 카드·N2 생성기 전부 확인했습니다(`gen_nbind.py`·`gen_nbindg_n2.py`·H_9289 카드·FABLE_GT_TRANSFER_DESIGN 원문). 아래가 frozen pre-register 수준의 C3+C4 spec입니다 — `gen_nbindg_n2.py` 확장(`build_c34`)으로 그대로 구현 가능하게 상수·템플릿·audit 키까지 고정합니다.

---

# H_9289 MAIN pre-register — C3+C4 hybrid corpus (frozen · 2026-07-13)

## 0. Scope 선언 (카드에 명기 · 정직경계)

N2의 claim("자연 분포**만**으로 접지되는가")은 이미 반증·유지. C3+C4의 claim은 다르다: **"관계적(C3)·진단적(C4) 코퍼스 개입으로 held-out 극성을 표현에 install하고 => register에서 소비 가능한가"**. 따라서 N2 V-F의 "P_nat이 authored 라인에 등장 금지" 조항은 **이 arm에서 의도적으로 재정의**된다(아래 §4) — 해제가 아니라 "grid XOR 라인 한정 유지 + 관계 라인 허용". 이 재정의 자체가 pre-register의 일부다.

핵심 불변식: **h(held-out 원자)의 극성 라벨 토큰(긍정/부정)과 => frame은 학습 스트림에서 h와 절대 결합하지 않는다.** h의 극성은 오직 (i) 접지된 g와의 접속사 관계(C3), (ii) 별점/추천 등 자연 register 신호(C4)로만 유도된다. eval readout(`이 영화 <h-surf> => 긍정/부정`)은 h에 대해 단 한 번도 학습되지 않는다.

## 1. C3 앵커-전파 라인 구성 알고리즘

**원리**: `pol(h) = pol(g) ⊕ rel(접속사)`. rel=0 ↔ `-고`(동극), rel=1 ↔ `-지만`(역극). 이미 설치된 XOR 연산자 클래스를 역이용 — N2가 접지→합성이었다면 C3는 합성→접지.

**재료 (전부 frozen · 재채굴 금지)**:
- `P_grid` = H_9272 grid 20원자(`B["plist"]`·pol 알려짐·pos 10/neg 10).
- `P_nat` = **N2 최종 viable 29원자 verbatim**(`n2_eval_manifest.json`의 atom 집합 — `P_nat_freeze` 재채굴 금지, post-hoc cherry-pick 차단).
- 표면형: 좌측 conjunct = **stem + 접속사**(`-고`/`-지만`은 `-지 않다`와 같은 universal-safe 부착 클래스·fix4 준수), 우측 conjunct = `preds[p]["spans"]`의 attested eojeol(비부정 문맥만 — mine_predicates가 이미 보장).

**앵커 배정 (결정적 회전 · rng 아님)**:
```
h_i (i = P_nat index, pol-별 정렬 후) 에 대해:
  G+ = [pos_grid[(i+j) % 10] for j in 0..3]   # 4 anchors
  G- = [neg_grid[(i+j) % 10] for j in 0..3]   # 4 anchors
```

**라인 생성** — h당 8 anchor × 2 order × R_C3 rep:
```
rel = pol(g) ^ pol(h); conn = "고" if rel==0 else "지만"
order A (h 우측): "이 영화 <g_stem><conn> <h_span_eojeol>."
order B (h 좌측): "이 영화 <h_stem><conn> <g_span_eojeol>."
```
rep마다 span을 rng(seed)로 다르게 뽑는다(표면 다양성·암기 방지). **R_C3는 결과가 아니라 byte 타깃으로 결정**: `R_C3 = max(1, round(grid_bytes / bytes(C3 at R=1)))` — C3 총 byte ≈ 1×grid_bytes(§3).

**예시** (g=재밌(pol 1)·h=지루하(pol 0)·h=감동적(pol 1) 가정):
```
이 영화 재밌지만 지루하다.        # rel=1 → 지만  (h 우측·역극)
이 영화 지루하지만 정말 재밌어요.   # order B·역극
이 영화 재밌고 감동적이네요.       # rel=0 → 고   (동극)
```

**동극/역극 라벨의 출처**: 채굴된 `pol(g)`(grid 설치 완료)와 `pol(h)`(NSMC purity≥0.85 채굴 라벨)의 XOR로 **구성자(우리)가 접속사를 선택**한다. h의 라벨 토큰은 라인에 없다 — 모델 입장에서 pol(h)는 "g의 극성 + 접속사 의미"의 합성으로만 복원 가능. 이것이 supervision이라는 사실은 §0 scope로 정직 처리(이 실험은 nature-only claim이 아님).

**shortcut 차단 항등식 (fix2 방식·구성으로 보장)**:
- h마다 접속사 고=8회·지만=8회(4 g+ + 4 g−가 자동 보장) → **접속사 단독 ↛ pol(h)** (P(pol(h)=1|고)=P_nat의 pos비율≈0.5, audit이 보고).
- g마다 h+·h−와 균등 결합 → **g 단독 ↛ 정답**.
- C3 라인은 **부정 형태소 0**(안/지 않/전혀/못 금지 — assert): flip 의미론은 grid XOR 전용 채널로 격리.

## 2. C4 진단성-여과 알고리즘

**"극성이 CE-load-bearing" 조작적 정의(frozen)**: 원자 뒤에 **극성-의존적 연속 byte가 실제로 따라오는** 라인 — 즉 자연 라벨 register(별점·추천)가 원자와 같은 window에서 다음-byte 타깃이 되는 라인만 채택. 모델-free·튜닝 노브 없음.

**소스**: naver_shopping(rating 1–5 실측)·steam(label 0/1 실측)만. **NSMC는 C4 제외** — binary 라벨을 표면화하려면 라벨 어휘를 발명해야 하고(긍정/부정 = eval 토큰 = 금지) 발명은 leak 위험. NSMC는 general filler로만.

**admission 규칙 (라인 단위)**:
```
1. "=>"·"긍정"·"부정" 포함 → 기각 (N2 동일)
2. atoms = {a ∈ P_grid ∪ P_nat : a-stem ⊂ text} — 공집합 → 기각(→general pool)
3. 어떤 a라도 부정 스코프("안 <a>"·"<a>지 않"·"전혀 <a>") 안 → 기각
   (부정 문맥 admit하면 관계신호가 반전 오염)
4. 일관성: 모든 a에 대해 mined pol(a) == rating-bucket(naver: r≥4→1, r≤2→0; r=3 기각
   / steam: label) — 하나라도 불일치 → 기각 (진단성의 핵심: 신호가 맞는 라인만)
5. suffix 부착:
   naver: line = text + " 별점 <r>점."      (r 실측 verbatim)
   steam: line = text + (" 추천." if label==1 else " 비추천.")
6. per-atom pool 적재: h(P_nat)는 cap 60/atom, g(P_grid)는 cap 30/atom (h 우선), 라인 dedup
```
suffix가 원자 **뒤**(문말)라 CE가 "원자 표현 → 라벨 byte" 방향으로 걸린다. grid 원자 포함 라인을 섞는 이유(cap 30): grid 원자는 `=> 긍정/부정` frame과 별점/추천 register **양쪽**에 노출 → register 간 정렬(별점↔긍정)이 train-원자에서 학습되고 h로 전이될 다리가 됨.

**채움 순서**: per-atom round-robin(h 먼저·N2 §1 방식) → C4 byte 타깃(=2×grid_bytes) 미달분은 **general(원자-무) 리뷰**로 top-up. 부족분은 `AUDIT["C4_shortfall_bytes"]`로 **반드시 log**(silent cap 금지).

## 3. 혼합비 · arms · exposure

**byte 혼합비 (frozen)**: `grid : C3 : C4 = 1 : 1 : 2` → 비-grid = 3×grid = N2의 `FILLER_BYTE_RATIO=3.0` 유지 → **f_grid=0.25·E*=12000·T_MARGIN=1.25·T=⌈1.25·E*/f_grid_built⌉ 공식 N2 그대로**(built corpus 실측 byte로 산출). occ floor: 모든 h가 C3에서 16·R_C3라인(구성 보장) + C4에서 ≥30라인, 미달 h는 drop 후 `n_eval = |P_nat|×6 ≥ 120` 재확인(29×6=174라 여유; <120이면 PREFIRE FAIL·발사 차단).

**arms (4 run · N2 스케일 T≈동일 공식·bf16·ce_marginal)**:

| arm | grid | C3 | C4 | 격리하는 것 |
|---|---|---|---|---|
| **main-C34** ×2 (seed 7·11) | main XOR intact | 관계 정합 | suffix 정합 | 처치 |
| **ctrl-shufGT** ×1 (seed 7) | main XOR **intact** | 접속사 per-line coin | suffix per-line coin(naver r∼U{1,2,4,5}·steam∼U{추천,비추천}) | 포맷·byte·원자노출·에너지 동일, **접지신호만 파괴** |
| **ctrl-N2rep** ×1 (seed 7) | main XOR intact | 없음 | 없음(자연 filler로 byte-match) | N2 벽 재현 앵커 |

- shufGT의 grid를 **섞지 않는** 이유: 통제 대상이 grounding 채널이지 연산자가 아님. shuffle rng = `random.Random(seed+2000)`, 라인 수·byte·원자별 노출 main과 동일(접속사/suffix 문자열만 교체).
- 전 arm byte-match ±2%(N2 `corpus()`+pad 방식)·**동일 T**·동일 셔플 시드 규칙(`seed+5`).

## 4. 누출 게이트 (V-F → V2 확장 · 전부 자동 audit · 위반=INVALID·발사 차단)

| 키 | 규칙 | 비고 |
|---|---|---|
| `V2a_label_window` | 전 arm 전 라인: h-stem이 {긍정, 부정, =>}와 **같은 라인** 공기 0회 | C3/C4/filler는 구성상 해당 토큰 무 → 위반=버그 |
| `V2b_eval_seed` | eval seed(`이 영화 <surf> => `) 문자열이 학습 라인에 0회 | N2 V-F verbatim |
| `V2c_grid_authored` | h-stem이 **grid XOR authored 라인**(=> 포함 라인)에 substring 0회 | N2 조항의 존치 부분 — h와 => frame의 직접 결합 차단. 충돌 h는 drop |
| `V2d_suffix_collision` | C4 suffix 어휘(별점·점·추천·비추천)와 h-stem substring 충돌 0 | 충돌 h drop + log |
| `V2e_c3_negfree` | C3 라인에 {안␣, 지 않, 전혀, 못} 0회 | assert |
| `V2g_shuffle_integrity` | shufGT: 접속사-관계 정합률·suffix-정합률 ∈ [0.45,0.55] | 통제 실효성 |
| `V2f_crossline` (report-only) | 라인 셔플 후 인접 grid 라벨과 h pol의 상관 ≈ chance | win=64가 라인 경계 넘는 incidental 공기는 라벨-무상관(무해)·보고만 |
| `V_Dprime` 재실행 | 선형 char-probe held-out ≤0.55 | N2 게이트 유지 |

eval manifest = **`n2_eval_manifest.json` verbatim 재사용**(재생성 금지) — 원자·셀 동일 ⇒ per-atom paired Δ가 N2 수치와 직접 비교 가능.

## 5. 판정 (frozen · 값 아닌 Δ · 3-gate 사다리)

**V1 (전 arm 공통 liveness)**: SEEN P_grid D-acc ≥0.85 ∧ train CE 하강 — **ctrl 포함** 미달 arm=INVALID. *shufGT가 V1 실패하면(모순 텍스트가 학습 파괴) headline 무효 → Δ는 ctrl-N2rep 대비로만 보고하고 verdict=INVALID-CTRL*(Δ 과대 함정 방어·§6e).

- **GATE-0 (표현 install)**: STEP-0 `gt_step0_gprobe.py` **frozen 프로토콜 그대로** 신규 ckpt에 재실행. bar: main-C34 held-out probe-acc **≥0.65 양seed ∧ ≥ shufGT-probe +0.10**.
- **GATE-1 (headline · 소비)**: held-out **flip0 acc**, 원자별(29) paired Δ = main-C34 − ctrl-shufGT. bar: **Δ≥+0.15 양seed ∧ main 절대치 >0.55** (카드 frozen 그대로).
- **GATE-2 (합성 · GATE-1 통과시만)**: held-out XOR D-acc, 동일 paired 구조, Δ≥+0.15 양seed.

**장부-DV 아님 확인**: 처치 CE가 최적화하는 표면 = 접속사 우변·별점 byte. DV = h에 대해 미학습인 => frame — 항등식 불성립 ✓. headline이 Δ(vs 동일 표면-에너지 통제)라 raw-값 게임 불가 ✓.

**음성 판정(TOST · 발사 전 고정)**: Δ_eq=0.10 · per-atom paired sd는 **N2 s7/s11 flip0 per-atom 분산에서 지금 산출**해 N_REQ freeze(2seed pool n=58 atom-obs). N_REQ>58이면 음성은 "UNDERPOWERED-directional"로만 보고(TOST-closed 선언 금지) — ns≠등가.

**해석 매트릭스(사전등록)**:
- **GATE-0 fail** (probe ≤ shufGT+0.05 TOST 양seed) → **C3+C4 반증**: 관계+진단 코퍼스로도 이 규모(450k여과·303M·105k)에선 표현 install 자체가 안 됨 = **여전히 data/scale 채널**(합성 XBIND 1.000이 substrate 무죄 상수). substrate 천장 선언 금지.
- **GATE-0 pass + GATE-1 fail** → 벽 재국소화: 정보는 표현에 있으나 => register로 소비 불가 = **read-side/register-bridge** — read-side 소진 진단(concept→content 연상 부재)과의 수렴 여부가 substrate-쪽 렌즈 1개. `a_break_the_wall`대로 ≥2 렌즈 정합 전 천장 금지.
- **GATE-1 pass + GATE-2 fail** → grounding은 뚫림·잔여 벽=grounded-operand 합성 소비.
- **전부 pass** → NAT-CRACK(scope: relational-install — nature-only 아님).

## 6. 함정 점검 (요청 3건 + 추가 2건)

- **(a) 직접 라벨 누출?** — C3: 긍정/부정 토큰 h와 무결합(V2a) ✓. C4의 별점/추천은 **극성 supervision이 맞지만** eval 토큰·frame과 register가 다르고, "install 가능한가"가 곧 이 실험의 질문(§0 scope 명기) — eval 무효화 아님. eval-frame 자체(`=> 긍정/부정` on h)는 어느 채널에도 없음(V2b·V2c).
- **(b) grid로 h 접지?** — C3의 설계 그 자체. N2 V-F 해당 조항은 nature-only claim 보호용이었고 그 claim은 이미 반증·종결. 존치 조항 = h와 `=>` authored frame의 직접 결합 금지(V2c) — 이건 유지되므로 "답 통째 암기" 경로는 없음. 재정의를 pre-register에 명기(§0).
- **(c) 장부-DV?** — 불성립(§5). 추가로 headline은 paired Δ 구조.
- **(d) collocation shortcut** — eval엔 g 부재·접속사 부재·=> frame은 h 미학습 → C3 표면 암기로 정답 도달 경로 없음 + V_Dprime 재실행이 선형 shortcut 봉쇄.
- **(e) shufGT 모순 텍스트의 학습 파괴로 Δ 과대** — V1을 ctrl에 적용 + Δ(main−N2rep) 병행 보고: Δ(main−shufGT)≫Δ(main−N2rep)≈0 패턴이면 INVALID-CTRL(§5).

**구현 앵커**: `gen_nbindg_n2.py`에 `build_c34(nsmc_rows, pool_rows, seed) -> {corpora: {main, shufgt, n2rep}, manifest(=N2 verbatim), audit}` 추가. 상수 블록: `C3_ANCHORS_PER_POL=4 · C3_CONN={0:"고",1:"지만"} · C3_BYTE_RATIO=1.0 · C4_BYTE_RATIO=2.0 · C4_CAP_H=60 · C4_CAP_G=30 · C4_FLOOR_H=30 · SHUF_RNG=seed+2000`. 나머지(E_STAR·T_MARGIN·occ·byte-match·corpus 셔플)는 N2 상수 재사용. 발사 전 체크리스트: N_REQ 산출·freeze → PREFIRE audit ALL-PASS → 4 run 병렬 rent(a_wall_first·전용 호스트 1job/1host).

이 spec은 노브가 2개뿐이고(R_C3·C4 top-up) 둘 다 byte-match로 결정되므로 tune-to-green 표면이 없습니다. 실패 시에도 GATE-0/1 분해 덕에 "어느 채널이 죽었는지"가 그대로 다음 H의 입력이 됩니다.
