# H_9839 — 꿈의 타깃을 기하 중점에서 선언규칙 파생으로 교체한다 (R12-2)

**status:** 🔻 **SCOPE-NARROWED — 합성 앵커 한정**(2026-07-21 자가반박 · 아래 「실제 앵커 교체」 절).
착륙본의 6/6 양성은 **재현되나**, 앵커 좌표의 출처를 빌더 자신의 균등추첨에서 **생산 303M 의
실제 penultimate 로 바꾸면 사라진다** — `rule-derived − midpoint` 가 6셀 중 **0셀**만 eps 를 넘고
(착륙본 4/6), `rule-derived` 자체가 어느 추정기에서도 읽히지 않는다. 원인은 실제 앵커의
**근공선성**(pairwise cosine mean **0.9213**)이고, 착륙본이 이긴 이유는 선언규칙이 아니라
합성 앵커 세계가 **손으로 만든 근직교 기하**였기 때문이다. ⟹ 이 카드의 양성은
**"합성 근직교 앵커에서의 코퍼스 사실"** 로 범위가 좁혀지며, **dream-mix 학습 지출은 BLOCKED**.

<details><summary>착륙 당시 status (보존 · 위 반박이 무효화한 범위를 그대로 읽을 수 있게)</summary>

🟢 DIRECTIONAL POSITIVE — **코퍼스 사실**(모델 미통과 · $0 · ckpt 0 · GPU 0).
사전등록 판독 **충족**: `rule-derived` 가 기하-강건 최솟값에서 `midpoint` 와 `shuffled` 를
**둘 다** 이겼다 (3 추정기 × 2 seed = 6/6 셀). ⚠️ **TERMINAL 아님** — 학습 판정은 여전히
`anima-py train` + `anima-py evaluate` 몫이고, 압축 추정기는 **하한**이다(읽을 수 있음의 부재를
한정할 뿐 존재의 부재를 증명하지 않는다).

</details>
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census` → `📋 R12`. R11(H_9830~9836)의 후속.
**wired:** ✅ `anima-py corpus dreamgen` (`cli/corpus.py` · VERSION 0.20.97→0.20.98 · G5)
+ ✅ `--dream-anchors synthetic|real:<ckpt.clm>` (실제 앵커 교체 · VERSION 0.20.111→0.20.112 · G5).
판정기 = 오늘 착륙한 `anima-py corpus mi-screen --mi-robust`(H_9844).
학습측 배선(`train --dream-target` replay)은 미구현이며 이제 ⛔ **BLOCKED**(아래 ⑦).

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

---

# 🔻 심화 (2026-07-21) — 앵커를 **실제 303M 표현**으로 교체하니 양성이 죽었다 (자가반박)

## 왜 이걸 했나

같은 날 **H_9838**(CA3 다단계 완성)이 12× 우연·절제 붕괴·3seed×3기하·독립 재현까지 갖춘
헤드라인 양성을 냈다가, **코드 출처만** 심어둔 정수 fixture → 생산 trunk 실제 penultimate 로
바꾸자 16항목이 CERTIFIED → **INVALID**(값-셔플 받침대 0.3750 > 바 0.3077), 32항목도 INVALID
(0.1562 > 0.1500) 로 죽었다. 진단은 **기하**였다 — 심어둔 코드는 사실상 직교(within .0469 /
across .0117)인데 실제 표현은 겹침 2.2배(.0625 / .0260)였고, `core/hippo_lane.py` 헤더가 이미
"Raw single-token 303M reps are near-collinear" 라고 경고하고 있었다.

**이 카드는 모양이 같다.** dreamgen 의 앵커 좌표 — 특히 구성법칙이 실제로 만지는 **슬롯별 토큰
인덱스** — 는 빌더 자신의 `_wp_rand` 가 64-토큰 풀에서 **iid 균등**으로 뽑는다. 그건 부모 둘이
슬롯마다 63/64 확률로 다른 **근직교 세계**이고, `rule-derived` 는 늘 고를 것이 있고 `midpoint` 는
늘 두 부모에서 떨어진 곳에 떨어진다. 실제 303M 앵커가 그 여유를 준다는 보장은 어디에도 없다.

## 개입 (착륙한 플래그 · 입력 출처만 교체)

```
anima-py corpus dreamgen ... --dream-anchors synthetic|real:<ckpt.clm>
```

- `synthetic`(기본) = 착륙본과 **바이트 동일**. 플래그 도입 전과 무회귀.
- `real:<ckpt>` = 앵커의 coord/tension5/radius **및 슬롯 인덱스**를 `core/decode.py`
  `clm_load_weights` → `clm_penult_pooled_W`(py-canonical 실제 pre-readout pooled penultimate)
  로 대체. **그 외 전부 불변** — 밤 수·seed·5팔·구성법칙·차단형 감사 5종·`mi-screen --mi-robust`
  ·eps(0.02)·판독 순서.
- real 경로도 **RNG 추첨을 먼저 그대로 소비한 뒤** 덮어쓴다 ⟹ 규칙열·엔티티 문자열 추첨·표류
  필러·plant 블록·밤 순서가 합성 경로와 바이트 동일하고, **바뀌는 것은 앵커 좌표 하나뿐**이다.

**축소기는 발사 전에 동결**했고 실제 앵커 숫자를 본 뒤 바꾸지 않았다. 두 반쪽 다 **스케일 불변**
(rep 의 단위는 내 설계 선택이 아니므로 절대 스케일이 든 축소기는 기하가 아니라 **단위** 때문에
붕괴/확산한다): 슬롯 인덱스 = 연속 chunk → `|·|` argmax → 위치를 `pos*64//len` 으로 버킷
(`core/decode.py::penult_fold8` 이 이미 이 rep 에 대해 동결해 둔 연속·절대값·argmax 관용구),
coord/t5/radius = chunk 평균을 rep 자신의 mean|·| 로 **나눈 뒤**(스케일 프리 비율)
`_dg_softsign01` 로 (0,1) 사영.

