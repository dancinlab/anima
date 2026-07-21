# H_9842 — 각성 working 링버퍼(cap=20 FIFO)는 재조합의 **기억측 상한**인가 (R12-5)

**status:** 🟡 **DIRECTIONAL · SPLIT** (구조 측정 완료 · 학습 판정 아님)
**source:** R12 뇌부위 census (2026-07-21). 상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` → `🧠 뇌부위 census` → `📋 R12`.
**wired:** ✅ `anima-py corpus wake-coresidency` (`cli/corpus.py`) + `core/wake_memory.py::mem_push_ctx_capped`.

---

## 1. 무엇을 배선했나

재조합은 두 개념의 **공기(共起)** 를 요구한다. `core/wake_memory.py` 의 working 버퍼는
`_working_cap()` 이 **하드코딩 20** 을 돌려주는 FIFO라, 거리 D>20 틱 떨어진 두 앵커는
**동시에 버퍼에 있을 수 없다** — H_9836/H_1394 가 trunk 에서 지적한 수용영역(RF) 한계의
**기억측 쌍둥이**. 그런데 그 용량이 상수라 **스윕할 대상이 없었다**.

| 착륙물 | 내용 |
|---|---|
| `core/wake_memory.py::mem_push_ctx_capped(mem, ctx_tokens, cap)` | 링버퍼 본체에 **용량을 인자로**. 기존 `mem_push_ctx` 는 `_working_cap()` 을 넘겨 위임 ⟹ 모든 기존 호출자(`core/imagination_replay.py`·`cli/chat.py:2192`) **바이트 동일**(아래 §5 검증). py 전용 seam — hexa twin 의 2-인자 표면은 그대로. |
| `cli/corpus.py` fmt `wake-coresidency` | `--wake-buffer-cap`(반복) · `--replay-source working\|episodic\|both` · `--wake-anchors` · `--wake-ticks` · `--wake-eps`. **shipped 함수를 그대로 구동**(재유도 없음) · 모델 0 · ckpt 0 · forward 0. |

`episodic` 팔 = 추가전용(무제한) ⟹ **FIFO 상한 가설의 직접 반증 팔**.

## 2. 재현 커맨드 (통째)

```bash
python3 -m venv /tmp/venv_h9842
/tmp/venv_h9842/bin/pip install -q --force-reinstall --no-deps .   # VERSION 0.20.98

# 입력 코퍼스 3종 (전부 결정적 · seed 7)
/tmp/venv_h9842/bin/anima-py corpus flat               --lang en --seed 7 --out flat_en.txt
/tmp/venv_h9842/bin/anima-py corpus derivtrace         --lang en --seed 7 --out deriv_en.txt
/tmp/venv_h9842/bin/anima-py corpus counterfactual-decl --lang en --seed 7 --held-out 32,8 --out decl_en.txt

# 측정 (약 19 초 · $0)
/tmp/venv_h9842/bin/anima-py corpus wake-coresidency \
    --corpus flat_en.txt --corpus deriv_en.txt --corpus decl_en.txt \
    --wake-ticks 6540 --out wake_h9842.json
```

`flat_en.txt` sha256 = `7b808eee65e24f6119a36c0207b3e1b8b06910c580a536454625a7d27ee34ffa` (798,570 B · 6,540 줄).

## 3. 통제 — **먼저** 돌고, 둘 다 통과해야 코퍼스 행이 나온다 (frozen 순서)

`run_mi_screen` 과 동일한 계약: 미통과 시 `INSTRUMENT-DEAD`/`INVALID` + **코퍼스 숫자 0개** + `exit 3`.

실측 (verbatim, `wake_h9842.json`):

```json
"status": "CERTIFIED",
"why": "both controls behaved: the planted spacing fires, the saturated stream refuses.",
"battery": {
  "plant_crossboundary": {          // 앵커 8개를 50틱 간격으로 1회씩 심음 (참값 기지)
    "n_ticks": 400, "n_pairs": 28,
    "working": { "20": 0.0, "64": 0.25, "256": 0.8929 },
    "episodic": 1.0, "cap_delta": 0.8929, "read_ceiling": true
  },
  "plant_null_stream": {            // 0-참값 받침: 모든 앵커를 매 틱 push (용량 의존성 = 0)
    "n_ticks": 400, "n_pairs": 28,
    "working": { "20": 1.0, "64": 1.0, "256": 1.0 },
    "episodic": 1.0, "cap_delta": 0.0, "read_ceiling": false
  },
  "plant_fires": true, "null_refuses": true, "certified": true
}
```

양성통제 값은 닫힌형과 일치한다(간격 50 · 쌍 |i−j|·50 ≤ C−1 ⟹ C=20 에서 0/28, C=64 에서 7/28=0.25,
C=256 에서 25/28=0.8929) — 계기가 링버퍼를 **실제로 읽고 있다**는 뜻.

## 4. 실측 — 공기(共起) 인구조사

`working[C]` = 두 앵커가 모두 등장하는 쌍 중 **cap C FIFO 안에 언젠가 동시 상주**한 비율.
분모는 스트림에서 직접 계산(버퍼 경유 아님) ⟹ `episodic` 의 1.0 은 정의가 아니라 **측정**이다.

```
== flat_en.txt    CEILING-DEAD  knob_dependent=False   (types 74)
   k=24  top   w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=24  mid   w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=24  rare  w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=12  (top/mid/rare 전부 동일 · 1.0000)
== deriv_en.txt   CEILING-DEAD  knob_dependent=False   (types 100)
   k=24  top   w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=24  mid   w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=24  rare  w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000
   k=12  (전부 동일 · 1.0000)
