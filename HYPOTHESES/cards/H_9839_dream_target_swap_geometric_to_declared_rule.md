# H_9839 — 꿈의 타깃을 기하 중점에서 선언규칙 파생으로 교체한다 (R12-2)

**status:** 🟢 DIRECTIONAL POSITIVE — **코퍼스 사실**(모델 미통과 · $0 · ckpt 0 · GPU 0).
사전등록 판독 **충족**: `rule-derived` 가 기하-강건 최솟값에서 `midpoint` 와 `shuffled` 를
**둘 다** 이겼다 (3 추정기 × 2 seed = 6/6 셀). ⚠️ **TERMINAL 아님** — 학습 판정은 여전히
`anima-py train` + `anima-py evaluate` 몫이고, 압축 추정기는 **하한**이다(읽을 수 있음의 부재를
한정할 뿐 존재의 부재를 증명하지 않는다).
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** ✅ `anima-py corpus dreamgen` (`cli/corpus.py` · VERSION 0.20.97→0.20.98 · G5).
판정기 = 오늘 착륙한 `anima-py corpus mi-screen --mi-robust`(H_9844). 학습측 배선은 미구현(후속).

## 실측 전제 (한 건 **부분 철회**)

`core/dream_compose.py`(124줄, `origin/main` 에 실재 · `git ls-tree -r origin/main` 확인) 헤더가
스스로 밝힌다: 두 co-replay 앵커를 **"coord midpoint · tension5 mean · radius max · lane=dream"**
으로 섞는 **"a designed geometric law (NOT a learned semantic insight, c9)"**. `text` 는 빈
payload(NARRATIVE hook). 보유 함수 `dc_make_anchor`·`dc_vec_mid`·`dc_fmax`·`dc_cosine`·
`dc_stage_replay_budget`·`dc_coreplayed`·`dc_compose_dream_anchor`·`dc_compose_window` — 전부
빌더가 **직접 호출**한다(재구현 아님).

🔻 **철회**: 원 카드는 "기하 중점은 **정의상 가법적**이므로 `midpoint` 팔은 사전등록된 **실패
기준선**(= 정보 0)" 이라 썼다. **틀렸다.** `midpoint` 팔은 기하-강건하게 **READ 3/3** 이 나온다
(seed 7 gzip +0.0391 · ppm +0.0354 · markov6 +0.0997). 이유는 프로덕션 법칙 자체가 순수 평균이
아니기 때문이다 — `dc_compose_dream_anchor` 는 ① id 를 `dream(a000.0+a000.1)` 로 **양 부모 id
축자 복사**하고 ② `radius = dc_fmax(ra, rb)` 로 **한 부모의 radius 를 축자 선택**한다(실측 라인:
`ANCHOR a000.1 … r=0.9893` → `DREAM dream(a000.0+a000.1) … r=0.9893`). 즉 기하 법칙에도
**비-평균 축자 운반**이 두 군데 있다. ⟹ 올바른 DV 는 `midpoint` 팔의 **절대값**이 아니라
**팔 사이 대비**이고, 이 카드의 판정은 그 대비로만 읽는다.

## 착륙한 개입 (플래그)

```
anima-py corpus dreamgen --out c.txt --lang en \
    --dream-target {planted|pedestal|midpoint|rule-derived|shuffled} [--dream-nights 24] [--seed 7]
```

세 처치 팔은 **하나의 RNG 스트림**을 공유한다 — 앵커·coord·tension5·radius·선언규칙이 같은
`--seed` 에서 바이트 동일하고, **다른 것은 꿈의 `text=` payload 를 유도하는 법칙뿐**이다.