## 재현 커맨드 (통째 · seed 포함)

```bash
python3 -m venv /tmp/venv_h9839r
/tmp/venv_h9839r/bin/pip install -q numpy && /tmp/venv_h9839r/bin/pip install -q --no-deps .
CK=/Users/mini/anima-weights/py303_full.clm
for s in 7 11; do for arm in planted pedestal midpoint rule-derived shuffled; do
  # ① 무회귀(구 경로) — --dream-anchors 생략 = synthetic
  /tmp/venv_h9839r/bin/anima-py corpus dreamgen --out s${s}_${arm}.txt --lang en \
      --dream-target $arm --dream-nights 24 --seed $s
  # ② 교체(신 경로)
  /tmp/venv_h9839r/bin/anima-py corpus dreamgen --out r_s${s}_${arm}.txt --lang en \
      --dream-target $arm --dream-nights 24 --seed $s --dream-anchors real:$CK
  for f in s${s}_${arm} r_s${s}_${arm}; do
    /tmp/venv_h9839r/bin/anima-py corpus mi-screen --corpus $f.txt --mi-robust --out mi_$f.json
  done
done; done
```

## ① 무회귀 — 구 경로는 바이트까지 그대로 (먼저 증명)

`--dream-anchors` 착륙 **전/후** 의 synthetic 코퍼스 sha256 이 **10/10 완전 일치**:

```
8321ddf8657944ba866f28f6d9f0ec59769e605da2b3c6d132d472632c6155c8  s11_midpoint.txt
a7b8684651604842395349a82f13b76a3ffb8e510019f32f20a3cd12b1698245  s11_pedestal.txt
a8988f0b89c38d5688ffa8031da54030bdc91d462faa74253d9d3ebc1706ab99  s11_planted.txt
9c5509d2a6a5317b2c09ddad6a1056094ed18df1225d4015dbd50a03b8e8520b  s11_rule-derived.txt
7a67e35a9c23b729b90b53d05ff7d9624a075bb12b94f8293d68e4b84a389e29  s11_shuffled.txt
b88d6eb40ab82ae90b716bf4ff0e072f1b1e42c9822ffb01958e6b54c074628d  s7_midpoint.txt
3814d1da4db9f00c8f56db48953c05326ecf12d826dff0ad86d5ca140d81e51b  s7_pedestal.txt
ceefa727cbefd1a7597d4fc53c0962c086b04e191afb63a7a344b64417b706a1  s7_planted.txt
f58de51f7965edfad99e2081d4f575bcffcdc56202822b8e352395e362f7061c  s7_rule-derived.txt
a8e919e2671eb6a773d4cc63abc4a97cd652a91e0d43e26f409ad88c822fbcde  s7_shuffled.txt
```

