# H_9825 — 얼어붙은 trunk 가 store 를 **주소지정**할 수 있는 천장은 얼마인가?

**status:** 🔧 INSTRUMENT LANDED (계기 착륙 · 판정 PENDING) · DIRECTIONAL 상한
**source:** `lab/v2/hypotheses/V2_7_decode_probe_seed_split.md` (v2 카드 = source, 수치는 이식 안 됨)
**wired:** yes — `anima-py evaluate <clm> --store-retr-probe <dump.npz> [--retr-probe-iters N]`
· 자체검사 `--retr-probe-selftest`

## Question

`--store-addr-census`(H_9719)는 **랜덤** W_q 의 argmax 충돌을 pedestal 과 대조하는 *기하 선별기*라
"기하가 붕괴했나"만 답한다. 답하지 못하는 것은 **"이 trunk 위에서 bolt-on 다리가 도달할 수 있는
검색 정확도의 천장이 얼마인가"** 이다. 이 천장이 없으면 H_9392(bolt-on lane)·H_9720(tap-depth lane)의
음성은 *표상 빈곤*(애초에 못 읽는다)과 *소비/라우팅 실패*(읽히는데 안 쓴다)를 구분하지 못한다.

## Intervention

다리가 실제로 쓰는 선형 질의사상 **W_q(d→d_k) 하나만** 적합한다 — `store_apply` 의
`q = h @ W_q` 와 동일 형태. 점수는 `softmax((h@W)·K[i]/√d_k)` 로 자기 엔티티 키를 고르는 것.
readout·operator gate 는 **격리**(검색 절반만 잰다).

일반화 강제: 엔티티를 **서로소 절반**으로 갈라 train 엔티티(+train 키)에서만 W 를 적합하고,
held-out 엔티티(+held-out 키)에서 읽는다 ⟹ 외운 행이 아니라 *내용주소의 일반화*.
우연 = 1/len(test) 로 **실현 분할에서 유도**(가정 금지 · `chance-level-must-be-derived-per-metric`).

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | 이 ckpt 의 penultimate H | 천장 (DIRECTIONAL) |
| **ORACLE** | H 를 K 의 선형상으로 심음 → 정확한 W 가 **존재** | 양성통제. <0.90 이면 INSTRUMENT-DEAD, 음성 판독 불가 |
| **NULL** | 구조 없는 norm-matched 가우시안 H | 참값 0 PEDESTAL. 우연 초과 = 검색을 **제조**한 것 ⟹ INVALID |

## Gates

- `ORACLE < 0.90` → **INSTRUMENT-DEAD** (`positive-control-before-reading-a-negative`)
- `NULL > max(4×chance, 0.15)` → **INVALID** (`phi-estimator-needs-zero-truth-pedestal`)
- `LIVE <= max(2×chance, 0.15)` → **FLOOR** (주소지정 도달 안 함)
- 그 외 → **REACHABLE** (천장이 열려 있음)

## Result

계기만 착륙. 자체검사 실측(심은 기하 · ckpt 불요):

```
[selftest] n_train=32 n_test=32  chance=0.0312
  ORACLE (planted linear-reachable) acc=1.0000
  NULL   (structureless H)         acc=0.0312   ← 우연과 정확히 일치
  LIVE   (structureless planted)   acc=0.0000
  SELFTEST PASS ✓
```

⟹ **이 가드는 실패할 수 있다**(v2 `gradcheck --selftest` 규율). 이웃 계기
`--store-census-selftest` 회귀 없음. 단일 진입점 `anima-py evaluate` 로 배선 확인(rc=0).

**아직 ckpt 에서 안 쟀다** — 실제 천장 수치는 store-trailer ckpt + `--dump-hidden` npz 로 발사해야 나온다.

## Falsify

- ORACLE 이 1.0 인데 LIVE 가 FLOOR ⟹ 표상 빈곤이 아니라 **주소지정 불가**가 진범.
- LIVE 가 REACHABLE 인데 in-vivo bolt-on 이 여전히 죽으면 ⟹ 벽은 검색이 아니라 **소비/라우팅**.
- NULL 이 우연을 넘으면 이 계기의 모든 수치는 무효 — 적합 자유도가 신호를 만든 것.

## 정직 고지

- DIRECTIONAL **천장**이지 능력 판정이 아니다. 굳히는 것은 303M engine-native 발사뿐.
- v2 의 수치(frozen 0.5134~0.5724 vs cotrained 0.9998~1.0)는 **이식하지 않았다** — v2 는 영구
  DIRECTIONAL 이라 여기 인용은 동기일 뿐 근거가 아니다.
- v2 원본은 예제 스트림에서 뽑은 0-shot 분할을 썼고, 프로덕션 dump 는 엔티티당 hidden 1개라
  **엔티티 분할**로 옮겼다. 같은 질문이지만 같은 수치가 아니다.
- **tap 범위 한계** (H_9720 카드 §40 이 census 에 대해 지적한 것과 같은 한계가 이 probe 에도 있다):
  입력이 `--dump-hidden` 의 **penultimate `__last`** 라서, 주소 질의가 초기층 tap +
  학습된 `W_fresh`/`W_q_fresh` 에서 나오는 **lane_type 5(fresh query lane)의 실제 주소경로는
  판별하지 못한다**. lane_type 1~4(penultimate 질의)에서만 천장이 그 lane 의 천장이다.
  fresh lane 을 재려면 `--dump-hidden` 을 fresh tap 으로 확장해야 한다 — 미착수.

## 발사 재개지점 (미측정)

재료는 있다 — `~/anima-weights/rv3c13.clm` 이 CLMS trailer 보유(lane_type=3 · n_slot=8 · d_k=64).
막힌 곳은 **엔티티 풀 spec 부재**: `--dump-hidden` 은 `{id}__last` 로 저장하므로 id = store 엔티티명인
프롬프트 spec 이 필요한데 repo 에 커밋된 것이 없다(H_9720 은 held-out 128 엔티티를 pod 에서 생성).
판정표는 이미 동결(#4241)됐으므로 남은 자유도는 엔티티 풀뿐 —
**데이터를 보기 전에 spec 을 먼저 동결**해야 shopping 이 아니다. 그 pre-registration 이 다음 단위.