| arm | 법칙 | 역할 |
|---|---|---|
| `midpoint` | child token k = `pool_k[(idx_A_k + idx_B_k)//2]` — 프로덕션 `dc_vec_mid` 를 **직접 호출**해 계산한 토큰-인덱스 축별 중점 | 기준선 (프로덕션 기하 법칙을 text lane 으로 확장. 프로덕션은 `text=""` 인데 빈 payload 는 정의상 판독불가라 기준선이 공허해지므로 **법칙 자신의 확장**을 씀 — 숨기지 않고 명시) |
| `rule-derived` | 밤이 헤더에 3-슬롯 선택규칙 `RULE ABA` 를 **선언**하고, child token k = 규칙이 고르는 부모의 슬롯 k | 처치 (부모 하나만으로도, 규칙만으로도 결정 안 됨) |
| `shuffled` | `rule-derived` 와 **바이트 동일한 꿈 라인 다중집합**을 결정론적 회전으로 **틀린 밤에 재부착** | 주변분포 일치 통제 (구성만 파괴) |
| `planted` | 밤의 body 에 고엔트로피 블록, 다음 밤 머리에 그 블록 **축자** — `mi_compress.plant_crossboundary` 의 코퍼스판 | **양성통제** — 안 터지면 이 코퍼스 계열의 블록 배치가 판독불가 ⟹ 어느 팔도 못 읽음 |
| `pedestal` | 동일 구성에서 **carry-over 제거**(다음 밤은 자기 새 블록) | **참값 0 받침대** — 터지면 계기가 신호를 제조 |

**게이트 순서 동결**: `planted` 발화 ∧ `pedestal` 거부 를 **먼저** 확인하기 전에는 세 처치 행을
읽지 않는다(`positive-control-before-reading-a-negative` + `phi-estimator-needs-zero-truth-pedestal`).

### 스트림 모양 (판정기가 잴 수 있는 형태)

`stream_mi` 는 "세그먼트 t 의 **body** 가 t+1 의 **prefix** 를 t 의 마지막 `win` 바이트(**tail**)
이상으로 예측하는가" 를 묻는다. 그래서 밤 블록은 `dc_compose_window` 자신의 의미(윈도 w 에
replay 된 앵커들이 꿈 노드로 합성)를 스트림으로 옮긴 배치다:

```
[전날 앵커들로 합성된 DREAM 라인 21개]   ← 다음 세그먼트의 prefix
NIGHT 007 STAGE 3 BUDGET 7 RULE ABA      ← 선언
ANCHOR a007.0..a007.6 (7개 = dc_stage_replay_budget(3))
DRIFT ... × 150 (tail 을 채우는 표류 필러 · 앵커 어휘와 분리된 nonce 풀)
<빈 줄>
```

밤은 **빈 줄**로 나뉜다. 그래서 `MI.segments_from_path` 가 **모든 기하에서** 코퍼스 자신의 레코드
단위(밤)로 자른다 — `--mi-robust` 의 1/2·1/8 스윕이 **win/span 만** 흔들고 밤 구조를 재절단하지
않는다. **`--mi-seg-lines` 를 쓰면 안 된다**(1/8 기하가 밤을 8토막 내 시험 대상 구조를 파괴).
실측 확인: 세 기하 전부 `n_seg 24 · pairs 23`.

## 재현 커맨드 (seed 포함 통째 · corpus-py-1 (J))

```bash
python3 -m venv /tmp/venv_h9839
/tmp/venv_h9839/bin/pip install -q --force-reinstall --no-deps .      # repo root
for arm in planted pedestal midpoint rule-derived shuffled; do
  /tmp/venv_h9839/bin/anima-py corpus dreamgen --out $arm.txt --lang en \
      --dream-target $arm --dream-nights 24 --seed 7
  /tmp/venv_h9839/bin/anima-py corpus mi-screen --corpus $arm.txt --mi-robust --out mi_$arm.json
done
# seed-강건성: 위를 --seed 11 로 반복
```

## 실측 출력 (생성기 · verbatim)

```
anima-py corpus dreamgen [arm=rule-derived] -> .../s11_rule-derived.txt
  nights 24 · segments 24 · pairs 23 (MIN_PAIRS 20) · bytes 240698 · lines 4298
  block bytes 7109..10155 · body->tail margin >= 6149B (win 4096) · 21 dream(s)/night = C(7,2)
  --dream-nights moves the SEGMENT/pair count (the judge's power), never the block
  geometry: nights x 21 dream items, each night a fresh anchor draw, so it is not a
  repeat-exposure knob (corpus-py-3). Block size is a frozen constant, not a flag.
  carry multiset sha 6836c761f3b107a9 · geometry-field sha cc1d3c17e0b299f6
```

