# H_9906 — `--store-query every-token` 은 출하됐는데 **읽을 수 있는 평가 경로가 없다** (계기 공백)

**tier:** 🔧 계기 공백 실측 (2 팔 × 2 조건 · 토이 · $0 · 새 코드 0줄) · **DIRECTIONAL** · NOT a substrate verdict
**group:** R13-instrument-audit
**date:** 2026-07-22
**source:** [[H_9904]] 의 교체 반증법을 실행하다 발견 — 원 시험이 왜 무효였는지의 **근본 원인**
**wired:** n/a (기존 계기의 한계를 특정하는 카드)
**verdict:** `every-token` 은 확증도 반증도 아닌 **측정 불가** 상태다

## 무엇을 쟀나 — 2 팔 × 2 조건, 판독기준은 데이터 전에 동결

`anima-py evaluate ~/anima-weights/store_struct_toy/toy.clm --store <manifest>` (128 items)

| 매니페스트 | A `qpos·overwrite` | B `every-token·gated-add` |
|---|---|---|
| 원본 (`is lumer => `) | 126/128 = **0.9844** | 126/128 = **0.9844** (셀별까지 동일) |
| 마커 제거 (`is lumer `) | **0/0 = 0.0000** | **0/0 = 0.0000** |

동결했던 판독표(3칸)와 실제 결과:

- A′ 무응답 ∧ B′ 응답 ⟹ 판별식 성립 — **미발생**
- **A′ 무응답 ∧ B′ 무응답 ⟹ 계기가 every-token 을 원리적으로 못 봄** — ✅ **이 칸**
- A′ 응답 ⟹ 마커 제거 실패 = 무효 — 미발생 (잔여 `=> ` 0 확인)

## 근본 원인 (코드 · 추정 아님)

`cli/evaluate.py::_predict`:

```python
clm.set_clms_store(..., query=store_query, fuse=store_fuse)   # 플래그는 정상 전달
logits = np.asarray(clm._fwd_logits(W, tok, T))
qp = _clms.find_qpos(tok)      # ← 모드와 **무관하게** 항상 호출
if not qp: return None         # ← 마커 없으면 전 항목 None ⟹ 분모 0
row = logits[qp[-1]]           # ← 마커 있어도 **qpos 행 하나만** 채점
```

**양쪽이 다 막힌다.**

```
마커 있음 →  채점기가 qpos 행만 봄
             그 행에서 overwrite(λ·s) 와 gated-add(logits+λ·s) 는
             레인이 강학습(0.9844)이라 2지선다 argmax 를 같은 쪽으로 몰아
             ⟹ 두 모드가 **원리적으로** 구별 불가 (실측: 소수점까지 동일)

마커 없음 →  find_qpos 가 빈값 ⟹ 전 항목 None ⟹ 분모 0
             ⟹ 아무것도 못 잰다
```

그런데 `every-token` 의 **존재 이유가 바로 마커 없는 자유 생성**이다 (H_9695 주석:
"free ideation carries no marker"). 즉 이 플래그가 쓰이도록 설계된 조건이
**평가 하네스가 아무것도 반환하지 못하는 조건과 정확히 일치**한다.

## 판정 — 제3의 상태

`--store-query every-token` 은 **작동한다고도 죽었다고도 말할 수 없다.**
플래그는 출하됐고(`--help` 에 문서화), 인자 검증도 있고(`every-token` 은 `gated-add` 를 강제),
`store_apply` 까지 전달된다. 그런데 **그 효과를 읽는 평가 경로가 저장소에 없다.**

⟹ 이 플래그로 발사하면 나오는 결과는 둘 중 하나다:
**거짓-동일**(마커 있음) 또는 **0/0**(마커 없음). 어느 쪽도 판독 불가다.
[[instrument-never-run-hides-multiple-bugs]] 의 교과서 사례 — 한 번도 실효 판독된 적 없는 계기.

## [[H_9904]] 에 미치는 영향 (정직한 분리)

- **유지(실증됨)**: `toy.clm` 이 `CLMX`+`CLMS` 트레일러를 담고(406,763 B) 디코더가 읽어
  답위치 로짓을 바꿔 **0.9844** 를 낸다 ⟹ "파일에 없는 헤드는 mouth 가 못 읽는다"([[H_9903]] 전제)의
  살아있는 반례. 포맷이 decode-time join 을 막지 않는다는 결론 불변.
- **미측정으로 강등**: 그 join 을 **다중바이트 스팬**으로 넓히는 `every-token` 경로.
  [[H_9904]] 가 "다중바이트 커버 가능" 을 시사했으나 **현 계기로는 확인 불가**다. 보류.

## 필요한 계기 (다음 사람 · 이게 이 카드의 산출)

`_predict` 의 qpos 하드와이어를 우회하는 판독 하나면 된다. 둘 중 아무거나:

1. **전 행 로짓 대조** — `‖logits_B − logits_A‖₁` 를 그대로 보고(0 이면 경로 사망,
   >0 이면 생존). 2지선다 argmax 를 거치지 않으므로 두 모드를 반드시 가른다.
2. **마커 없는 창의 자유 디코드 채점** — `find_qpos` 대신 마지막 행(또는 생성 스팬 전체)을
   읽는 readout. 조성 lane 이 필요로 하는 다중바이트 채점과 **같은 요구사항**이라
   한 번 만들면 두 캠페인이 같이 쓴다.

⚠️ 이 카드는 **계기 판정**이지 기질 판정이 아니다. cement 는 engine-native `anima-py` 로만.
재현: 위 두 매니페스트(원본 · `=> ` 제거본)로 4회 실행.
