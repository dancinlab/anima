# H_9843 — .kosmos 지속 앵커를 학습 실행 사이로 이월한다 (R12-6)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/kosmos_io.py`(470줄): `.kosmos` 앵커 포맷(kosmos/1.1) 읽기/쓰기 · `map_8factor_to_5channel` ·
`tension_5ch_to_embedding`(LCG + Box-Muller) · `create_anchor` · `emit_anchor_from_v3` ·
`load_anchors`. **분리된 연구 lane(retrieve/merge/CA3)은 여기 없고 `hippo_lane.py` 에 있다**(헤더 명시).

## 가설과 그 약점 (약점을 먼저)

`a_kosmos` 는 정체성 지속을 `.kosmos` 로 본다. 그러나 **H_9789 에서 self-anchor 는 VOID** 로 끝났다
— 자기앵커 축은 이미 죽었다. 따라서 "정체성을 학습으로 잇는다"는 각도는 **재생성 금지**다.

살아있는 좁은 각도는 정체성이 아니라 **데이터**다: 앵커 저장소가 실행 사이에 살아남으면
H_9838(CA3)의 저장소가 한 번의 학습에 갇히지 않고 **누적**된다. 즉 이 카드는 H_9838 의 **공급선**.

## Intervention

```
anima-py train --kosmos-carry <path.kosmos> --kosmos-carry-mode {ro,append}
```

## 통제

| arm | 읽는 법 |
|---|---|
| 빈 `.kosmos` | 이월 없음 기준선 |
| **셔플된 앵커** | 같은 개수·같은 분포, 내용만 치환 — 붕괴해야 (누적이 정보인지 부피인지) |

## 판독가능성

H_9838 이 먼저 양성이어야 의미가 있다. **선후 종속** · 단독 발사 금지.

**related:** H_9789 · H_9838 · H_9842
