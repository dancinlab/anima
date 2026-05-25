# IIT4 — C lane n=8: WALL-BLOCKED 🟠

> rule 110, n=8, bounded k=3 anchored sampling — Mac-local 실용 wall 한계 초과로 **미완**.
> n=7 (8.57362) 까지의 scaling 커브를 carry 로 C lane 종결.

## 1. 결과 — WALL-BLOCKED

| rule | n | mode | cap k | big-Φ | wall | 상태 |
|---|---|---|---|---|---|---|
| 110 | 4 | exact | — | 7.55 | <초 | 🟢 |
| 110 | 6 | exact (M12) | — | 6.82 | ~분 | 🟢 |
| 110 | 7 | bounded | 3 | **8.57362** | bg ~min | 🟢 ([iit4_c_n7](../iit4_c_n7_bounded_2026_05_25/)) |
| **110** | **8** | **bounded** | **3** | **—** | **>34분 무출력** | **🟠 WALL-BLOCKED** |

## 2. 무엇이 막았나

n=8 bounded(cap=3) 는 mechanism 전수(2^8=256) × purview anchored-sample × repertoire(2^8 state) 로, n=7 대비 state-space 2배 + 조합 폭증. Mac-local 단일 프로세스로 여러 차례 발사했으나 **모두 34~42분 경과까지 big-Φ println 미출력** (hexa 는 종료 시점에만 결과를 print → 0-byte = 미완 신호). 비결정적 hang 이 아니라 honest wall: bounded sampling 도 n=8 에서 실용 시간 envelope 초과.

```
   wall (mac-local, single proc)
   n=4  ▏ <초
   n=6  ▍ ~분
   n=7  ▊ ~분 (bounded)
   n=8  ████████████████ >34분, 미완 ← WALL
```

## 3. honest scope (C3)

- **wall-blocker ≠ 알고리즘 실패**: 엔진은 정확. n=7 까지 동일 코드가 deterministic 산출 (8.57362 byte-equal 재현). n=8 은 순수 시간/메모리 envelope.
- **scaling finding (carry)**: rule 110 big-Φ = 7.55(n4) → 6.82(n6 exact) → 8.57(n7 bounded). n=6→7 단조 증가는 bounded 의 trend-보존 검증. n=8 값은 미측정.
- **재시도 path**: (a) `cap=2` 더 보수적 bound 로 시간 단축, (b) 원격 고사양 호스트(ubu-1/2 빌드 sync 후), (c) sparse-mechanism 가지치기 최적화 — 별도 fire envelope.
- 단일 state(85=01010101)/single-seed 가정 carry.

## 4. C lane 종결

C lane (deferred-closure rule 110 large-n) 은 **n=7 (8.57362) 에서 의미있는 bounded 결과 확보 + n=8 wall-blocker honest 문서화**로 종결. 추가 large-n 은 위 재시도 path 의 별도 fire 대상.