**빌더 witness (seed 7)** — `rule-derived` 와 `shuffled` 의 carry multiset sha 가 **동일**
(`be421d6cf1ab9c31`) ⟹ 주변분포 완전 일치, 짝만 파괴. `midpoint` 와 `rule-derived` 의
geometry-field sha 가 **동일**(`74c98f5a0919d70c`) ⟹ coord/t5/r 바이트 동일, `text=` 만 다름.
차단형 감사 5종(빈줄 분절 = 밤 수 · 최단 블록 ≥ win+span · body→tail 여유 > win · pairs ≥
`MI.MIN_PAIRS` · shuffle fixed_points 0)이 통과 못 하면 코퍼스를 아예 쓰지 않는다.

## 실측 판정 (`mi-screen --mi-robust` · `robust_over_floor` = 3 기하 **최솟값** · eps 0.02)

### ① 통제 먼저 (동결 순서)

| arm | seed | gzip | ppm | markov6 | 판독 |
|---|---|---|---|---|---|
| `planted` | 7 | **+5.8438** | **+0.8371** | **+5.3128** | 🔥 FIRES 3/3 |
| `planted` | 11 | **+5.7812** | **+0.8389** | **+5.3014** | 🔥 FIRES 3/3 |
| `pedestal` | 7 | −0.0078 | −0.0092 | −0.0028 | ✅ REFUSES 3/3 |
| `pedestal` | 11 | +0.0000 | +0.0024 | −0.0112 | ✅ REFUSES 3/3 |

동봉 배터리도 CERTIFIED(`plant_crossboundary` gzip +6.6641 · ppm +0.7673 · markov6 +5.9726 /
`plant_null_stream` 0.0000 / +0.0019 / +0.0036). ⟹ **계기도 코퍼스 기하도 살아 있다.**

### ② 처치 3팔 (통제 인증 후에만 읽음)

| arm | seed | gzip | ppm | markov6 | `read` | `geometry_dependent` |
|---|---|---|---|---|---|---|
| `rule-derived` | 7 | **+0.1641** | **+0.0525** | **+0.2396** | 3/3 | 없음 |
| `rule-derived` | 11 | **+0.1680** | **+0.0648** | **+0.2043** | 3/3 | 없음 |
| `midpoint` | 7 | +0.0391 | +0.0354 | +0.0997 | 3/3 | 없음 |
| `midpoint` | 11 | +0.0781 | +0.0347 | +0.1194 | 3/3 | 없음 |
| `shuffled` | 7 | −0.0039 | +0.0074 | −0.0083 | **none** | gzip·ppm |
| `shuffled` | 11 | −0.0312 | −0.0062 | −0.0062 | **none** | gzip·markov6 |

### ③ 사전등록 대비 (판정이 사는 곳)

| 대비 | seed | gzip | ppm | markov6 |
|---|---|---|---|---|
| `rule-derived` − `shuffled` | 7 | +0.1680 | +0.0451 | +0.2479 |
| `rule-derived` − `shuffled` | 11 | +0.1992 | +0.0710 | +0.2105 |
| `rule-derived` − `midpoint` | 7 | +0.1250 | **+0.0171** | +0.1399 |
| `rule-derived` − `midpoint` | 11 | +0.0899 | +0.0301 | +0.0849 |

- **순서 `rule-derived` > `midpoint` > `shuffled` 가 3 추정기 × 2 seed = 6/6 셀에서 성립.**
- `rule-derived` − `shuffled` 는 6/6 셀에서 eps(0.02) 초과 ⟹ 리프트의 출처는 **어휘가 아니라
  짝짓기**다(두 팔의 꿈 라인 다중집합이 바이트 동일).
- `rule-derived` − `midpoint` 는 gzip·markov6 가 2/2 seed 에서 eps 초과, **ppm 은 seed 7 에서
  +0.0171 로 eps 미달**(seed 11 은 +0.0301 통과) ⟹ **order-aware 쌍은 부호는 일치하나 ppm 은
  seed-취약**. 이건 결함이므로 감춤 없이 기록한다.