그리고 그 코퍼스들의 `mi-screen --mi-robust` 재측정(**구 경로 · verbatim**):

| arm | seed | gzip | ppm | markov6 | read | battery |
|---|---|---|---|---|---|---|
| `planted` | 7 | +5.8438 | +0.8371 | +5.3128 | 3/3 | CERTIFIED |
| `pedestal` | 7 | −0.0078 | −0.0092 | −0.0028 | 0/3 | CERTIFIED |
| `midpoint` | 7 | +0.0391 | +0.0354 | +0.0997 | 3/3 | CERTIFIED |
| `rule-derived` | 7 | +0.1641 | +0.0525 | +0.2396 | 3/3 | CERTIFIED |
| `shuffled` | 7 | −0.0039 | +0.0074 | −0.0083 | 0/3 | CERTIFIED |
| `planted` | 11 | +5.7812 | +0.8389 | +5.3014 | 3/3 | CERTIFIED |
| `pedestal` | 11 | +0.0000 | +0.0024 | −0.0112 | 0/3 | CERTIFIED |
| `midpoint` | 11 | +0.0781 | +0.0347 | +0.1194 | 3/3 | CERTIFIED |
| `rule-derived` | 11 | +0.1680 | +0.0648 | +0.2043 | 3/3 | CERTIFIED |
| `shuffled` | 11 | −0.0312 | −0.0062 | −0.0062 | 0/3 | CERTIFIED |

```
rule-derived - shuffled  seed 7   gzip +0.1680  ppm +0.0451  markov6 +0.2479
rule-derived - midpoint  seed 7   gzip +0.1250  ppm +0.0171  markov6 +0.1400
rule-derived - shuffled  seed 11  gzip +0.1992  ppm +0.0710  markov6 +0.2105
rule-derived - midpoint  seed 11  gzip +0.0898  ppm +0.0301  markov6 +0.0849
```

⟹ 위 표의 모든 칸이 착륙본 표와 **일치**(markov6 −midpoint seed7 은 카드 표기 +0.1399, 실제
float 는 +0.13996… — 반올림 자릿수 차이). **구 경로 회귀 0.**

## ② 실제 앵커 — 통제 먼저, 동결 순서

| arm | seed | gzip | ppm | markov6 | 판독 |
|---|---|---|---|---|---|
| `planted` | 7 | **+5.8750** | **+0.8396** | **+5.3159** | 🔥 FIRES 3/3 |
| `planted` | 11 | **+5.8438** | **+0.8415** | **+5.3063** | 🔥 FIRES 3/3 |
| `pedestal` | 7 | −0.0078 | −0.0019 | −0.0033 | ✅ REFUSES 3/3 |
| `pedestal` | 11 | −0.0156 | +0.0033 | −0.0100 | ✅ REFUSES 3/3 |

⟹ **계기는 실제 앵커에서도 살아 있다**(양성통제 발화 · 참값0 받침대 거부 · 배터리 CERTIFIED).
따라서 처치 3팔을 읽을 자격이 성립한다.
🔻 다만 정직하게: `planted`/`pedestal` 은 앵커 코드 레인을 **거의 쓰지 않는다**(이 두 팔이 나르는
것은 RNG 고엔트로피 블록이고, 실제 앵커는 `ANCHOR` 줄의 `text=`/좌표만 바꾼다). 즉 이 통제
통과는 **계기·분절·블록배치가 살아 있다**는 뜻이지 **앵커 기하가 건강하다**는 뜻이 아니다.

## ③ 실제 앵커 — 처치 3팔 (통제 인증 후에만 읽음)

| arm | seed | gzip | ppm | markov6 | `read` |
|---|---|---|---|---|---|
| `rule-derived` | 7 | −0.0156 | +0.0111 | −0.0045 | **0/3** |
| `rule-derived` | 11 | +0.0117 | +0.0136 | +0.0579 | 1/3 (markov6) |
| `midpoint` | 7 | −0.0234 | −0.0009 | −0.0109 | **0/3** |
| `midpoint` | 11 | +0.0117 | +0.0125 | +0.0572 | 1/3 (markov6) |
| `shuffled` | 7 | −0.0234 | −0.0146 | −0.0301 | **0/3** |
| `shuffled` | 11 | −0.0312 | +0.0062 | −0.0527 | **0/3** |