== decl_en.txt    SPLIT         knob_dependent=False   (types 298)
   k=24  top   w20=0.9964 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0036   read=False
   k=24  mid   w20=0.2899 w64=0.6522 w256=0.9819 ep=1.0000  Δcap=+0.6920   read=True
   k=24  rare  w20=0.0290 w64=0.0870 w256=0.2138 ep=1.0000  Δcap=+0.1848   read=True
   k=12  top   w20=1.0000 w64=1.0000 w256=1.0000 ep=1.0000  Δcap=+0.0000   read=False
   k=12  mid   w20=0.2727 w64=0.7273 w256=0.9697 ep=1.0000  Δcap=+0.6970   read=True
   k=12  rare  w20=0.0152 w64=0.0455 w256=0.0909 ep=1.0000  Δcap=+0.0757   read=True
```

**판독 — 카드의 원 주장은 반만 산다.**

- 🔴 **anima 가 실제로 학습하는 ρ·weave 코퍼스(`flat`·`derivtrace`)에서는 상한이 없다.**
  cap=20 에서 이미 **모든** 앵커 쌍이 공기한다(1.0000, 3 지층 × 2 knob 전부). 어휘가 74~100 종뿐이라
  무엇이든 몇 틱 안에 재등장한다 ⟹ 여기서 버퍼 용량을 키우는 것은 **레버가 아니다**. 카드가 예고한
  대로 "co-residency 가 cap=20 에서 이미 높으면 가설은 오늘 죽는다" — 이 두 코퍼스에서는 **죽었다**.
- 🟡 **어휘가 큰 코퍼스(`counterfactual-decl`, 298 종 · 일회성 stem 풀)에서는 상한이 실재하고 크다.**
  중빈도 지층에서 cap=20 은 쌍의 **29.0% 만** 공기시키고 cap=256 은 **98.2%** 로 올린다(Δ +0.692).
  희소 지층은 cap=256 로도 21.4% 에 그치고 **episodic(무제한)만 1.0** 을 낸다.
  ⟹ 용량은 이 regime 에서 **실제 상한**이고, `--replay-source episodic` 이 그것을 완전히 없앤다.
- 결론: **버퍼 용량은 코퍼스-조건부 상한이다.** 상한이 무는지 여부를 결정하는 것은 용량이 아니라
  **스트림의 앵커 재등장 간격 분포**다. anima 의 현 재조합 코퍼스는 그 분포가 너무 조밀해서
  상한에 닿지 않는다.

## 5. 튠-투-그린 방지 (knob 이 판정을 못 뒤집게)

판정을 흔들 수 있는 knob 3개를 전부 스윕했고 **전부 일치**했다.

| knob | 값 | 결과 |
|---|---|---|
| 앵커 집합 크기 | k = 24, 12 | `knob_dependent=False` (3 코퍼스 전부) |
| 앵커 빈도 지층 | top / mid / rare | 지층별로 갈리면 `SPLIT` 으로 **표시**하고 지층 하나를 고르지 않음 |
| 틱 예산 | 3000 / 6540 / 12000 | decl 의 verdict `SPLIT` 불변 · 지층별 read 패턴(top False · mid True · rare True) **9/9 일치** |

틱 예산 스윕 실측(decl · k=24 mid): `w20` 0.2717(3000) / 0.2899(6540) / 0.4746(12000),
`w256` 0.8913 / 0.9819 / 1.0000 — 값은 움직이지만 **부호도 판정도 안 움직인다**.

**기본 경로 바이트 동일성 검증** (origin/main 본문을 그대로 옮겨 500 push 대조):

```
default path identical to origin/main: True · len(working) = 20
capped(64) working len after 300 pushes: 64
```

## 6. 정직한 범위 — 이건 **구조** 사실이지 행동 사실이 아니다

1. **살아있는 데몬은 내용을 push 하지 않는다.** `cli/chat.py:2192` = `mem_push_ctx(wake_mem,
   [tick, stage, cell_count])` — **시계 삼중항**(H_9422 가 이미 지적). 내용-앵커 스트림은
   **반사실(counterfactual)** 이다: "내용을 나르는 percept 가 생긴다면 만날 천장" 을 잰 것이고,
   그 percept 는 아직 없다.
2. **`wake_memory` 는 train 진입점이 0이다**(ARCHITECTURE R12 census: `core/` 12모듈 중 하나).
   따라서 이 상한은 **아직 아무도 만들지 않은 replay lane 의 선결 조건**이지 학습 결과가 아니다.
   원 카드의 Intervention 문구 `anima-py train --wake-buffer-cap …` 는 **오늘 착륙 불가** —
   그 플래그가 바꿀 학습 경로 자체가 없다(배관을 먼저 만들면 그건 H_9841/H_9839 의 몫).
   **이 카드는 그래서 `train` 이 아니라 `corpus` 계측으로 착륙했다.**
3. 압축/추정 없음 — 순수 조합 사실이라 통계 검정력 이슈는 없으나, **DIRECTIONAL**:
   재조합 능력이 실제로 공기에 의존한다는 것은 여기서 증명되지 않았다(그건 학습 실험).

## 7. 다음

- 상한이 무는 유일한 regime(대어휘·일회성 엔티티 풀)은 정확히 store-bridge/H_9800 계열의 regime이다.
  ⟹ replay lane 을 만들 때 **`--replay-source episodic` 을 기본으로 하면 상한 문제는 발생 전에 사라진다**
  (용량을 20→256 로 키우는 것보다 싸고 완전하다: 희소 지층 0.2138 vs 1.0000).
- `flat`/`derivtrace` 에서 버퍼 용량 스윕에 GPU 예산을 쓰는 것은 **금지** — 오늘 $0 로 죽었다.

**related:** H_9836 · H_9841 · H_9839 · H_9422 · H_9800