## 정직한 범위·한계 (읽는 사람이 반드시 같이 읽어야 함)

1. 🔻 **기전은 표면이다.** 선언규칙은 자식 토큰을 부모 토큰의 **축자 복사**로 만들고, 중점은
   **인덱스 산술**로 만든다. gzip/ppm/markov6 는 산술을 못 하고 복사를 본다. 즉 이 결과의 정직한
   서술은 "선언규칙은 결합의존성을 **바이트 스트림에서 읽히게** 만들고, 기하 중점은 결정론적이되
   **읽히지 않게** 만든다" 이다. byte-LM 에겐 이게 바로 관련 진술이지만(스트림에 안 보이는 관계는
   기질이 접근할 경로가 없다), 뻔한 반론도 그대로 성립한다 — **"복사가 압축되는 건 당연하다."**
   `shuffled` 통제는 그 반론의 *어휘* 판본만 막고(같은 라인, 틀린 짝 → 0), *복사 대 계산* 판본은
   **막지 못한다**. 후속이 필요하다.
2. 🔻 **midpoint 는 0 이 아니다** (위 철회). 프로덕션 법칙의 비-평균 부분(부모 id 축자 · radius
   max 선택)이 그 작은 양성을 설명한다. 따라서 "꿈은 정보를 전혀 못 만든다" 가 아니라 "꿈이 지금
   만드는 결합정보는 선언규칙판의 **1/2~1/4** 수준" 이 맞는 진술이다.
3. 🔻 **압축 추정기는 하한**이다. `midpoint` 의 낮은 값은 **읽을 수 있음**의 부재를 한정하지
   정보의 부재를 증명하지 않는다(`a_scale_honest_scope`).
4. 🔻 **DIRECTIONAL, TERMINAL 아님.** 이건 코퍼스 사실이고 모델을 통과시키지 않았다. "학습에
   투입하면 재조합 벽이 열린다" 는 주장은 여기서 **전혀** 나오지 않는다 — `--dream-target` 를
   `anima-py train` 의 replay 소스로 배선하는 것은 미구현 후속이다.
5. 🔻 **shuffled 의 기하의존 양성**: seed 7 win512 에서 gzip +0.1250, seed 11 win512 에서
   markov6 +0.0544 가 뜬다. 최솟값 게이트(H_9844)가 이를 분절 인공물로 정확히 분류했다 — 단일
   기하만 봤다면 "통제도 터진다 ⟹ INVALID" 로 오독했을 것이다. 게이트가 값을 했다.
6. 🔻 **n=23 pairs · 24 밤 · 2 seed.** `MI.MIN_PAIRS`(20)는 넘지만 여유가 크지 않다. 중앙값
   통계라 개별 쌍 노이즈에는 강하나, 팔 간 차이의 신뢰구간은 산출하지 않았다(TOST 미수행).
7. 🔻 **eps 는 계기의 것**(`MI.EPS_BPB`=0.02)을 그대로 썼고 이동시키지 않았다. 블록 크기는
   플래그가 아니라 동결 상수라 조작 표면이 없다.

## H_9831 과의 관계 (중복 아님)

H_9831 은 **혼합비·replay 정책**(error vs uniform)이 DV 였다. 이 카드는 **타깃 자체의 대수**가
DV 다. 두 카드는 직교하며 같은 발사에 합칠 수 있다.

## 후속 (등록 안 함 — 다음 세션 판단)

- **복사 대 계산 분리**: 자식 토큰이 부모 토큰의 축자 복사가 **아니면서** 짝-결정인 팔(예: 선언된
  치환표를 통과한 부모 토큰). 통과하면 (1)의 반론이 죽는다.
- **학습측 배선**: `anima-py train --dream-target …` replay 소스 + `--brain-runtime` 계약
  (R11 공통: 뇌 lane 이 evaluate 경로에서 동일 재실행 안 되면 실패시킴).

**related:** H_9304 · H_9287 · H_9267 · H_9831 · H_9844 · H_9806