## ④ 사전등록 대비 — **판정이 사는 곳**

| 대비 | seed | gzip | ppm | markov6 | eps 초과 |
|---|---|---|---|---|---|
| `rule-derived` − `shuffled` | 7 | +0.0078 | +0.0257 | +0.0256 | 2/3 |
| `rule-derived` − `shuffled` | 11 | +0.0430 | +0.0074 | +0.1106 | 2/3 |
| `rule-derived` − `midpoint` | 7 | +0.0078 | +0.0120 | +0.0064 | **0/3** |
| `rule-derived` − `midpoint` | 11 | +0.0000 | +0.0011 | +0.0007 | **0/3** |

- 사전등록 판독 (ii) **순서 `rule-derived` > `midpoint` > `shuffled` 가 기하-강건 최솟값에서
  성립** — 부호로는 5/6 셀에서 유지되지만(seed7 gzip 은 `midpoint` = `shuffled` = −0.0234 **동률**),
  **세 팔 전부가 eps 아래**라 순서를 읽을 신호 자체가 없다.
- 사전등록 판독 (iii) **`rule-derived` − `midpoint` 가 eps 아래로 붕괴**: 착륙본 4/6 → **0/6**,
  seed 11 은 `+0.0000 / +0.0011 / +0.0007` 로 **사실상 0**. order-aware 쌍이 **완전 소멸**했다.
- `rule-derived` − `shuffled` 도 6/6 → **4/6** 으로 내려갔고, 남은 4셀도 `rule-derived` 자신이
  읽히지 않는(READ 0~1/3) 상태에서 나온 차이라 리프트라고 부를 것이 없다.

⟹ **착륙한 양성은 실제 앵커에서 살아남지 못했다.**

## ⑤ 원인 — 손으로 만든 근직교 기하 (H_9838 과 **같은** 진단)

빌더가 스스로 내놓는 witness(신규 audit 필드 · 판정용 아님 · 차단하지 않음):

```
합성:  168 anchor(s) → 168 distinct code(s) · per-slot distinct [59, 62, 60]
실제(seed 7):  168 anchor(s) → 5 distinct code(s) · per-slot distinct [2, 1, 3]
               real rep geometry: 168 distinct entity string(s)
               · pairwise cosine mean 0.9213 [0.8470 .. 0.9763]
실제(seed 11): 168 anchor(s) → 6 distinct code(s) · per-slot distinct [2, 2, 3]
               · pairwise cosine mean 0.9200 [0.8481 .. 0.9775]
```

- 합성 세계는 64-풀에 **거의 균등**하게 퍼져 있다(슬롯당 distinct 59~62/64) = 두 부모가 슬롯마다
  다를 확률 63/64. **손으로 만든 유리한 기하**다.
- 실제 세계는 168개 서로 다른 엔티티 문자열이 **5~6개 코드**로 붕괴한다. seed 7 에서는 슬롯 1 의
  distinct 가 **1** — 168 앵커 전부가 그 슬롯에서 **같은 토큰**이다.
- 표현 자체의 숫자: pairwise cosine **mean 0.9213**(min 0.8470) = 근공선. H_9838 이 `.0625/.0260`
  으로 진단한 것과 같은 사실을 다른 통화로 잰 것이다.
- 그 결과가 스트림에 그대로 나온다: `rule-derived` 와 `midpoint` 의 꿈 텍스트가 483줄 중
  **352줄(72.9%)** 동일(seed 11 은 336줄 · 69.6%), distinct 꿈 텍스트가 **460 → 5**.
  **규칙이 고를 것이 남지 않는다.**

즉 착륙본의 리프트는 "선언규칙이 결합정보를 만든다" 가 아니라 **"앵커가 균등추첨이라 부모끼리
달랐다"** 였다.

**팔 구성은 무죄**: 실제 앵커에서도 카드 자신의 두 witness 가 성립한다 —
`rule-derived`≡`shuffled` carry multiset sha(seed7 `05fc1266d0e4ac54` · seed11 `a711202045eb982d`),
`midpoint`≡`rule-derived` geometry-field sha(seed7 `8ce24e730c6ce573` · seed11 `37439c5683c32173`).
바뀐 것은 **입력 기하 하나뿐**이다.

## ⑥ 기존 caveat 2건의 실제-앵커 재검

- **ppm seed-취약**(착륙본 `rule−midpoint` ppm +0.0171@seed7 vs +0.0301@seed11): 실제 앵커에선
  ppm 이 두 seed 모두 **+0.0120 / +0.0011** 로 eps 한참 아래 ⟹ seed-취약을 논할 신호가 없다.
  결함이 고쳐진 게 아니라 **대상이 사라졌다**.
- **복사 대 계산**(자식 토큰이 부모 토큰의 축자 복사라는 표면기전): 실제 앵커에선 부모 둘이
  대부분의 슬롯에서 **서로 같아지므로**, "복사냐 계산이냐" 를 가를 대비 자체가 성립하지 않는다.
  후속으로 예정했던 「치환표 팔」은 **이 앵커 위에서는 설계 불가**다.

## ⑦ 골화 (범위 축소) · 무엇이 막히는가

- 🟢 **살아남은 것**: 순서 `rule-derived` > `midpoint` > `shuffled` 는 **합성 근직교 앵커 세계에
  한정된 코퍼스 사실**(DIRECTIONAL). 그 세계에서 6/6 은 재현된다(위 ① 표).
- 🔴 **죽은 것**: 그 순서를 **생산 303M 앵커에 대한 주장**으로 읽는 것. 실제 앵커에서 무효.
- ⛔ **BLOCKED — dream-mix 학습 지출**: `anima-py train --dream-target …` replay 배선(카드의
  「후속 · 학습측 배선」)은 **발사 금지**. 실제 앵커에서 팔 간 대비가 eps 아래인 데이터를 GPU 로
  태우는 것은 순서가 뒤집힌 지출이다. H_9831(혼합비·replay 정책)과 합쳐 쏘려던 계획도 이
  데이터에 관해서는 같은 이유로 보류.
- 🚫 **금지**: 축소기(chunk·abs·argmax·softsign01)·풀 크기·차원·seed 를 바꿔가며 대비가 살아나는
  설정을 찾는 탐색 = 정의상 tune-to-green. 되살리려면 **아래 사전등록 후속** 으로만.

## ⑧ 후속 (사전등록 초안 · **이번 세션에서 실행하지 않음**)

- **앵커 코드 다양성 하한을 팔 판독 전 게이트로 박은 별도 H**: 실제 rep 을 비퇴화 코드로 펼치는
  앵커 인코더(예: 앵커 집합 평균 제거 후 화이트닝, 또는 단일 문자열이 아닌 더 긴 문맥의 rep)를
  도입하되, **팔을 읽기 전에** `distinct_anchor_codes / n_anchors` 가 사전등록된 하한을 넘어야
  한다. 그 하한을 못 넘으면 그 실험은 INSTRUMENT-DEAD 이지 음성이 아니다. 하한·인코더·seed 를
  **측정 전에** 카드에 박고, 통과 여부와 무관하게 그 값을 보고한다.
- 이 후속을 통과하기 전까지 dreamgen 의 어떤 숫자도 실제 303M 앵커에 대한 주장으로 인용 금지.

## H_9831 과의 관계 (중복 아님)

H_9831 은 **혼합비·replay 정책**(error vs uniform)이 DV 였다. 이 카드는 **타깃 자체의 대수**가
DV 다. 두 카드는 직교하며 같은 발사에 합칠 수 있다.

## 후속 (등록 안 함 — 다음 세션 판단)

- **복사 대 계산 분리**: 자식 토큰이 부모 토큰의 축자 복사가 **아니면서** 짝-결정인 팔(예: 선언된
  치환표를 통과한 부모 토큰). 통과하면 (1)의 반론이 죽는다.
- **학습측 배선**: `anima-py train --dream-target …` replay 소스 + `--brain-runtime` 계약
  (R11 공통: 뇌 lane 이 evaluate 경로에서 동일 재실행 안 되면 실패시킴).

**related:** H_9304 · H_9287 · H_9267 · H_9831 · H_9844 · H_9806
